"""
Agent Coordinator Service - Level 1 Workflow Engine

Demonstrates:
- OrchestratorStarted/Completed with rich activity sequences
- Cross-app child workflow spawning (SubOrchestrationInstance)
- Rule-based task decomposition (agent-like behavior without LLM)
"""

import json
import logging
import os
import random
import string
import sys

# Add parent directory to path for common imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import dapr.ext.workflow as wf
from dapr.clients import DaprClient
from flask import Flask, request, jsonify

from common.agent_models import TaskType, TaskDefinition, task_definition_to_dict
from common.resilient_workflow_runtime import ResilientWorkflowRuntime
from models import (
    ProjectInput, TaskDecomposition, ProjectResult,
    dict_to_project_input, dict_to_task_decomposition,
    task_decomposition_to_dict, project_result_to_dict,
    dict_to_project_result
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

APP_PORT = os.getenv("APP_PORT", "3011")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)


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


def decompose_project(ctx: wf.WorkflowActivityContext, project_input) -> dict:
    """
    Rule-based task decomposition - simulates agent reasoning.

    Rules:
    1. Complexity determines task count
    2. Standard task progression: research -> analysis -> synthesis -> validation
    3. Generate tasks based on project requirements
    """
    project = dict_to_project_input(project_input)
    logger.info(f"[DECOMPOSE] Decomposing project: {project.name} (complexity: {project.complexity})")

    # Rule 1: Complexity determines task count
    complexity_map = {"simple": 2, "moderate": 3, "complex": 4}
    task_count = min(project.task_count, complexity_map.get(project.complexity, 3))

    # Rule 2: Standard task progression
    task_types = [TaskType.RESEARCH, TaskType.ANALYSIS, TaskType.SYNTHESIS, TaskType.VALIDATION]

    # Rule 3: Generate tasks
    tasks = []
    for i in range(task_count):
        task_type = task_types[i % len(task_types)]
        task = TaskDefinition(
            id=f"{project.id}_task_{i}",
            project_id=project.id,
            name=f"{task_type.value.title()} Phase",
            task_type=task_type.value,
            priority="medium" if i < task_count - 1 else "high",
            description=f"Execute {task_type.value} phase for project: {project.description}",
            estimated_duration_ms=project.simulate_delay_ms
        )
        tasks.append(task_definition_to_dict(task))

    decomposition = TaskDecomposition(
        project_id=project.id,
        project_name=project.name,
        tasks=tasks,
        coordination_strategy="parallel",
        fail_at_level=project.fail_at_level,
        fail_at_task=project.fail_at_task
    )

    logger.info(f"[DECOMPOSE] Created {len(tasks)} tasks for project {project.id}")
    return task_decomposition_to_dict(decomposition)


# =============================================================================
# LEVEL 1: PROJECT COORDINATOR WORKFLOW
# =============================================================================

def project_coordinator_workflow(ctx: wf.DaprWorkflowContext, project_input):
    """
    Level 1: Project Coordinator Workflow

    Orchestrates the entire project by:
    1. Decomposing the project into tasks (agent reasoning)
    2. Delegating to supervisor workflow via cross-app call
    3. Aggregating final results

    Demonstrates:
    - OrchestratorStarted/Completed events
    - Multiple activity calls
    - Cross-app call_child_workflow with app_id parameter
    """
    project = dict_to_project_input(project_input)

    # Announce start
    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Starting project: {project.name}")
    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Complexity: {project.complexity}, Tasks requested: {project.task_count}")

    # Failure injection at Level 1
    if project.fail_at_level == 1:
        yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] FAILURE INJECTED at Level 1")
        raise Exception("Simulated failure at Level 1 (Coordinator)")

    # Rule-based task decomposition (agent-like behavior)
    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Decomposing project into tasks...")
    decomposition_dict = yield ctx.call_activity(decompose_project, input=project_input)
    decomposition = dict_to_task_decomposition(decomposition_dict)

    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Created {len(decomposition.tasks)} tasks")

    # Announce delegation to supervisor
    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Delegating to supervisor (CROSS-APP)...")

    # CROSS-APP delegation to supervisor in agent-worker service
    try:
        supervisor_result_dict = yield ctx.call_child_workflow(
            "supervisor_workflow",  # String name for cross-app
            input=decomposition_dict,
            instance_id=f"{project.id}_child_supervisor",
            app_id="agent-worker"  # CROSS-APP call to different service!
        )
    except Exception as e:
        yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Supervisor failed: {str(e)}")
        return project_result_to_dict(ProjectResult(
            id=project.id,
            name=project.name,
            success=False,
            message=f"Supervisor workflow failed: {str(e)}",
            workflow_levels=["L1-COORDINATOR"],
            total_tasks=len(decomposition.tasks),
            completed_tasks=0,
            failed_tasks=len(decomposition.tasks)
        ))

    # Handle supervisor result
    if isinstance(supervisor_result_dict, dict):
        completed = len(supervisor_result_dict.get("tasks_completed", []))
        failed = len(supervisor_result_dict.get("tasks_failed", []))
        success = supervisor_result_dict.get("success", False)
        message = supervisor_result_dict.get("message", "")
    else:
        completed = len(getattr(supervisor_result_dict, "tasks_completed", []))
        failed = len(getattr(supervisor_result_dict, "tasks_failed", []))
        success = getattr(supervisor_result_dict, "success", False)
        message = getattr(supervisor_result_dict, "message", "")

    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Supervisor complete: {completed} succeeded, {failed} failed")
    yield ctx.call_activity(announce, input=f"[L1-COORDINATOR] Project {project.name} complete: {'SUCCESS' if success else 'FAILED'}")

    return project_result_to_dict(ProjectResult(
        id=project.id,
        name=project.name,
        success=success,
        message=message,
        workflow_levels=["L1-COORDINATOR", "L2-SUPERVISOR", "L3-SPECIALIST", "L4-ATOMIC"],
        total_tasks=len(decomposition.tasks),
        completed_tasks=completed,
        failed_tasks=failed
    ))


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route("/", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "agent-coordinator"}), 200


