"""Shared agent models for cross-service workflow communication"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Any, Dict


class TaskType(Enum):
    """Task types for agent specialization"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"


@dataclass
class TaskDefinition:
    """Definition of a task to be processed by specialists"""
    id: str
    project_id: str
    name: str
    task_type: str
    priority: str
    description: str
    estimated_duration_ms: int
    dependencies: List[str] = field(default_factory=list)


def task_definition_to_dict(task: TaskDefinition) -> dict:
    """Convert TaskDefinition to dict for serialization"""
    return {
        "id": task.id,
        "project_id": task.project_id,
        "name": task.name,
        "task_type": task.task_type,
        "priority": task.priority,
        "description": task.description,
        "estimated_duration_ms": task.estimated_duration_ms,
        "dependencies": task.dependencies
    }


def dict_to_task_definition(data) -> TaskDefinition:
    """Convert dict to TaskDefinition"""
    if isinstance(data, TaskDefinition):
        return data
    return TaskDefinition(
        id=data.get("id", ""),
        project_id=data.get("project_id", ""),
        name=data.get("name", ""),
        task_type=data.get("task_type", ""),
        priority=data.get("priority", "medium"),
        description=data.get("description", ""),
        estimated_duration_ms=int(data.get("estimated_duration_ms", 500)),
        dependencies=data.get("dependencies", [])
    )
