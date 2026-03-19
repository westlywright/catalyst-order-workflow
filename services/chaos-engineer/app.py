import json
import logging
import os
import random
import string
import sys
import time
import uuid

# Add parent directory to path for common imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import dapr.ext.workflow as wf
from common.resilient_workflow_runtime import ResilientWorkflowRuntime
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from flask import Flask, request, jsonify, make_response, url_for
from markupsafe import escape
from typing import Dict, List, Optional, Any
from dapr.clients import DaprClient

APP_PORT = os.getenv("APP_PORT", "3010")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)

# Failure simulation configuration
FAILURE_RATE = float(os.getenv("FAILURE_RATE", "0.3"))  # 30% default failure rate
ENABLE_CHAOS = os.getenv("ENABLE_CHAOS", "false").lower() == "true"

class FailureType(Enum):
    TIMEOUT = "timeout"
    SERVICE_UNAVAILABLE = "service_unavailable"
    RATE_LIMITED = "rate_limited"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"
    MEMORY_ERROR = "memory_error"
    AUTHENTICATION_ERROR = "authentication_error"
    DEPENDENCY_FAILURE = "dependency_failure"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    INTERMITTENT_ERROR = "intermittent_error"
    # Advanced workflow-specific failure types
    EXTERNAL_EVENT_STARVATION = "external_event_starvation"
    CHILD_WORKFLOW_ZOMBIE = "child_workflow_zombie"
    ACTIVITY_EXECUTION_LIMBO = "activity_execution_limbo"
    DISTRIBUTED_TRANSACTION_FAILURE = "distributed_transaction_failure"

class EventSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class RetryPolicy(Enum):
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    FIXED_INTERVAL = "fixed_interval"
    LINEAR_BACKOFF = "linear_backoff"
    NO_RETRY = "no_retry"

@dataclass
class ChaosScenario:
    id: str
    name: str
    description: str
    failure_type: str
    target_service: str
    failure_rate: float
    duration_seconds: int
    enabled: bool
    created_at: str

@dataclass
class DiagnosticEvent:
    id: str
    timestamp: str
    severity: str
    service: str
    workflow_id: str
    event_type: str
    message: str
    details: Dict[str, Any]
    correlation_id: str
    retry_count: int = 0
    execution_time_ms: int = 0

@dataclass
class RetryAttempt:
    attempt: int
    timestamp: str
    delay_ms: int
    error_message: str
    will_retry: bool

@dataclass
class FailureScenarioResult:
    scenario_id: str
    success: bool
    execution_time_ms: int
    retry_attempts: List[RetryAttempt]
    final_error: Optional[str]
    diagnostic_events: List[DiagnosticEvent]

@dataclass
class WorkflowFailureState:
    """Track workflow-specific failure states"""
    workflow_id: str
    failure_type: str
    target_service: str
    started_at: str
    expected_recovery_time: Optional[str] = None
    zombie_child_ids: List[str] = None
    blocked_activities: List[str] = None
    missed_events: List[str] = None

@dataclass
class ZombieWorkflowInfo:
    """Information about zombie child workflows"""
    child_workflow_id: str
    parent_workflow_id: str
    stuck_activity: str
    time_stuck_seconds: int
    simulated_hang_reason: str

@dataclass
class MissedEventInfo:
    """Information about missed external events"""
    workflow_id: str
    event_name: str
    expected_at: str
    timeout_at: str
    event_source: str

# In-memory storage for chaos scenarios and events
chaos_scenarios: Dict[str, ChaosScenario] = {}
diagnostic_events: List[DiagnosticEvent] = []
active_failures: Dict[str, datetime] = {}

# Advanced failure state tracking
workflow_failure_states: Dict[str, WorkflowFailureState] = {}
zombie_workflows: Dict[str, ZombieWorkflowInfo] = {}
missed_events: Dict[str, MissedEventInfo] = {}
hanging_activities: Dict[str, List[str]] = {}  # service -> list of hanging activity types

# Helper function to safely convert scenario to dict (handles both dataclass and dict inputs)
def scenario_to_dict(scenario):
    """Safely convert scenario to dictionary, handling both dataclass and dict inputs"""
    if scenario is None:
        return {}
    if isinstance(scenario, dict):
        return scenario

    # Try to use asdict for proper dataclass instances
    try:
        return asdict(scenario)
    except TypeError:
        # Fallback: manually create dict if asdict fails
        if hasattr(scenario, 'id') and hasattr(scenario, 'name'):
            return {
                'id': getattr(scenario, 'id', ''),
                'name': getattr(scenario, 'name', ''),
                'description': getattr(scenario, 'description', ''),
                'failure_type': getattr(scenario, 'failure_type', ''),
                'target_service': getattr(scenario, 'target_service', ''),
                'failure_rate': getattr(scenario, 'failure_rate', 0.0),
                'duration_seconds': getattr(scenario, 'duration_seconds', 0),
                'enabled': getattr(scenario, 'enabled', True),
                'created_at': getattr(scenario, 'created_at', '')
            }
        else:
            # Last resort: return debug info
            return {
                "error": "unable_to_serialize",
                "type": str(type(scenario)),
                "value": str(scenario)
            }

