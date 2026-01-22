"""
Resilient Workflow Runtime Wrapper

This module provides a wrapper around the Dapr WorkflowRuntime that automatically
reconnects when the gRPC connection to Diagrid Catalyst is terminated due to idle timeout.

The Diagrid infrastructure terminates idle gRPC connections after ~57 seconds, causing
workflow workers to stop listening. This wrapper monitors the connection and restarts
the runtime when disconnection is detected.

Usage:
    from common.resilient_workflow_runtime import ResilientWorkflowRuntime

    # Create resilient runtime
    runtime = ResilientWorkflowRuntime()

    # Register workflows and activities (same API as WorkflowRuntime)
    runtime.register_workflow(my_workflow)
    runtime.register_activity(my_activity)

    # Start with auto-reconnect (blocking)
    runtime.start()
"""

import logging
import threading
import time
from typing import Optional, List, Callable, Any

import dapr.ext.workflow as wf


class ResilientWorkflowRuntime:
    """
    Wrapper around WorkflowRuntime that handles automatic reconnection.

    Monitors the worker thread and restarts the runtime when disconnected.
    """

    def __init__(
        self,
        reconnect_delay_seconds: float = 2.0,
        max_reconnect_attempts: int = 0,  # 0 = unlimited
        health_check_interval_seconds: float = 5.0,
    ):
        self._logger = logging.getLogger('ResilientWorkflowRuntime')
        self._reconnect_delay = reconnect_delay_seconds
        self._max_reconnect_attempts = max_reconnect_attempts
        self._health_check_interval = health_check_interval_seconds

        # Track registered workflows and activities for re-registration on reconnect
        self._workflows: List[tuple] = []  # [(fn, name), ...]
        self._activities: List[tuple] = []  # [(fn, name), ...]

        self._runtime: Optional[wf.WorkflowRuntime] = None
        self._running = False
        self._reconnect_count = 0
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def register_workflow(self, fn: Callable, *, name: Optional[str] = None):
        """Register a workflow function. Will be re-registered on reconnection."""
        # Clear any previous registration flags
        if hasattr(fn, '_workflow_registered'):
            delattr(fn, '_workflow_registered')
        self._workflows.append((fn, name))
        self._logger.info(f"Queued workflow '{fn.__name__}' for registration")

    def register_activity(self, fn: Callable, *, name: Optional[str] = None):
        """Register an activity function. Will be re-registered on reconnection."""
        # Clear any previous registration flags
        if hasattr(fn, '_activity_registered'):
            delattr(fn, '_activity_registered')
        self._activities.append((fn, name))
        self._logger.info(f"Queued activity '{fn.__name__}' for registration")

    def _create_and_start_runtime(self) -> bool:
        """Create a new WorkflowRuntime and register all workflows/activities."""
        try:
            self._logger.info("Creating new WorkflowRuntime...")
            self._runtime = wf.WorkflowRuntime()

            # Re-register all workflows
            for fn, name in self._workflows:
                # Clear registration flag to allow re-registration
                if hasattr(fn, '_workflow_registered'):
                    delattr(fn, '_workflow_registered')
                if name:
                    self._runtime.register_workflow(fn, name=name)
                else:
                    self._runtime.register_workflow(fn)

            # Re-register all activities
            for fn, name in self._activities:
                # Clear registration flag to allow re-registration
                if hasattr(fn, '_activity_registered'):
                    delattr(fn, '_activity_registered')
                if name:
                    self._runtime.register_activity(fn, name=name)
                else:
                    self._runtime.register_activity(fn)

            # Start the runtime
            self._runtime.start()
            self._logger.info("WorkflowRuntime started successfully")
            return True

        except Exception as e:
            self._logger.error(f"Failed to create/start WorkflowRuntime: {e}")
            return False

    def _check_worker_health(self) -> bool:
        """
        Check if the worker is still healthy.

        Returns True if healthy, False if disconnected or dead.
        """
        if self._runtime is None:
            return False

        try:
            # Access the internal worker to check its state
            worker = self._runtime._WorkflowRuntime__worker

            # Check if the main run loop thread is alive
            # The durabletask worker uses _runLoop as the main thread
            if hasattr(worker, '_runLoop') and worker._runLoop:
                return worker._runLoop.is_alive()

            # If we can't check the thread, assume it's running
            # (this is a fallback for different SDK versions)
            return True

        except Exception as e:
            self._logger.warning(f"Error checking worker health: {e}")
            return False

    def _monitor_and_reconnect(self):
        """Background thread that monitors connection and handles reconnection."""
        self._logger.info("Connection monitor started")

        while self._running and not self._stop_event.is_set():
            # Wait for health check interval
            if self._stop_event.wait(self._health_check_interval):
                break  # Stop event was set

            if not self._running:
                break

            # Check worker health
            if not self._check_worker_health():
                self._logger.warning("Worker disconnected, attempting reconnection...")

                # Shutdown old runtime if exists
                if self._runtime:
                    try:
                        self._runtime.shutdown()
                    except Exception:
                        pass
                    self._runtime = None

                # Attempt reconnection
                self._reconnect_count += 1
                if self._max_reconnect_attempts > 0 and self._reconnect_count > self._max_reconnect_attempts:
                    self._logger.error(f"Max reconnection attempts ({self._max_reconnect_attempts}) reached")
                    self._running = False
                    break

                self._logger.info(f"Reconnection attempt #{self._reconnect_count}")

                # Wait before reconnecting
                time.sleep(self._reconnect_delay)

                if self._create_and_start_runtime():
                    self._logger.info("Reconnection successful")
                else:
                    self._logger.error("Reconnection failed, will retry...")

        self._logger.info("Connection monitor stopped")

    def start(self):
        """
        Start the workflow runtime with automatic reconnection.

        This method is non-blocking - it starts the runtime and a monitor thread.
        """
        if self._running:
            self._logger.warning("Runtime already running")
            return

        self._running = True
        self._stop_event.clear()
        self._reconnect_count = 0

        # Create and start initial runtime
        if not self._create_and_start_runtime():
            self._logger.error("Failed to start initial runtime")
            self._running = False
            return

        # Start monitor thread
        self._monitor_thread = threading.Thread(
            target=self._monitor_and_reconnect,
            name="WorkflowRuntimeMonitor",
            daemon=True
        )
        self._monitor_thread.start()

    def shutdown(self):
        """Stop the workflow runtime and monitor."""
        self._logger.info("Shutting down resilient runtime...")
        self._running = False
        self._stop_event.set()

        # Stop monitor thread
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=5.0)

        # Shutdown runtime
        if self._runtime:
            try:
                self._runtime.shutdown()
            except Exception as e:
                self._logger.warning(f"Error during runtime shutdown: {e}")
            self._runtime = None

        self._logger.info("Resilient runtime shutdown complete")

    @property
    def reconnect_count(self) -> int:
        """Number of reconnection attempts since start."""
        return self._reconnect_count

    @property
    def is_running(self) -> bool:
        """Whether the runtime is currently running."""
        return self._running