@app.route("/projects", methods=["POST"])
def submit_project():
    """
    Submit a new project for agent coordination.

    Request body:
    {
        "name": "Project Name",
        "description": "Project description",
        "complexity": "simple|moderate|complex",
        "task_count": 3,
        "fail_at_level": null,  // 1-4 for failure injection
        "simulate_delay_ms": 500
    }
    """
    data = request.get_json()

    # Generate project ID
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    project_id = f"project_{random_suffix}"

    # Build project input
    project_input = {
        "id": project_id,
        "name": data.get("name", "Unnamed Project"),
        "description": data.get("description", ""),
        "complexity": data.get("complexity", "moderate"),
        "task_count": data.get("task_count", 3),
        "fail_at_level": data.get("fail_at_level"),
        "fail_at_task": data.get("fail_at_task"),
        "simulate_delay_ms": data.get("simulate_delay_ms", 500)
    }

    logger.info(f"Submitting project: {project_id}")

    try:
        with DaprClient() as d:
            instance_id = d.start_workflow(
                workflow_component="dapr",
                workflow_name="project_coordinator_workflow",
                input=project_input,
                instance_id=project_id
            ).instance_id

            logger.info(f"Started workflow with instance_id: {instance_id}")

            return jsonify({
                "status": "accepted",
                "project_id": project_id,
                "instance_id": instance_id,
                "message": f"Project '{project_input['name']}' submitted for coordination"
            }), 202

    except Exception as e:
        logger.error(f"Error starting workflow: {e}")
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@app.route("/projects/<project_id>", methods=["GET"])
def get_project_status(project_id):
    """Get project workflow status"""
    try:
        with DaprClient() as d:
            state = d.get_workflow(
                workflow_component="dapr",
                instance_id=project_id
            )

            # Handle runtime_status as either string or enum
            if state.runtime_status:
                if isinstance(state.runtime_status, str):
                    status = state.runtime_status
                else:
                    status = state.runtime_status.name
            else:
                status = "UNKNOWN"

            response = {
                "project_id": project_id,
                "runtime_status": status,
                "created_at": str(state.created_at) if state.created_at else None,
                "last_updated_at": str(state.last_updated_at) if state.last_updated_at else None
            }

            # Include result if completed
            if status == "COMPLETED":
                if state.serialized_output:
                    response["result"] = json.loads(state.serialized_output)

            # Include failure info if failed
            if status == "FAILED":
                response["failure_details"] = state.failure_details if hasattr(state, 'failure_details') else None

            return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error getting workflow status: {e}")
        return jsonify({
            "error": "Not Found",
            "message": f"Project {project_id} not found or error: {str(e)}"
        }), 404


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Initialize and run the agent coordinator service"""
    logger.info("Starting Agent Coordinator Service...")

    # Use resilient runtime for auto-reconnection
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )

    # Register workflow and activities
    wf_runtime.register_workflow(project_coordinator_workflow)
    wf_runtime.register_activity(announce)
    wf_runtime.register_activity(decompose_project)

    wf_runtime.start()
    logger.info(f"Workflow runtime started on port {APP_PORT}")

    app.run(host='0.0.0.0', port=int(APP_PORT), debug=False, use_reloader=False)
    wf_runtime.shutdown()


if __name__ == "__main__":
    main()