# Workflow that demonstrates failure handling and retry patterns
def chaos_resilience_workflow(ctx: wf.DaprWorkflowContext, scenario: ChaosScenario):
    """
    Workflow that demonstrates failure handling, retry patterns, and diagnostic event generation
    """
    # Convert to dataclass if it's a dict (due to Dapr serialization)
    if isinstance(scenario, dict):
        scenario = ChaosScenario(**scenario)
    elif scenario is None:
        raise ValueError("Scenario cannot be None")

    # Verify we have a proper scenario object
    if not hasattr(scenario, 'id') or not hasattr(scenario, 'name'):
        raise ValueError(f"Invalid scenario object: missing required attributes")

    correlation_id = str(uuid.uuid4())

    yield ctx.call_activity(announce_chaos_workflow_started, input={
        "message": f"Starting chaos resilience workflow for scenario: {scenario.name}",
        "details": {"scenario": scenario_to_dict(scenario)},
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    # Phase 1: Pre-failure system check
    yield ctx.call_activity(announce_baseline_health_check_started, input={
        "message": "Performing pre-failure system health check",
        "details": {"phase": "pre_failure_check"},
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    health_check = yield ctx.call_activity(perform_baseline_system_health_check, input=scenario)

    # Phase 2: Inject failure and test resilience
    yield ctx.call_activity(announce_failure_injection_started, input={
        "message": f"Injecting {scenario.failure_type} failure into {scenario.target_service}",
        "details": {
            "failure_type": scenario.failure_type,
            "target_service": scenario.target_service,
            "failure_rate": scenario.failure_rate
        },
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    # Enable the failure scenario
    yield ctx.call_activity(activate_chaos_failure_scenario, input=scenario)

    # Test resilience with retry patterns
    resilience_results = []

    for test_round in range(3):  # Run 3 test rounds
        yield ctx.call_activity(announce_resilience_test_round_started, input={
            "message": f"Starting resilience test round {test_round + 1}",
            "details": {"test_round": test_round + 1, "total_rounds": 3},
            "correlation_id": correlation_id,
            "workflow_id": ctx.instance_id
        })

        # Test different retry policies
        retry_policies = [RetryPolicy.EXPONENTIAL_BACKOFF, RetryPolicy.FIXED_INTERVAL, RetryPolicy.LINEAR_BACKOFF]

        for policy in retry_policies:
            test_result = yield ctx.call_activity(execute_retry_policy_test, input={
                "scenario": scenario_to_dict(scenario),
                "retry_policy": policy.value,
                "correlation_id": correlation_id,
                "test_round": test_round + 1
            })
            resilience_results.append(test_result)

            # Add delay between tests
            yield ctx.call_activity(announce_retry_test_delay, input={
                "message": f"Waiting between retry policy tests",
                "details": {"delay_seconds": 2},
                "correlation_id": correlation_id,
                "workflow_id": ctx.instance_id
            })

            yield ctx.create_timer(ctx.current_utc_datetime + timedelta(seconds=2))

    # Phase 3: Circuit breaker simulation
    yield ctx.call_activity(announce_circuit_breaker_test_started, input={
        "message": "Testing circuit breaker patterns",
        "details": {"test_type": "circuit_breaker"},
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    circuit_breaker_result = yield ctx.call_activity(execute_circuit_breaker_test, input={
        "scenario": scenario_to_dict(scenario),
        "correlation_id": correlation_id
    })

    # Phase 4: Cascade failure simulation
    yield ctx.call_activity(announce_cascade_failure_test_started, input={
        "message": "Simulating cascade failure scenario",
        "details": {"test_type": "cascade_failure"},
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    cascade_result = yield ctx.call_activity(execute_cascade_failure_simulation, input={
        "scenario": scenario_to_dict(scenario),
        "correlation_id": correlation_id
    })

    # Phase 4.5: Advanced Workflow Failure Testing (if applicable)
    advanced_failure_result = None
    if scenario.failure_type in [FailureType.EXTERNAL_EVENT_STARVATION.value,
                                FailureType.CHILD_WORKFLOW_ZOMBIE.value,
                                FailureType.ACTIVITY_EXECUTION_LIMBO.value,
                                FailureType.DISTRIBUTED_TRANSACTION_FAILURE.value]:

        if scenario.failure_type == FailureType.EXTERNAL_EVENT_STARVATION.value:
            yield ctx.call_activity(announce_external_event_starvation_started, input={
                "message": f"Simulating external event starvation for {scenario.target_service}",
                "details": {
                    "failure_type": scenario.failure_type,
                    "target_service": scenario.target_service,
                    "expected_impact": "workflows_waiting_indefinitely_for_external_events"
                },
                "correlation_id": correlation_id,
                "workflow_id": ctx.instance_id
            })

            advanced_failure_result = yield ctx.call_activity(execute_external_event_starvation_test, input={
                "scenario": scenario_to_dict(scenario),
                "correlation_id": correlation_id
            })

        elif scenario.failure_type == FailureType.CHILD_WORKFLOW_ZOMBIE.value:
            yield ctx.call_activity(announce_child_workflow_zombie_detected, input={
                "message": f"Creating zombie child workflows in {scenario.target_service}",
                "details": {
                    "failure_type": scenario.failure_type,
                    "target_service": scenario.target_service,
                    "expected_impact": "parent_workflows_stuck_waiting_for_zombie_children"
                },
                "correlation_id": correlation_id,
                "workflow_id": ctx.instance_id
            })

            advanced_failure_result = yield ctx.call_activity(execute_child_workflow_zombie_test, input={
                "scenario": scenario_to_dict(scenario),
                "correlation_id": correlation_id
            })

        elif scenario.failure_type == FailureType.ACTIVITY_EXECUTION_LIMBO.value:
            yield ctx.call_activity(announce_activity_execution_limbo_started, input={
                "message": f"Simulating hanging activities in {scenario.target_service}",
                "details": {
                    "failure_type": scenario.failure_type,
                    "target_service": scenario.target_service,
                    "expected_impact": "activities_consume_resources_without_completion"
                },
                "correlation_id": correlation_id,
                "workflow_id": ctx.instance_id
            })

            advanced_failure_result = yield ctx.call_activity(execute_activity_execution_limbo_test, input={
                "scenario": scenario_to_dict(scenario),
                "correlation_id": correlation_id
            })

        elif scenario.failure_type == FailureType.DISTRIBUTED_TRANSACTION_FAILURE.value:
            yield ctx.call_activity(announce_distributed_transaction_failure_started, input={
                "message": f"Simulating distributed transaction compensation failures in {scenario.target_service}",
                "details": {
                    "failure_type": scenario.failure_type,
                    "target_service": scenario.target_service,
                    "expected_impact": "partial_rollback_state_with_data_inconsistencies"
                },
                "correlation_id": correlation_id,
                "workflow_id": ctx.instance_id
            })

            advanced_failure_result = yield ctx.call_activity(execute_distributed_transaction_failure_test, input={
                "scenario": scenario_to_dict(scenario),
                "correlation_id": correlation_id
            })

    # Phase 5: Recovery simulation
    yield ctx.call_activity(announce_recovery_test_started, input={
        "message": "Starting system recovery simulation",
        "details": {"test_type": "recovery"},
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    # Deactivate failure scenario
    yield ctx.call_activity(deactivate_chaos_failure_scenario, input=scenario.id)

    # Test recovery
    recovery_result = yield ctx.call_activity(execute_system_recovery_test, input={
        "scenario": scenario_to_dict(scenario),
        "correlation_id": correlation_id
    })

    # Phase 6: Final system check
    final_health_check = yield ctx.call_activity(perform_final_system_health_check, input=scenario)

    yield ctx.call_activity(announce_chaos_workflow_completed, input={
        "message": f"Chaos resilience workflow completed for scenario: {scenario.name}",
        "details": {
            "total_resilience_tests": len(resilience_results),
            "circuit_breaker_triggered": circuit_breaker_result.get("triggered", False),
            "cascade_failure_contained": cascade_result.get("contained", False),
            "recovery_successful": recovery_result.get("successful", False),
            "pre_failure_health": health_check,
            "post_failure_health": final_health_check
        },
        "correlation_id": correlation_id,
        "workflow_id": ctx.instance_id
    })

    return {
        "scenario_id": scenario.id,
        "correlation_id": correlation_id,
        "resilience_tests": resilience_results,
        "circuit_breaker_result": circuit_breaker_result,
        "cascade_result": cascade_result,
        "recovery_result": recovery_result,
        "health_checks": {
            "pre_failure": health_check,
            "post_failure": final_health_check
        },
        "advanced_failure_result": advanced_failure_result
    }

# Activity Functions - Stage-Specific Notification Activities
def announce_chaos_workflow_started(_, event_data: Dict[str, Any]):
    """Activity to announce chaos workflow has started"""
    logging.info(f"[CHAOS START] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="workflow_started",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_baseline_health_check_started(_, event_data: Dict[str, Any]):
    """Activity to announce baseline health check has started"""
    logging.info(f"[BASELINE CHECK] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="baseline_health_check",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_failure_injection_started(_, event_data: Dict[str, Any]):
    """Activity to announce failure injection has started"""
    logging.info(f"[FAILURE INJECT] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.WARNING.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="failure_injection",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_resilience_test_round_started(_, event_data: Dict[str, Any]):
    """Activity to announce resilience test round has started"""
    logging.info(f"[RESILIENCE ROUND] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="resilience_test_round",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_retry_test_delay(_, event_data: Dict[str, Any]):
    """Activity to announce delay between retry tests"""
    logging.info(f"[RETRY DELAY] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="retry_test_delay",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_circuit_breaker_test_started(_, event_data: Dict[str, Any]):
    """Activity to announce circuit breaker test has started"""
    logging.info(f"[CIRCUIT BREAKER] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.WARNING.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="circuit_breaker_test",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_cascade_failure_test_started(_, event_data: Dict[str, Any]):
    """Activity to announce cascade failure test has started"""
    logging.info(f"[CASCADE FAILURE] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.ERROR.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="cascade_failure_test",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_recovery_test_started(_, event_data: Dict[str, Any]):
    """Activity to announce recovery test has started"""
    logging.info(f"[RECOVERY TEST] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="recovery_test",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_chaos_workflow_completed(_, event_data: Dict[str, Any]):
    """Activity to announce chaos workflow has completed"""
    logging.info(f"[CHAOS COMPLETE] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.INFO.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="workflow_completed",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

# Advanced Workflow Failure Announcement Activities
def announce_external_event_starvation_started(_, event_data: Dict[str, Any]):
    """Activity to announce external event starvation scenario has started"""
    logging.info(f"[EVENT STARVATION] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.ERROR.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="external_event_starvation",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_child_workflow_zombie_detected(_, event_data: Dict[str, Any]):
    """Activity to announce child workflow zombie state detected"""
    logging.info(f"[ZOMBIE WORKFLOW] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.CRITICAL.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="child_workflow_zombie",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_activity_execution_limbo_started(_, event_data: Dict[str, Any]):
    """Activity to announce activity execution limbo scenario started"""
    logging.info(f"[ACTIVITY LIMBO] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.ERROR.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="activity_execution_limbo",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

def announce_distributed_transaction_failure_started(_, event_data: Dict[str, Any]):
    """Activity to announce distributed transaction failure scenario started"""
    logging.info(f"[TRANSACTION FAILURE] {event_data['message']}")

    event = DiagnosticEvent(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        severity=EventSeverity.CRITICAL.value,
        service="chaos-engineer",
        workflow_id=event_data.get("workflow_id", "unknown"),
        event_type="distributed_transaction_failure",
        message=event_data.get("message", ""),
        details=event_data.get("details", {}),
        correlation_id=event_data.get("correlation_id", "unknown"),
        retry_count=0,
        execution_time_ms=0
    )

    diagnostic_events.append(event)

    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": event.workflow_id,
            "message": f"[CHAOS] {event.message}",
            "severity": event.severity,
            "event_type": event.event_type,
            "details": event.details,
            "correlation_id": event.correlation_id,
            "data-content-type": "application/json"
        }))

    return event

# Business Logic Activities (Renamed for Clarity)
def perform_baseline_system_health_check(_, scenario: ChaosScenario) -> Dict[str, Any]:
    """Activity to check system health before failure injection"""
    if isinstance(scenario, dict):
        scenario = ChaosScenario(**scenario)

    logging.info(f"Performing baseline health check for scenario: {scenario.name}")

    # Simulate health checks for various services
    services = ["inventory", "payments", "shipping", "order-processor", "notifications"]
    health_status = {}

    for service in services:
        # Simulate health check with some variance
        base_health = 95.0
        if service == scenario.target_service and scenario.id in active_failures:
            base_health = 60.0  # Degraded health when failure is active

        health_score = base_health + random.uniform(-5, 5)
        health_score = max(0, min(100, health_score))

        health_status[service] = {
            "health_score": round(health_score, 2),
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "unhealthy",
            "response_time_ms": random.randint(50, 300),
            "error_rate": random.uniform(0, 0.05) if health_score > 80 else random.uniform(0.1, 0.3)
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "overall_health": round(sum(s["health_score"] for s in health_status.values()) / len(health_status), 2),
        "services": health_status
    }

def perform_final_system_health_check(_, scenario: ChaosScenario) -> Dict[str, Any]:
    """Activity to check system health after failure testing"""
    if isinstance(scenario, dict):
        scenario = ChaosScenario(**scenario)

    logging.info(f"Performing final health check for scenario: {scenario.name}")

    # Simulate health checks for various services
    services = ["inventory", "payments", "shipping", "order-processor", "notifications"]
    health_status = {}

    for service in services:
        # Simulate health check with some variance - should be healthier after recovery
        base_health = 90.0
        if service == scenario.target_service and scenario.id in active_failures:
            base_health = 60.0  # Still degraded if failure is active
        else:
            base_health = 92.0  # Slightly better after recovery

        health_score = base_health + random.uniform(-5, 5)
        health_score = max(0, min(100, health_score))

        health_status[service] = {
            "health_score": round(health_score, 2),
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "unhealthy",
            "response_time_ms": random.randint(50, 300),
            "error_rate": random.uniform(0, 0.05) if health_score > 80 else random.uniform(0.1, 0.3)
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "overall_health": round(sum(s["health_score"] for s in health_status.values()) / len(health_status), 2),
        "services": health_status
    }

def activate_chaos_failure_scenario(_, scenario: ChaosScenario):
    """Activity to activate a chaos failure scenario"""
    if isinstance(scenario, dict):
        scenario = ChaosScenario(**scenario)

    logging.info(f"Activating chaos failure scenario: {scenario.name}")
    active_failures[scenario.id] = datetime.now() + timedelta(seconds=scenario.duration_seconds)

    return {"activated": True, "expires_at": active_failures[scenario.id].isoformat()}

def deactivate_chaos_failure_scenario(_, scenario_id: str):
    """Activity to deactivate a chaos failure scenario"""
    logging.info(f"Deactivating chaos failure scenario: {scenario_id}")
    if scenario_id in active_failures:
        del active_failures[scenario_id]

    return {"deactivated": True}

def execute_retry_policy_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute retry policy testing with specific retry strategy"""
    scenario = ChaosScenario(**test_data["scenario"])
    retry_policy = test_data["retry_policy"]
    correlation_id = test_data["correlation_id"]
    test_round = test_data["test_round"]

    logging.info(f"Executing retry policy test: {retry_policy}")

    retry_attempts = []
    max_retries = 3
    base_delay_ms = 100

    for attempt in range(max_retries + 1):
        start_time = time.time()

        # Simulate service call with potential failure
        success = simulate_service_call(scenario, attempt)

        execution_time = int((time.time() - start_time) * 1000)

        if success:
            return {
                "test_id": f"{correlation_id}_retry_test_{test_round}_{retry_policy}",
                "retry_policy": retry_policy,
                "success": True,
                "total_attempts": attempt + 1,
                "total_execution_time_ms": sum(r.delay_ms for r in retry_attempts) + execution_time,
                "retry_attempts": [asdict(r) for r in retry_attempts]
            }

        # Calculate delay based on retry policy
        if attempt < max_retries:
            if retry_policy == RetryPolicy.EXPONENTIAL_BACKOFF.value:
                delay_ms = base_delay_ms * (2 ** attempt)
            elif retry_policy == RetryPolicy.LINEAR_BACKOFF.value:
                delay_ms = base_delay_ms * (attempt + 1)
            else:  # FIXED_INTERVAL
                delay_ms = base_delay_ms

            retry_attempts.append(RetryAttempt(
                attempt=attempt + 1,
                timestamp=datetime.now().isoformat(),
                delay_ms=delay_ms,
                error_message=f"Service call failed: {scenario.failure_type}",
                will_retry=True
            ))

            # Simulate delay
            time.sleep(delay_ms / 1000.0)
        else:
            retry_attempts.append(RetryAttempt(
                attempt=attempt + 1,
                timestamp=datetime.now().isoformat(),
                delay_ms=0,
                error_message=f"Service call failed: {scenario.failure_type}",
                will_retry=False
            ))

    return {
        "test_id": f"{correlation_id}_retry_test_{test_round}_{retry_policy}",
        "retry_policy": retry_policy,
        "success": False,
        "total_attempts": max_retries + 1,
        "total_execution_time_ms": sum(r.delay_ms for r in retry_attempts),
        "retry_attempts": [asdict(r) for r in retry_attempts],
        "final_error": f"Max retries exceeded for {scenario.failure_type}"
    }

def execute_circuit_breaker_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute circuit breaker pattern testing"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing circuit breaker pattern tests")

    # Simulate circuit breaker states
    failure_threshold = 5
    failure_count = 0
    circuit_open = False

    test_results = []

    # Test 10 requests to trigger circuit breaker
    for i in range(10):
        if circuit_open:
            # Circuit is open, fail fast
            test_results.append({
                "request": i + 1,
                "result": "failed_fast",
                "reason": "circuit_breaker_open",
                "response_time_ms": 1
            })
        else:
            success = simulate_service_call(scenario, i)

            if not success:
                failure_count += 1
                if failure_count >= failure_threshold:
                    circuit_open = True

                test_results.append({
                    "request": i + 1,
                    "result": "failed",
                    "reason": scenario.failure_type,
                    "response_time_ms": random.randint(100, 1000),
                    "failure_count": failure_count
                })
            else:
                test_results.append({
                    "request": i + 1,
                    "result": "success",
                    "response_time_ms": random.randint(50, 200)
                })

        time.sleep(0.1)  # Small delay between requests

    return {
        "circuit_breaker_triggered": circuit_open,
        "failure_threshold": failure_threshold,
        "total_failures": failure_count,
        "test_results": test_results
    }

def execute_cascade_failure_simulation(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute cascade failure simulation"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing cascade failure simulation")

    # Simulate how failure in one service affects others
    services = ["inventory", "payments", "shipping", "order-processor"]
    failure_cascade = []

    # Start with the target service
    affected_services = [scenario.target_service]
    cascade_step = 1

    while len(affected_services) < len(services) and cascade_step <= 3:
        # Determine which additional services get affected
        for service in services:
            if service not in affected_services and random.random() < 0.4:  # 40% chance of cascade
                affected_services.append(service)
                failure_cascade.append({
                    "step": cascade_step,
                    "service": service,
                    "reason": f"dependency_on_{affected_services[-2] if len(affected_services) > 1 else scenario.target_service}",
                    "timestamp": datetime.now().isoformat()
                })

        cascade_step += 1
        time.sleep(0.5)  # Simulate time for cascade to spread

    # Determine if cascade was contained
    contained = len(affected_services) < len(services)

    return {
        "cascade_contained": contained,
        "affected_services": affected_services,
        "cascade_steps": failure_cascade,
        "total_affected": len(affected_services),
        "total_services": len(services)
    }

def execute_system_recovery_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute system recovery testing"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing system recovery tests")

    # Simulate recovery steps
    recovery_steps = [
        "service_restart",
        "health_check_pass",
        "traffic_restoration",
        "performance_validation"
    ]

    recovery_results = []

    for step in recovery_steps:
        success = random.random() > 0.1  # 90% success rate for recovery steps

        recovery_results.append({
            "step": step,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": random.randint(500, 2000)
        })

        if not success:
            break

        time.sleep(0.2)  # Simulate time for each recovery step

    all_successful = all(r["success"] for r in recovery_results)

    return {
        "recovery_successful": all_successful,
        "recovery_steps": recovery_results,
        "total_recovery_time_ms": sum(r["duration_ms"] for r in recovery_results)
    }

# Advanced Workflow Failure Execution Activities
def execute_external_event_starvation_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute external event starvation testing"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing external event starvation simulation")

    # Simulate workflows waiting for events that never arrive
    starved_workflows = []
    event_sources = ["approval_system", "payment_gateway", "shipping_provider", "external_api"]

    for i in range(3):  # Simulate 3 workflows waiting for events
        workflow_id = f"starved_workflow_{correlation_id}_{i}"
        event_source = random.choice(event_sources)
        expected_event = f"{event_source}_response"

        timeout_minutes = random.randint(5, 30)
        timeout_at = (datetime.now() + timedelta(minutes=timeout_minutes)).isoformat()

        # Record the missed event
        missed_event = MissedEventInfo(
            workflow_id=workflow_id,
            event_name=expected_event,
            expected_at=datetime.now().isoformat(),
            timeout_at=timeout_at,
            event_source=event_source
        )

        missed_events[f"{workflow_id}_{expected_event}"] = missed_event

        starved_workflows.append({
            "workflow_id": workflow_id,
            "expected_event": expected_event,
            "event_source": event_source,
            "waiting_time_minutes": timeout_minutes,
            "timeout_at": timeout_at,
            "recovery_action_needed": "manual_event_injection_or_timeout_handling"
        })

        time.sleep(0.2)  # Brief delay between simulations

    # Track workflow failure state
    failure_state = WorkflowFailureState(
        workflow_id=correlation_id,
        failure_type="external_event_starvation",
        target_service=scenario.target_service,
        started_at=datetime.now().isoformat(),
        expected_recovery_time=(datetime.now() + timedelta(minutes=30)).isoformat(),
        missed_events=[w["expected_event"] for w in starved_workflows]
    )

    workflow_failure_states[correlation_id] = failure_state

    return {
        "starvation_triggered": True,
        "starved_workflows": starved_workflows,
        "affected_event_sources": list(set(w["event_source"] for w in starved_workflows)),
        "total_starved_workflows": len(starved_workflows),
        "recovery_methods": [
            "manual_event_injection",
            "timeout_extension",
            "workflow_cancellation",
            "fallback_processing"
        ]
    }

def execute_child_workflow_zombie_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute child workflow zombie state simulation"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing child workflow zombie simulation")

    # Simulate parent workflow with zombie children
    parent_workflow_id = f"parent_workflow_{correlation_id}"
    zombie_children = []

    hang_reasons = [
        "infinite_loop_in_activity",
        "deadlock_on_external_resource",
        "network_partition_with_service",
        "memory_leak_causing_freeze",
        "blocked_on_unavailable_dependency"
    ]

    stuck_activities = [
        "process_payment_activity",
        "validate_inventory_activity",
        "submit_shipping_request",
        "external_api_call_activity",
        "database_transaction_activity"
    ]

    for i in range(4):  # Create 4 zombie child workflows
        child_workflow_id = f"zombie_child_{correlation_id}_{i}"
        hang_reason = random.choice(hang_reasons)
        stuck_activity = random.choice(stuck_activities)
        time_stuck = random.randint(300, 3600)  # 5 minutes to 1 hour stuck

        zombie_info = ZombieWorkflowInfo(
            child_workflow_id=child_workflow_id,
            parent_workflow_id=parent_workflow_id,
            stuck_activity=stuck_activity,
            time_stuck_seconds=time_stuck,
            simulated_hang_reason=hang_reason
        )

        zombie_workflows[child_workflow_id] = zombie_info

        zombie_children.append({
            "child_workflow_id": child_workflow_id,
            "stuck_activity": stuck_activity,
            "hang_reason": hang_reason,
            "time_stuck_seconds": time_stuck,
            "requires_manual_intervention": True
        })

        time.sleep(0.1)

    # Track workflow failure state
    failure_state = WorkflowFailureState(
        workflow_id=parent_workflow_id,
        failure_type="child_workflow_zombie",
        target_service=scenario.target_service,
        started_at=datetime.now().isoformat(),
        zombie_child_ids=[z["child_workflow_id"] for z in zombie_children]
    )

    workflow_failure_states[parent_workflow_id] = failure_state

    return {
        "zombie_state_created": True,
        "parent_workflow_id": parent_workflow_id,
        "zombie_children": zombie_children,
        "total_zombie_children": len(zombie_children),
        "recovery_methods": [
            "terminate_zombie_children",
            "restart_parent_workflow",
            "manual_cleanup_and_compensation",
            "force_child_workflow_completion"
        ]
    }

def execute_activity_execution_limbo_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute activity execution limbo simulation"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing activity execution limbo simulation")

    # Simulate activities that hang indefinitely
    hanging_activities_list = []
    service_activities = {
        "payments": ["process_credit_card", "validate_payment_method", "submit_payment_batch"],
        "inventory": ["reserve_items", "update_stock_levels", "check_availability"],
        "shipping": ["calculate_shipping_cost", "schedule_pickup", "track_package"],
        "order-processor": ["validate_order", "apply_discounts", "generate_invoice"]
    }

    target_service = scenario.target_service
    activities = service_activities.get(target_service, ["generic_activity"])

    for activity in activities:
        hang_duration = random.randint(600, 7200)  # 10 minutes to 2 hours
        resource_consumed = random.choice(["memory", "cpu", "network_connection", "database_connection"])

        hanging_activity = {
            "activity_name": activity,
            "service": target_service,
            "hang_duration_seconds": hang_duration,
            "resource_consumed": resource_consumed,
            "hang_reason": f"blocking_on_{resource_consumed}",
            "workflow_impact": "workflow_suspended_indefinitely",
            "requires_manual_intervention": True
        }

        hanging_activities_list.append(hanging_activity)

    # Track hanging activities by service
    if target_service not in hanging_activities:
        hanging_activities[target_service] = []
    hanging_activities[target_service].extend([h["activity_name"] for h in hanging_activities_list])

    # Track workflow failure state
    failure_state = WorkflowFailureState(
        workflow_id=correlation_id,
        failure_type="activity_execution_limbo",
        target_service=target_service,
        started_at=datetime.now().isoformat(),
        blocked_activities=[h["activity_name"] for h in hanging_activities_list]
    )

    workflow_failure_states[correlation_id] = failure_state

    return {
        "limbo_state_created": True,
        "target_service": target_service,
        "hanging_activities": hanging_activities_list,
        "total_hanging_activities": len(hanging_activities_list),
        "system_impact": "resource_exhaustion_and_workflow_suspension",
        "recovery_methods": [
            "kill_hanging_processes",
            "restart_service_instance",
            "implement_activity_timeouts",
            "add_circuit_breaker_protection"
        ]
    }

def execute_distributed_transaction_failure_test(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Activity to execute distributed transaction failure simulation"""
    scenario = ChaosScenario(**test_data["scenario"])
    correlation_id = test_data["correlation_id"]

    logging.info("Executing distributed transaction failure simulation")

    # Simulate saga pattern failure during compensation
    transaction_steps = [
        {"service": "inventory", "action": "reserve_items", "status": "completed"},
        {"service": "payments", "action": "charge_customer", "status": "completed"},
        {"service": "shipping", "action": "create_shipment", "status": "failed"},
    ]

    # Simulate compensation failures
    compensation_failures = []
    compensation_steps = [
        {"service": "payments", "compensation": "refund_customer", "expected": True},
        {"service": "inventory", "compensation": "release_reservation", "expected": True},
    ]

    for step in compensation_steps:
        # Simulate compensation failure
        compensation_failed = random.random() < 0.4  # 40% chance of compensation failure

        if compensation_failed:
            failure_reason = random.choice([
                "payment_gateway_unavailable",
                "inventory_service_timeout",
                "network_partition_during_rollback",
                "compensation_activity_deadlock"
            ])

            compensation_failures.append({
                "service": step["service"],
                "compensation_action": step["compensation"],
                "failure_reason": failure_reason,
                "data_consistency_impact": "partial_rollback_state",
                "manual_intervention_required": True
            })

    # Track workflow failure state
    failure_state = WorkflowFailureState(
        workflow_id=correlation_id,
        failure_type="distributed_transaction_failure",
        target_service=scenario.target_service,
        started_at=datetime.now().isoformat(),
        expected_recovery_time=(datetime.now() + timedelta(hours=2)).isoformat()
    )

    workflow_failure_states[correlation_id] = failure_state

    return {
        "transaction_failure_simulated": True,
        "original_transaction_steps": transaction_steps,
        "compensation_failures": compensation_failures,
        "data_consistency_state": "partial_rollback_with_inconsistencies",
        "affected_services": list(set([f["service"] for f in compensation_failures])),
        "recovery_methods": [
            "manual_compensation_retry",
            "data_reconciliation_process",
            "rollback_to_known_good_state",
            "implement_idempotent_compensation"
        ]
    }

# Legacy function kept for compatibility (rename only)
def emit_diagnostic_event(_, event_data: Dict[str, Any]):
    """Legacy activity - use specific announcement activities instead"""
    return announce_chaos_workflow_started(_, event_data)

def perform_system_health_check(_, scenario: ChaosScenario) -> Dict[str, Any]:
    """Legacy activity - redirects to baseline health check"""
    return perform_baseline_system_health_check(_, scenario)

def activate_failure_scenario(_, scenario: ChaosScenario):
    """Legacy activity - redirects to chaos failure scenario"""
    return activate_chaos_failure_scenario(_, scenario)

def deactivate_failure_scenario(_, scenario_id: str):
    """Legacy activity - redirects to chaos failure scenario"""
    return deactivate_chaos_failure_scenario(_, scenario_id)

def test_service_with_retries(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy activity - redirects to retry policy test"""
    return execute_retry_policy_test(_, test_data)

def test_circuit_breaker(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy activity - redirects to circuit breaker test"""
    return execute_circuit_breaker_test(_, test_data)

def simulate_cascade_failure(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy activity - redirects to cascade failure simulation"""
    return execute_cascade_failure_simulation(_, test_data)

def test_system_recovery(_, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy activity - redirects to system recovery test"""
    return execute_system_recovery_test(_, test_data)

def simulate_service_call(scenario, attempt: int) -> bool:
    """Simulate a service call that may fail based on the chaos scenario"""
    # Convert to dataclass if it's a dict (due to Dapr serialization)
    if isinstance(scenario, dict):
        scenario = ChaosScenario(**scenario)

    if scenario.id not in active_failures:
        return True  # No active failure, success

    # Check if failure scenario is still active
    if datetime.now() > active_failures[scenario.id]:
        del active_failures[scenario.id]
        return True

    # Apply failure rate with some variance based on attempt number
    failure_probability = scenario.failure_rate

    # Slightly reduce failure rate with each retry attempt (simulating transient issues)
    if attempt > 0:
        failure_probability = max(0.1, failure_probability - (attempt * 0.1))

    return random.random() > failure_probability

# API Endpoints
@app.route("/chaos/scenarios", methods=["POST"])
def create_chaos_scenario():
    """Create a new chaos engineering scenario"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request. Expected JSON body"}), 400

    required_fields = ["name", "description", "failure_type", "target_service"]
    for field in required_fields:
        if not request_data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    scenario_id = f"chaos_{request_data['name'].lower().replace(' ', '_')}_{random.randint(1000, 9999)}"

    scenario = ChaosScenario(
        id=scenario_id,
        name=request_data["name"],
        description=request_data["description"],
        failure_type=request_data["failure_type"],
        target_service=request_data["target_service"],
        failure_rate=request_data.get("failure_rate", 0.5),
        duration_seconds=request_data.get("duration_seconds", 60),
        enabled=request_data.get("enabled", True),
        created_at=datetime.now().isoformat()
    )

    chaos_scenarios[scenario_id] = scenario

    return jsonify(asdict(scenario)), 201

@app.route("/chaos/scenarios/<scenario_id>/execute", methods=["POST"])
def execute_chaos_scenario(scenario_id):
    """Execute a chaos engineering scenario"""
    if scenario_id not in chaos_scenarios:
        return jsonify({"error": f"Scenario not found: {escape(scenario_id)}"}), 404

    scenario = chaos_scenarios[scenario_id]

    if not scenario.enabled:
        return jsonify({"error": "Scenario is disabled"}), 400

    try:
        wf_client = wf.DaprWorkflowClient()
        instance_id = wf_client.schedule_new_workflow(
            chaos_resilience_workflow,
            input=scenario,
            instance_id=f"{scenario_id}_{int(datetime.now().timestamp())}"
        )

        logging.info(f"Started chaos scenario workflow: {instance_id}")

        return jsonify({
            "instance_id": instance_id,
            "scenario_id": scenario_id,
            "scenario_name": scenario.name,
            "status": "started"
        }), 202

    except Exception as e:
        logging.error(f"Error executing chaos scenario: {str(e)}")
        return jsonify({"error": f"Failed to execute scenario: {str(e)}"}), 500

@app.route("/chaos/scenarios", methods=["GET"])
def list_chaos_scenarios():
    """List all chaos engineering scenarios"""
    return jsonify([asdict(scenario) for scenario in chaos_scenarios.values()]), 200

@app.route("/chaos/scenarios/<scenario_id>", methods=["GET"])
def get_chaos_scenario(scenario_id):
    """Get a specific chaos engineering scenario"""
    if scenario_id not in chaos_scenarios:
        return jsonify({"error": f"Scenario not found: {escape(scenario_id)}"}), 404

    return jsonify(asdict(chaos_scenarios[scenario_id])), 200

@app.route("/chaos/events", methods=["GET"])
def get_diagnostic_events():
    """Get diagnostic events for dashboard consumption"""
    # Support filtering by correlation_id, severity, time range
    correlation_id = request.args.get("correlation_id")
    severity = request.args.get("severity")
    limit = int(request.args.get("limit", 100))

    filtered_events = diagnostic_events

    if correlation_id:
        filtered_events = [e for e in filtered_events if e.correlation_id == correlation_id]

    if severity:
        filtered_events = [e for e in filtered_events if e.severity == severity]

    # Return most recent events first
    filtered_events = sorted(filtered_events, key=lambda x: x.timestamp, reverse=True)[:limit]

    return jsonify([asdict(event) for event in filtered_events]), 200

@app.route("/chaos/inject/<failure_type>/<target_service>", methods=["POST"])
def inject_failure(failure_type, target_service):
    """Quick failure injection for testing"""
    request_data = request.get_json() or {}

    scenario_id = f"quick_inject_{failure_type}_{target_service}_{int(datetime.now().timestamp())}"

    scenario = ChaosScenario(
        id=scenario_id,
        name=f"Quick {failure_type} injection",
        description=f"Quick failure injection: {failure_type} in {target_service}",
        failure_type=failure_type,
        target_service=target_service,
        failure_rate=request_data.get("failure_rate", 0.8),
        duration_seconds=request_data.get("duration_seconds", 30),
        enabled=True,
        created_at=datetime.now().isoformat()
    )

    # Activate immediately
    active_failures[scenario_id] = datetime.now() + timedelta(seconds=scenario.duration_seconds)

    # Emit diagnostic event
    emit_diagnostic_event(None, {
        "severity": EventSeverity.WARNING.value,
        "event_type": "quick_failure_injection",
        "message": f"Quick failure injection: {failure_type} in {target_service}",
        "details": asdict(scenario),
        "correlation_id": scenario_id,
        "workflow_id": "manual_injection"
    })

    return jsonify({
        "scenario_id": scenario_id,
        "status": "injected",
        "expires_at": active_failures[scenario_id].isoformat()
    }), 201

@app.route("/chaos/status", methods=["GET"])
def get_chaos_status():
    """Get current chaos engineering status"""
    active_scenario_count = len(active_failures)
    total_scenarios = len(chaos_scenarios)
    recent_events = len([e for e in diagnostic_events if datetime.fromisoformat(e.timestamp) > datetime.now() - timedelta(hours=1)])

    return jsonify({
        "chaos_enabled": ENABLE_CHAOS,
        "active_failures": active_scenario_count,
        "total_scenarios": total_scenarios,
        "recent_events_1h": recent_events,
        "failure_rate": FAILURE_RATE,
        "active_scenarios": [
            {
                "scenario_id": sid,
                "expires_at": exp_time.isoformat()
            } for sid, exp_time in active_failures.items()
        ]
    }), 200

@app.route("/health", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({
        "service": "chaos-engineer",
        "status": "healthy",
        "version": "1.0.0",
        "chaos_enabled": ENABLE_CHAOS,
        "active_failures": len(active_failures)
    })

@app.route("/chaos/advanced-failures", methods=["GET"])
def get_advanced_failure_states():
    """Get all advanced workflow failure states"""
    failure_type = request.args.get("type")

    filtered_states = workflow_failure_states
    if failure_type:
        filtered_states = {k: v for k, v in workflow_failure_states.items() if v.failure_type == failure_type}

    return jsonify({
        "workflow_failure_states": [asdict(state) for state in filtered_states.values()],
        "total_failures": len(filtered_states),
        "failure_types": list(set(s.failure_type for s in workflow_failure_states.values()))
    }), 200

@app.route("/chaos/zombie-workflows", methods=["GET"])
def get_zombie_workflows():
    """Get all zombie workflow information"""
    return jsonify({
        "zombie_workflows": [asdict(zombie) for zombie in zombie_workflows.values()],
        "total_zombies": len(zombie_workflows),
        "recovery_needed": len(zombie_workflows) > 0
    }), 200

@app.route("/chaos/missed-events", methods=["GET"])
def get_missed_events():
    """Get all missed external events"""
    event_source = request.args.get("source")

    filtered_events = missed_events
    if event_source:
        filtered_events = {k: v for k, v in missed_events.items() if v.event_source == event_source}

    return jsonify({
        "missed_events": [asdict(event) for event in filtered_events.values()],
        "total_missed": len(filtered_events),
        "event_sources": list(set(e.event_source for e in missed_events.values()))
    }), 200

@app.route("/chaos/hanging-activities", methods=["GET"])
def get_hanging_activities():
    """Get all hanging activities by service"""
    return jsonify({
        "hanging_activities": hanging_activities,
        "total_services_affected": len(hanging_activities),
        "total_hanging_activities": sum(len(activities) for activities in hanging_activities.values())
    }), 200

@app.route("/chaos/advanced-failures/<workflow_id>/recover", methods=["POST"])
def recover_advanced_failure(workflow_id):
    """Simulate recovery actions for advanced workflow failures"""
    if workflow_id not in workflow_failure_states:
        return jsonify({"error": f"Workflow failure state not found: {escape(workflow_id)}"}), 404

    failure_state = workflow_failure_states[workflow_id]
    recovery_actions = []

    if failure_state.failure_type == "external_event_starvation":
        # Simulate manual event injection
        for event_name in failure_state.missed_events or []:
            recovery_actions.append({
                "action": "manual_event_injection",
                "event": event_name,
                "status": "simulated_recovery"
            })

    elif failure_state.failure_type == "child_workflow_zombie":
        # Simulate zombie cleanup
        for child_id in failure_state.zombie_child_ids or []:
            if child_id in zombie_workflows:
                recovery_actions.append({
                    "action": "terminate_zombie_child",
                    "child_workflow_id": child_id,
                    "status": "simulated_termination"
                })
                del zombie_workflows[child_id]

    elif failure_state.failure_type == "activity_execution_limbo":
        # Simulate activity timeout/kill
        for activity in failure_state.blocked_activities or []:
            recovery_actions.append({
                "action": "kill_hanging_activity",
                "activity": activity,
                "status": "simulated_termination"
            })

    # Remove the failure state after recovery
    del workflow_failure_states[workflow_id]

    return jsonify({
        "workflow_id": workflow_id,
        "recovery_actions": recovery_actions,
        "status": "recovery_simulated"
    }), 200

def main():
    logging.info("Starting Chaos Engineering Service...")

    if ENABLE_CHAOS:
        logging.info(f"⚡ CHAOS MODE ENABLED: Failure rate {FAILURE_RATE * 100}%")
    else:
        logging.info("Chaos mode disabled - running in safe mode")

    # Start the workflow runtime with auto-reconnection
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )
    wf_runtime.register_workflow(chaos_resilience_workflow)

    # Register stage-specific notification activities
    wf_runtime.register_activity(announce_chaos_workflow_started)
    wf_runtime.register_activity(announce_baseline_health_check_started)
    wf_runtime.register_activity(announce_failure_injection_started)
    wf_runtime.register_activity(announce_resilience_test_round_started)
    wf_runtime.register_activity(announce_retry_test_delay)
    wf_runtime.register_activity(announce_circuit_breaker_test_started)
    wf_runtime.register_activity(announce_cascade_failure_test_started)
    wf_runtime.register_activity(announce_recovery_test_started)
    wf_runtime.register_activity(announce_chaos_workflow_completed)

    # Register advanced workflow failure notification activities
    wf_runtime.register_activity(announce_external_event_starvation_started)
    wf_runtime.register_activity(announce_child_workflow_zombie_detected)
    wf_runtime.register_activity(announce_activity_execution_limbo_started)
    wf_runtime.register_activity(announce_distributed_transaction_failure_started)

    # Register business logic activities
    wf_runtime.register_activity(perform_baseline_system_health_check)
    wf_runtime.register_activity(perform_final_system_health_check)
    wf_runtime.register_activity(activate_chaos_failure_scenario)
    wf_runtime.register_activity(deactivate_chaos_failure_scenario)
    wf_runtime.register_activity(execute_retry_policy_test)
    wf_runtime.register_activity(execute_circuit_breaker_test)
    wf_runtime.register_activity(execute_cascade_failure_simulation)
    wf_runtime.register_activity(execute_system_recovery_test)

    # Register advanced workflow failure execution activities
    wf_runtime.register_activity(execute_external_event_starvation_test)
    wf_runtime.register_activity(execute_child_workflow_zombie_test)
    wf_runtime.register_activity(execute_activity_execution_limbo_test)
    wf_runtime.register_activity(execute_distributed_transaction_failure_test)

    wf_runtime.start()  # non-blocking with auto-reconnect

    # Start the Flask app server
    app.run(host='0.0.0.0', port=APP_PORT, debug=False, use_reloader=False)

    # Stop the workflow runtime to allow the process to terminate
    wf_runtime.shutdown()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    main()
