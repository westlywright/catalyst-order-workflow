"""
Agent Worker Service - Levels 2-4 Workflow Engine

Demonstrates:
- SupervisorWorkflow (Level 2) with parallel child spawning
- SpecialistWorkflow (Level 3) with role-based processing
- AtomicTaskWorkflow (Level 4) with timers and validation
- when_all for parallel execution
- Multi-level nested sub-workflows
"""

import json
import logging
import os
import sys
import time

# Add parent directory to path for common imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import dapr.ext.workflow as wf
from dapr.clients import DaprClient
from flask import Flask, jsonify
from datetime import timedelta

from common.agent_models import dict_to_task_definition
from common.resilient_workflow_runtime import ResilientWorkflowRuntime
from models import (
    SupervisorResult, SpecialistInput, SpecialistResult,
    AtomicTaskInput, AtomicTaskResult,
    dict_to_specialist_input, dict_to_atomic_task_input,
    supervisor_result_to_dict, specialist_result_to_dict,
    atomic_task_result_to_dict, specialist_input_to_dict,
    atomic_task_input_to_dict
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

APP_PORT = os.getenv("APP_PORT", "3012")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def map_task_type_to_role(task_type: str) -> str:
    """Map task type to specialist role"""
    return {
        "research": "researcher",
        "analysis": "analyst",
        "synthesis": "synthesizer",
        "validation": "validator"
    }.get(task_type, "generalist")


# =============================================================================
# ACTIVITIES
# =============================================================================

def announce(ctx: wf.WorkflowActivityContext, message: str):
    """Publish notification to pub/sub for UI display"""
    logger.info(f"[ANNOUNCE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": message,
            "data-content-type": "application/json"
        }))


def execute_atomic_task(ctx: wf.WorkflowActivityContext, atomic_input) -> dict:
    """Execute an atomic task (simulated work)"""
    input_data = dict_to_atomic_task_input(atomic_input)

    logger.info(f"[EXECUTE] Executing atomic task: {input_data.action}")

    # Simulate work
    start_time = time.time()

    # Simulated task execution
    output = f"Completed action '{input_data.action}' with parameters: {input_data.parameters}"

    execution_time = int((time.time() - start_time) * 1000)

    result = AtomicTaskResult(
        task_id=input_data.task_id,
        action=input_data.action,
        success=True,
        output=output,
        execution_time_ms=execution_time
    )

    return atomic_task_result_to_dict(result)


def validate_atomic_result(ctx: wf.WorkflowActivityContext, result_input) -> dict:
    """Validate the result of an atomic task"""
    result = result_input if isinstance(result_input, dict) else atomic_task_result_to_dict(result_input)

    logger.info(f"[VALIDATE] Validating result for task: {result.get('task_id', 'unknown')}")

    # Simple validation: check if output is not empty
    is_valid = bool(result.get("output"))

    result["validated"] = is_valid
    return result


# =============================================================================
# LEVEL 4: ATOMIC TASK WORKFLOW
# =============================================================================

def atomic_task_workflow(ctx: wf.DaprWorkflowContext, atomic_input):
    """
    Level 4: Atomic Task Workflow

    The lowest level workflow that:
    1. Executes a single atomic task
    2. Applies configurable delay via timer
    3. Validates the result

    Demonstrates:
    - OrchestratorStarted/Completed
    - Timer usage for delay simulation
    - Activity chaining
    """
    input_data = dict_to_atomic_task_input(atomic_input)

    yield ctx.call_activity(announce, input=f"[L4-ATOMIC] Starting: {input_data.action}")

    # Failure injection at Level 4
    if input_data.fail_at_level == 4:
        yield ctx.call_activity(announce, input=f"[L4-ATOMIC] FAILURE INJECTED at Level 4")
        raise Exception(f"Simulated failure at Level 4 (Atomic: {input_data.action})")

    # Simulate work with configurable delay using timer
    if input_data.simulate_delay_ms > 0:
        yield ctx.call_activity(announce, input=f"[L4-ATOMIC] Processing... ({input_data.simulate_delay_ms}ms)")
        deadline = ctx.current_utc_datetime + timedelta(milliseconds=input_data.simulate_delay_ms)
        yield ctx.create_timer(deadline)

    # Execute the atomic task
    result_dict = yield ctx.call_activity(execute_atomic_task, input=atomic_input)

    # Validate result
    validated_result = yield ctx.call_activity(validate_atomic_result, input=result_dict)

    yield ctx.call_activity(announce, input=f"[L4-ATOMIC] Complete: {input_data.action}")

    return validated_result


