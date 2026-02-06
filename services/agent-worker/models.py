"""Data models for the agent-worker service"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict


@dataclass
class SupervisorResult:
    """Result from supervisor workflow"""
    project_id: str
    success: bool
    message: str
    tasks_completed: List[str] = field(default_factory=list)
    tasks_failed: List[str] = field(default_factory=list)
    total_execution_time_ms: int = 0


@dataclass
class SpecialistInput:
    """Input for specialist workflow"""
    task: dict  # TaskDefinition as dict
    specialist_role: str
    fail_at_level: Optional[int] = None


@dataclass
class SpecialistResult:
    """Result from specialist workflow"""
    task_id: str
    specialist_role: str
    success: bool
    output: str
    execution_time_ms: int = 0


@dataclass
class AtomicTaskInput:
    """Input for atomic task workflow"""
    task_id: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    simulate_delay_ms: int = 500
    fail_at_level: Optional[int] = None


@dataclass
class AtomicTaskResult:
    """Result from atomic task workflow"""
    task_id: str
    action: str
    success: bool
    output: str
    execution_time_ms: int = 0


def dict_to_supervisor_result(data) -> SupervisorResult:
    """Convert dict to SupervisorResult"""
    if isinstance(data, SupervisorResult):
        return data
    return SupervisorResult(
        project_id=data.get("project_id", ""),
        success=data.get("success", False),
        message=data.get("message", ""),
        tasks_completed=data.get("tasks_completed", []),
        tasks_failed=data.get("tasks_failed", []),
        total_execution_time_ms=int(data.get("total_execution_time_ms", 0))
    )


def dict_to_specialist_input(data) -> SpecialistInput:
    """Convert dict to SpecialistInput"""
    if isinstance(data, SpecialistInput):
        return data
    return SpecialistInput(
        task=data.get("task", {}),
        specialist_role=data.get("specialist_role", "generalist"),
        fail_at_level=data.get("fail_at_level")
    )


def dict_to_specialist_result(data) -> SpecialistResult:
    """Convert dict to SpecialistResult"""
    if isinstance(data, SpecialistResult):
        return data
    return SpecialistResult(
        task_id=data.get("task_id", ""),
        specialist_role=data.get("specialist_role", ""),
        success=data.get("success", False),
        output=data.get("output", ""),
        execution_time_ms=int(data.get("execution_time_ms", 0))
    )


def dict_to_atomic_task_input(data) -> AtomicTaskInput:
    """Convert dict to AtomicTaskInput"""
    if isinstance(data, AtomicTaskInput):
        return data
    return AtomicTaskInput(
        task_id=data.get("task_id", ""),
        action=data.get("action", ""),
        parameters=data.get("parameters", {}),
        simulate_delay_ms=int(data.get("simulate_delay_ms", 500)),
        fail_at_level=data.get("fail_at_level")
    )


def dict_to_atomic_task_result(data) -> AtomicTaskResult:
    """Convert dict to AtomicTaskResult"""
    if isinstance(data, AtomicTaskResult):
        return data
    return AtomicTaskResult(
        task_id=data.get("task_id", ""),
        action=data.get("action", ""),
        success=data.get("success", False),
        output=data.get("output", ""),
        execution_time_ms=int(data.get("execution_time_ms", 0))
    )


def supervisor_result_to_dict(result: SupervisorResult) -> dict:
    """Convert SupervisorResult to dict for serialization"""
    return {
        "project_id": result.project_id,
        "success": result.success,
        "message": result.message,
        "tasks_completed": result.tasks_completed,
        "tasks_failed": result.tasks_failed,
        "total_execution_time_ms": result.total_execution_time_ms
    }


def specialist_input_to_dict(input_data: SpecialistInput) -> dict:
    """Convert SpecialistInput to dict for serialization"""
    return {
        "task": input_data.task,
        "specialist_role": input_data.specialist_role,
        "fail_at_level": input_data.fail_at_level
    }


def specialist_result_to_dict(result: SpecialistResult) -> dict:
    """Convert SpecialistResult to dict for serialization"""
    return {
        "task_id": result.task_id,
        "specialist_role": result.specialist_role,
        "success": result.success,
        "output": result.output,
        "execution_time_ms": result.execution_time_ms
    }


def atomic_task_input_to_dict(input_data: AtomicTaskInput) -> dict:
    """Convert AtomicTaskInput to dict for serialization"""
    return {
        "task_id": input_data.task_id,
        "action": input_data.action,
        "parameters": input_data.parameters,
        "simulate_delay_ms": input_data.simulate_delay_ms,
        "fail_at_level": input_data.fail_at_level
    }


def atomic_task_result_to_dict(result: AtomicTaskResult) -> dict:
    """Convert AtomicTaskResult to dict for serialization"""
    return {
        "task_id": result.task_id,
        "action": result.action,
        "success": result.success,
        "output": result.output,
        "execution_time_ms": result.execution_time_ms
    }
