"""Data models for the agent-coordinator service"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ProjectInput:
    """Input for project coordination workflow"""
    id: str
    name: str
    description: str
    complexity: str  # "simple", "moderate", "complex"
    task_count: int = 3
    fail_at_level: Optional[int] = None  # 1-4 for failure injection
    fail_at_task: Optional[str] = None
    simulate_delay_ms: int = 500


@dataclass
class TaskDecomposition:
    """Result of project decomposition into tasks"""
    project_id: str
    project_name: str
    tasks: List[dict]  # List of TaskDefinition dicts
    coordination_strategy: str  # "parallel" or "sequential"
    fail_at_level: Optional[int] = None
    fail_at_task: Optional[str] = None


@dataclass
class ProjectResult:
    """Result of project coordination workflow"""
    id: str
    name: str
    success: bool
    message: str
    workflow_levels: List[str] = field(default_factory=list)
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0


def dict_to_project_input(data) -> ProjectInput:
    """Convert dict to ProjectInput"""
    if isinstance(data, ProjectInput):
        return data
    return ProjectInput(
        id=data.get("id", ""),
        name=data.get("name", ""),
        description=data.get("description", ""),
        complexity=data.get("complexity", "moderate"),
        task_count=int(data.get("task_count", 3)),
        fail_at_level=data.get("fail_at_level"),
        fail_at_task=data.get("fail_at_task"),
        simulate_delay_ms=int(data.get("simulate_delay_ms", 500))
    )


def dict_to_task_decomposition(data) -> TaskDecomposition:
    """Convert dict to TaskDecomposition"""
    if isinstance(data, TaskDecomposition):
        return data
    return TaskDecomposition(
        project_id=data.get("project_id", ""),
        project_name=data.get("project_name", ""),
        tasks=data.get("tasks", []),
        coordination_strategy=data.get("coordination_strategy", "parallel"),
        fail_at_level=data.get("fail_at_level"),
        fail_at_task=data.get("fail_at_task")
    )


def dict_to_project_result(data) -> ProjectResult:
    """Convert dict to ProjectResult"""
    if isinstance(data, ProjectResult):
        return data
    return ProjectResult(
        id=data.get("id", ""),
        name=data.get("name", ""),
        success=data.get("success", False),
        message=data.get("message", ""),
        workflow_levels=data.get("workflow_levels", []),
        total_tasks=int(data.get("total_tasks", 0)),
        completed_tasks=int(data.get("completed_tasks", 0)),
        failed_tasks=int(data.get("failed_tasks", 0))
    )


def task_decomposition_to_dict(decomposition: TaskDecomposition) -> dict:
    """Convert TaskDecomposition to dict for serialization"""
    return {
        "project_id": decomposition.project_id,
        "project_name": decomposition.project_name,
        "tasks": decomposition.tasks,
        "coordination_strategy": decomposition.coordination_strategy,
        "fail_at_level": decomposition.fail_at_level,
        "fail_at_task": decomposition.fail_at_task
    }


def project_result_to_dict(result: ProjectResult) -> dict:
    """Convert ProjectResult to dict for serialization"""
    return {
        "id": result.id,
        "name": result.name,
        "success": result.success,
        "message": result.message,
        "workflow_levels": result.workflow_levels,
        "total_tasks": result.total_tasks,
        "completed_tasks": result.completed_tasks,
        "failed_tasks": result.failed_tasks
    }