# =============================================================================
# LEVEL 3: SPECIALIST WORKFLOW
# =============================================================================

def specialist_workflow(ctx: wf.DaprWorkflowContext, specialist_input):
    """
    Level 3: Specialist Workflow

    A role-based workflow that:
    1. Processes a task according to its specialty
    2. Spawns an atomic task workflow for execution
    3. Returns specialist results

    Demonstrates:
    - Role-based processing
    - call_child_workflow for nesting
    - OrchestratorStarted/Completed at this level
    """
    input_data = dict_to_specialist_input(specialist_input)
    task = dict_to_task_definition(input_data.task)

    yield ctx.call_activity(announce,
        input=f"[L3-SPECIALIST:{input_data.specialist_role.upper()}] Processing: {task.name}")

    # Failure injection at Level 3
    if input_data.fail_at_level == 3:
        yield ctx.call_activity(announce,
            input=f"[L3-SPECIALIST:{input_data.specialist_role.upper()}] FAILURE INJECTED at Level 3")
        raise Exception(f"Simulated failure at Level 3 (Specialist: {input_data.specialist_role})")

    # Prepare atomic task input
    atomic_input = AtomicTaskInput(
        task_id=task.id,
        action=f"execute_{input_data.specialist_role}",
        parameters={
            "task_type": task.task_type,
            "task_name": task.name,
            "description": task.description
        },
        simulate_delay_ms=task.estimated_duration_ms,
        fail_at_level=input_data.fail_at_level
    )

    # Spawn atomic task (Level 4)
    yield ctx.call_activity(announce,
        input=f"[L3-SPECIALIST:{input_data.specialist_role.upper()}] Delegating to atomic task...")

    try:
        atomic_result = yield ctx.call_child_workflow(
            atomic_task_workflow,
            input=atomic_task_input_to_dict(atomic_input),
            instance_id=f"{task.id}_child_atomic"
        )
    except Exception as e:
        yield ctx.call_activity(announce,
            input=f"[L3-SPECIALIST:{input_data.specialist_role.upper()}] Atomic task failed: {str(e)}")
        return specialist_result_to_dict(SpecialistResult(
            task_id=task.id,
            specialist_role=input_data.specialist_role,
            success=False,
            output=f"Atomic task failed: {str(e)}",
            execution_time_ms=0
        ))

    yield ctx.call_activity(announce,
        input=f"[L3-SPECIALIST:{input_data.specialist_role.upper()}] Complete: {task.name}")

    # Extract execution time from atomic result
    exec_time = atomic_result.get("execution_time_ms", 0) if isinstance(atomic_result, dict) else 0

    return specialist_result_to_dict(SpecialistResult(
        task_id=task.id,
        specialist_role=input_data.specialist_role,
        success=True,
        output=f"Specialist {input_data.specialist_role} completed task: {task.name}",
        execution_time_ms=exec_time
    ))


# =============================================================================
# LEVEL 2: SUPERVISOR WORKFLOW
# =============================================================================

def supervisor_workflow(ctx: wf.DaprWorkflowContext, decomposition_input):
    """
    Level 2: Supervisor Workflow

    Manages multiple specialist workflows by:
    1. Receiving task decomposition from coordinator
    2. Spawning specialist workflows in parallel
    3. Aggregating results with when_all

    Demonstrates:
    - Parallel child workflow execution
    - when_all for concurrent processing
    - SubOrchestrationInstance events
    - Result aggregation
    """
    # Handle dict input
    if isinstance(decomposition_input, dict):
        project_id = decomposition_input.get("project_id", "")
        project_name = decomposition_input.get("project_name", "")
        tasks = decomposition_input.get("tasks", [])
        fail_at_level = decomposition_input.get("fail_at_level")
    else:
        project_id = decomposition_input.project_id
        project_name = decomposition_input.project_name
        tasks = decomposition_input.tasks
        fail_at_level = decomposition_input.fail_at_level

    yield ctx.call_activity(announce,
        input=f"[L2-SUPERVISOR] Received {len(tasks)} tasks for project: {project_name}")

    # Failure injection at Level 2
    if fail_at_level == 2:
        yield ctx.call_activity(announce, input=f"[L2-SUPERVISOR] FAILURE INJECTED at Level 2")
        raise Exception("Simulated failure at Level 2 (Supervisor)")

    # Spawn specialists in parallel
    yield ctx.call_activity(announce,
        input=f"[L2-SUPERVISOR] Spawning {len(tasks)} specialist workflows in parallel...")

    specialist_tasks = []
    for i, task in enumerate(tasks):
        task_def = dict_to_task_definition(task)
        specialist_role = map_task_type_to_role(task_def.task_type)

        specialist_input = SpecialistInput(
            task=task,
            specialist_role=specialist_role,
            fail_at_level=fail_at_level
        )

        specialist_task = ctx.call_child_workflow(
            specialist_workflow,
            input=specialist_input_to_dict(specialist_input),
            instance_id=f"{project_id}_child_specialist_{i}"
        )
        specialist_tasks.append((specialist_task, task_def.id, specialist_role))

    # Wait for all specialists using when_all
    yield ctx.call_activity(announce,
        input=f"[L2-SUPERVISOR] Waiting for all specialists (when_all)...")

    tasks_completed = []
    tasks_failed = []
    total_time = 0

    # Collect just the tasks for when_all
    just_tasks = [t[0] for t in specialist_tasks]
    results = yield wf.when_all(just_tasks)

    # Process results
    for idx, result in enumerate(results):
        task_id = specialist_tasks[idx][1]
        role = specialist_tasks[idx][2]

        try:
            if isinstance(result, dict):
                success = result.get("success", False)
                exec_time = result.get("execution_time_ms", 0)
            else:
                success = getattr(result, "success", False)
                exec_time = getattr(result, "execution_time_ms", 0)

            total_time += exec_time

            if success:
                tasks_completed.append(task_id)
                yield ctx.call_activity(announce,
                    input=f"[L2-SUPERVISOR] Specialist {role} succeeded for {task_id}")
            else:
                tasks_failed.append(task_id)
                yield ctx.call_activity(announce,
                    input=f"[L2-SUPERVISOR] Specialist {role} failed for {task_id}")
        except Exception as e:
            tasks_failed.append(task_id)
            yield ctx.call_activity(announce,
                input=f"[L2-SUPERVISOR] Error processing result for {task_id}: {str(e)}")

    # Aggregate results
    yield ctx.call_activity(announce,
        input=f"[L2-SUPERVISOR] Aggregation complete: {len(tasks_completed)} succeeded, {len(tasks_failed)} failed")

    overall_success = len(tasks_failed) == 0

    yield ctx.call_activity(announce,
        input=f"[L2-SUPERVISOR] Project {project_name}: {'SUCCESS' if overall_success else 'PARTIAL FAILURE'}")

    return supervisor_result_to_dict(SupervisorResult(
        project_id=project_id,
        success=overall_success,
        message=f"Completed {len(tasks_completed)}/{len(tasks)} tasks successfully",
        tasks_completed=tasks_completed,
        tasks_failed=tasks_failed,
        total_execution_time_ms=total_time
    ))


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route("/", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "agent-worker"}), 200


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Initialize and run the agent worker service"""
    logger.info("Starting Agent Worker Service...")

    # Use resilient runtime for auto-reconnection
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )

    # Register workflows (Levels 2-4)
    wf_runtime.register_workflow(supervisor_workflow)
    wf_runtime.register_workflow(specialist_workflow)
    wf_runtime.register_workflow(atomic_task_workflow)

    # Register activities
    wf_runtime.register_activity(announce)
    wf_runtime.register_activity(execute_atomic_task)
    wf_runtime.register_activity(validate_atomic_result)

    wf_runtime.start()
    logger.info(f"Workflow runtime started on port {APP_PORT}")

    app.run(host='0.0.0.0', port=int(APP_PORT), debug=False, use_reloader=False)
    wf_runtime.shutdown()


if __name__ == "__main__":
    main()
