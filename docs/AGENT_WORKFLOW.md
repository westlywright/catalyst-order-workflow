# Mock Agent Task Delegation System

## TL;DR

A demonstration system showing 4-level nested sub-workflows with cross-app delegation using Diagrid Catalyst. Two services (`agent-coordinator` and `agent-worker`) simulate an AI agent architecture with rule-based task decomposition (no LLM required). Projects flow through Coordinator -> Supervisor -> Specialists -> Atomic Tasks, showcasing `call_child_workflow` with the `app_id` parameter for cross-service orchestration and `when_all` for parallel execution.

**Quick Start:**
```bash
# Start all services
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME

# Submit a project
curl -X POST http://localhost:3011/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Project", "complexity": "moderate", "task_count": 3}'
```

---

## Overview

### Purpose

This system demonstrates advanced Diagrid Catalyst workflow patterns for building agent-like task delegation systems without LLM dependencies. It showcases:

- **Cross-App Workflow Delegation**: Using `call_child_workflow` with `app_id` parameter to spawn workflows in different services
- **Nested Sub-Workflows**: 4 levels of workflow hierarchy (Coordinator -> Supervisor -> Specialist -> Atomic)
- **Parallel Execution**: Using `when_all` for concurrent specialist processing
- **Rule-Based Agent Logic**: Deterministic task decomposition based on complexity rules
- **Failure Injection**: Testing error handling at any workflow level

### Why It's Useful

| Use Case | Benefit |
|----------|---------|
| Agent Architectures | Model multi-agent systems without LLM costs during development |
| Workflow Patterns | Learn nested sub-orchestration patterns |
| Error Testing | Validate failure handling with configurable injection points |
| Demo Purposes | Clear visual hierarchy in Catalyst UI console |

### Key Features

- **SubOrchestrationInstance**: Cross-app child workflow creation visible in Catalyst UI
- **Deterministic Behavior**: Rule-based logic makes demos reproducible
- **Configurable Delays**: Adjust execution speed for live demonstrations
- **Rich Notifications**: Real-time progress via pub/sub to notifications UI

---

## Architecture

### 4-Level Workflow Hierarchy

```
+-------------------------------------------------------------------+
|                         agent-coordinator                          |
|                           (Port 3011)                              |
|  +-------------------------------------------------------------+  |
|  |  LEVEL 1: ProjectCoordinatorWorkflow                        |  |
|  |  - Receives project request                                 |  |
|  |  - Decomposes project into tasks (rule-based)               |  |
|  |  - Delegates via CROSS-APP call_child_workflow              |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
                              |
                              | SubOrchestrationInstance
                              | app_id="agent-worker"
                              v
+-------------------------------------------------------------------+
|                          agent-worker                              |
|                           (Port 3012)                              |
|  +-------------------------------------------------------------+  |
|  |  LEVEL 2: SupervisorWorkflow                                |  |
|  |  - Receives task decomposition                              |  |
|  |  - Spawns N specialists in PARALLEL                         |  |
|  |  - Uses when_all for concurrent execution                   |  |
|  |  - Aggregates results                                       |  |
|  +-------------------------------------------------------------+  |
|                              |                                     |
|        +---------------------+---------------------+               |
|        |                     |                     |               |
|        v                     v                     v               |
|  +-------------+       +-------------+       +-------------+       |
|  |  LEVEL 3:   |       |  LEVEL 3:   |       |  LEVEL 3:   |       |
|  |  Specialist |       |  Specialist |       |  Specialist |       |
|  |  (Researcher)|      |  (Analyst)  |       |  (Validator)|       |
|  +-------------+       +-------------+       +-------------+       |
|        |                     |                     |               |
|        v                     v                     v               |
|  +-------------+       +-------------+       +-------------+       |
|  |  LEVEL 4:   |       |  LEVEL 4:   |       |  LEVEL 4:   |       |
|  |  AtomicTask |       |  AtomicTask |       |  AtomicTask |       |
|  +-------------+       +-------------+       +-------------+       |
+-------------------------------------------------------------------+
```

### Workflow Instance Naming

Instance IDs maintain correlation across the hierarchy:

```
project_abc123                          # L1: Coordinator
├── project_abc123_supervisor           # L2: Supervisor (cross-app)
│   ├── project_abc123_specialist_0     # L3: Researcher
│   │   └── project_abc123_specialist_0_atomic    # L4: Atomic
│   ├── project_abc123_specialist_1     # L3: Analyst
│   │   └── project_abc123_specialist_1_atomic    # L4: Atomic
│   └── project_abc123_specialist_2     # L3: Synthesizer
│       └── project_abc123_specialist_2_atomic    # L4: Atomic
```

### Task Type to Specialist Role Mapping

| Task Type | Specialist Role | Description |
|-----------|-----------------|-------------|
| `research` | Researcher | Information gathering phase |
| `analysis` | Analyst | Data analysis phase |
| `synthesis` | Synthesizer | Combining findings phase |
| `validation` | Validator | Final verification phase |

### Complexity to Task Count Mapping

| Complexity | Max Tasks | Task Pipeline |
|------------|-----------|---------------|
| `simple` | 2 | Research -> Analysis |
| `moderate` | 3 | Research -> Analysis -> Synthesis |
| `complex` | 4 | Research -> Analysis -> Synthesis -> Validation |

---

## Services

### agent-coordinator (Port 3011)

The entry point service hosting Level 1 workflows.

**Location:** `services/agent-coordinator/`

**Responsibilities:**
- Accept project submissions via REST API
- Decompose projects into tasks using rule-based logic
- Delegate to supervisor via cross-app workflow call
- Aggregate final results

**Registered Components:**

| Type | Name | Description |
|------|------|-------------|
| Workflow | `project_coordinator_workflow` | Level 1 orchestrator |
| Activity | `announce` | Publishes notifications to pub/sub |
| Activity | `decompose_project` | Rule-based task decomposition |

**Key Code Pattern - Cross-App Delegation:**

```python
# Cross-app call to agent-worker service
supervisor_result_dict = yield ctx.call_child_workflow(
    "supervisor_workflow",  # String name required for cross-app
    input=decomposition_dict,
    instance_id=f"{project.id}_supervisor",
    app_id="agent-worker"  # Target service app_id
)
```

### agent-worker (Port 3012)

The worker service hosting Levels 2-4 workflows.

**Location:** `services/agent-worker/`

**Responsibilities:**
- Run supervisor workflow to manage specialists
- Execute specialist workflows with role-based processing
- Perform atomic task execution with timers

**Registered Components:**

| Type | Name | Level | Description |
|------|------|-------|-------------|
| Workflow | `supervisor_workflow` | L2 | Parallel specialist management |
| Workflow | `specialist_workflow` | L3 | Role-based task processing |
| Workflow | `atomic_task_workflow` | L4 | Timer-based task execution |
| Activity | `announce` | - | Publishes notifications |
| Activity | `execute_atomic_task` | - | Simulates task work |
| Activity | `validate_atomic_result` | - | Validates task output |

**Key Code Pattern - Parallel Execution with when_all:**

```python
# Spawn all specialists
specialist_tasks = []
for i, task in enumerate(tasks):
    specialist_task = ctx.call_child_workflow(
        specialist_workflow,
        input=specialist_input_to_dict(specialist_input),
        instance_id=f"{project_id}_specialist_{i}"
    )
    specialist_tasks.append(specialist_task)

# Wait for all to complete
results = yield wf.when_all([t[0] for t in specialist_tasks])
```

---

## Data Models

### Shared Models (services/common/agent_models.py)

```python
class TaskType(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"

@dataclass
class TaskDefinition:
    id: str
    project_id: str
    name: str
    task_type: str
    priority: str
    description: str
    estimated_duration_ms: int
    dependencies: List[str]
```

### Coordinator Models (agent-coordinator/models.py)

```python
@dataclass
class ProjectInput:
    id: str
    name: str
    description: str
    complexity: str          # "simple", "moderate", "complex"
    task_count: int          # Requested number of tasks
    fail_at_level: int       # 1-4 for failure injection
    simulate_delay_ms: int   # Delay per task

@dataclass
class TaskDecomposition:
    project_id: str
    project_name: str
    tasks: List[dict]        # TaskDefinition list
    coordination_strategy: str  # "parallel" or "sequential"
    fail_at_level: int

@dataclass
class ProjectResult:
    id: str
    name: str
    success: bool
    message: str
    workflow_levels: List[str]
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
```

### Worker Models (agent-worker/models.py)

```python
@dataclass
class SupervisorResult:
    project_id: str
    success: bool
    message: str
    tasks_completed: List[str]
    tasks_failed: List[str]
    total_execution_time_ms: int

@dataclass
class SpecialistInput:
    task: dict
    specialist_role: str
    fail_at_level: int

@dataclass
class AtomicTaskInput:
    task_id: str
    action: str
    parameters: Dict[str, Any]
    simulate_delay_ms: int
    fail_at_level: int
```

---

## Usage

### Prerequisites

1. Diagrid CLI installed
2. Catalyst project configured
3. Project dependencies installed via `./build-apps.sh`

### Starting the System

```bash
# Set your Catalyst project
export WORKFLOW_PROJECT_NAME="your-project-name"

# Start all services
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

### Verifying Services

```bash
# Health check coordinator
curl http://localhost:3011/healthz

# Health check worker
curl http://localhost:3012/healthz
```

### Submitting a Project

```bash
curl -X POST http://localhost:3011/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Market Analysis",
    "description": "Comprehensive market research",
    "complexity": "moderate",
    "task_count": 3,
    "simulate_delay_ms": 500
  }'
```

**Response:**
```json
{
  "status": "accepted",
  "project_id": "project_abc123",
  "instance_id": "project_abc123",
  "message": "Project 'Market Analysis' submitted for coordination"
}
```

### Checking Project Status

```bash
curl http://localhost:3011/projects/project_abc123
```

**Response (completed):**
```json
{
  "project_id": "project_abc123",
  "runtime_status": "COMPLETED",
  "created_at": "2024-01-15T10:30:00Z",
  "last_updated_at": "2024-01-15T10:30:05Z",
  "result": {
    "id": "project_abc123",
    "name": "Market Analysis",
    "success": true,
    "message": "Completed 3/3 tasks successfully",
    "workflow_levels": ["L1-COORDINATOR", "L2-SUPERVISOR", "L3-SPECIALIST", "L4-ATOMIC"],
    "total_tasks": 3,
    "completed_tasks": 3,
    "failed_tasks": 0
  }
}
```

---

## Demo Scenarios

Use `agent-demo.http` with VS Code REST Client for interactive testing.

### Scenario 1: Simple Project (2 Tasks)

**Purpose:** Minimal demonstration of 4-level hierarchy

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Simple Report",
    "description": "Create a basic analysis report",
    "complexity": "simple",
    "task_count": 2,
    "simulate_delay_ms": 500
}
```

**Expected Workflow Hierarchy:**
```
project_xxx (L1)
└── project_xxx_supervisor (L2)
    ├── project_xxx_specialist_0 (L3: Researcher)
    │   └── project_xxx_specialist_0_atomic (L4)
    └── project_xxx_specialist_1 (L3: Analyst)
        └── project_xxx_specialist_1_atomic (L4)
```

### Scenario 2: Moderate Project (3 Tasks)

**Purpose:** Shows research -> analysis -> synthesis pipeline

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Market Analysis",
    "description": "Conduct comprehensive market research",
    "complexity": "moderate",
    "task_count": 3,
    "simulate_delay_ms": 400
}
```

### Scenario 3: Complex Project (4 Tasks)

**Purpose:** Full pipeline with maximum parallelism

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Strategic Initiative",
    "description": "Full strategic analysis with validation",
    "complexity": "complex",
    "task_count": 4,
    "simulate_delay_ms": 300
}
```

### Scenario 4: Quick Demo

**Purpose:** Fast execution for live demonstrations

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Quick Demo",
    "description": "Fast execution demonstration",
    "complexity": "simple",
    "task_count": 2,
    "simulate_delay_ms": 100
}
```

---

## API Reference

### agent-coordinator (Port 3011)

#### GET /healthz

Health check endpoint.

**Response:**
```json
{"status": "healthy", "service": "agent-coordinator"}
```

#### POST /projects

Submit a new project for agent coordination.

**Request Body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | No | "Unnamed Project" | Project display name |
| `description` | string | No | "" | Project description |
| `complexity` | string | No | "moderate" | "simple", "moderate", or "complex" |
| `task_count` | int | No | 3 | Requested number of tasks |
| `fail_at_level` | int | No | null | 1-4 for failure injection |
| `fail_at_task` | string | No | null | Specific task ID to fail |
| `simulate_delay_ms` | int | No | 500 | Delay per atomic task |

**Response (202 Accepted):**
```json
{
  "status": "accepted",
  "project_id": "project_abc123",
  "instance_id": "project_abc123",
  "message": "Project 'Name' submitted for coordination"
}
```

#### GET /projects/{project_id}

Get project workflow status.

**Response (200 OK):**
```json
{
  "project_id": "project_abc123",
  "runtime_status": "COMPLETED|RUNNING|FAILED|PENDING",
  "created_at": "2024-01-15T10:30:00Z",
  "last_updated_at": "2024-01-15T10:30:05Z",
  "result": { ... }
}
```

### agent-worker (Port 3012)

#### GET /healthz

Health check endpoint.

**Response:**
```json
{"status": "healthy", "service": "agent-worker"}
```

> Note: agent-worker does not expose REST endpoints for workflow submission. Workflows are invoked via cross-app `call_child_workflow` from agent-coordinator.

---

## Workflow Events

### What to Look for in Catalyst UI

1. **Navigate to Workflows** in the Catalyst console (console.diagrid.io)

2. **Identify the workflow hierarchy by instance_id patterns:**
   - `project_xxx` - Parent coordinator workflow
   - `project_xxx_supervisor` - Child supervisor (cross-app)
   - `project_xxx_specialist_N` - Grandchild specialists
   - `project_xxx_specialist_N_atomic` - Great-grandchild atomic tasks

3. **Key Events to Observe:**

| Event Type | Description | Where |
|------------|-------------|-------|
| `OrchestratorStarted` | Workflow began execution | All 4 levels |
| `OrchestratorCompleted` | Workflow finished | All 4 levels |
| `ActivityScheduled` | Activity queued for execution | Activities |
| `ActivityCompleted` | Activity finished | Activities |
| `SubOrchestrationInstanceCreated` | Child workflow spawned | L1->L2, L2->L3, L3->L4 |
| `SubOrchestrationInstanceCompleted` | Child workflow finished | When child completes |
| `TimerCreated` | Timer scheduled | L4 atomic tasks |
| `TimerFired` | Timer completed | L4 atomic tasks |

4. **Cross-App Verification:**
   - The `SubOrchestrationInstanceCreated` event from L1 (agent-coordinator) to L2 (agent-worker) should show `app_id="agent-worker"`
   - This confirms cross-service workflow delegation is working

### Notification Prefixes

Watch the notifications UI (localhost:8080) for messages with these prefixes:

| Prefix | Level | Description |
|--------|-------|-------------|
| `[L1-COORDINATOR]` | Level 1 | Project coordination events |
| `[L2-SUPERVISOR]` | Level 2 | Task supervision events |
| `[L3-SPECIALIST:ROLE]` | Level 3 | Role-specific processing (RESEARCHER, ANALYST, etc.) |
| `[L4-ATOMIC]` | Level 4 | Atomic task execution events |

---

## Failure Injection

Test error handling at any workflow level using the `fail_at_level` parameter.

### Level 1 Failure (Coordinator)

**Behavior:** Immediate failure, no delegation to supervisor

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Fail at Coordinator",
    "description": "Test Level 1 failure injection",
    "complexity": "simple",
    "task_count": 2,
    "fail_at_level": 1
}
```

**Expected Notifications:**
```
[L1-COORDINATOR] Starting project: Fail at Coordinator
[L1-COORDINATOR] FAILURE INJECTED at Level 1
```

**Result:** Workflow status = `FAILED`

### Level 2 Failure (Supervisor)

**Behavior:** Cross-app delegation succeeds, supervisor fails before spawning specialists

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Fail at Supervisor",
    "description": "Test Level 2 failure injection",
    "complexity": "simple",
    "task_count": 2,
    "fail_at_level": 2
}
```

**Expected Notifications:**
```
[L1-COORDINATOR] Starting project: Fail at Supervisor
[L1-COORDINATOR] Delegating to supervisor (CROSS-APP)...
[L2-SUPERVISOR] Received 2 tasks for project: Fail at Supervisor
[L2-SUPERVISOR] FAILURE INJECTED at Level 2
[L1-COORDINATOR] Supervisor failed: Simulated failure at Level 2
```

### Level 3 Failure (Specialist)

**Behavior:** Specialists fail, supervisor aggregates failures

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Fail at Specialist",
    "description": "Test Level 3 failure injection",
    "complexity": "moderate",
    "task_count": 3,
    "fail_at_level": 3
}
```

**Expected Notifications:**
```
[L2-SUPERVISOR] Spawning 3 specialist workflows in parallel...
[L3-SPECIALIST:RESEARCHER] Processing: Research Phase
[L3-SPECIALIST:RESEARCHER] FAILURE INJECTED at Level 3
[L3-SPECIALIST:ANALYST] Processing: Analysis Phase
[L3-SPECIALIST:ANALYST] FAILURE INJECTED at Level 3
...
[L2-SUPERVISOR] Aggregation complete: 0 succeeded, 3 failed
```

### Level 4 Failure (Atomic Task)

**Behavior:** Atomic tasks fail, bubbles up through specialists

```http
POST http://localhost:3011/projects
Content-Type: application/json

{
    "name": "Fail at Atomic Task",
    "description": "Test Level 4 failure injection",
    "complexity": "simple",
    "task_count": 2,
    "fail_at_level": 4
}
```

**Expected Notifications:**
```
[L3-SPECIALIST:RESEARCHER] Delegating to atomic task...
[L4-ATOMIC] Starting: execute_researcher
[L4-ATOMIC] FAILURE INJECTED at Level 4
[L3-SPECIALIST:RESEARCHER] Atomic task failed: Simulated failure at Level 4
```

### Failure Summary Table

| Level | Component | Exception Message | Impact |
|-------|-----------|-------------------|--------|
| 1 | Coordinator | "Simulated failure at Level 1 (Coordinator)" | No tasks executed |
| 2 | Supervisor | "Simulated failure at Level 2 (Supervisor)" | No specialists spawned |
| 3 | Specialist | "Simulated failure at Level 3 (Specialist: {role})" | Individual specialist fails |
| 4 | Atomic Task | "Simulated failure at Level 4 (Atomic: {action})" | Task fails, specialist reports failure |

---

## File Reference

| File | Description |
|------|-------------|
| `services/agent-coordinator/app.py` | Level 1 workflow and REST API |
| `services/agent-coordinator/models.py` | Coordinator data models |
| `services/agent-worker/app.py` | Levels 2-4 workflows |
| `services/agent-worker/models.py` | Worker data models |
| `services/common/agent_models.py` | Shared models across services |
| `agent-demo.http` | VS Code REST Client test scenarios |
| `dapr.yaml` | Service configuration |

---

## Related Documentation

- [Diagrid Catalyst Workflows](https://docs.diagrid.io/catalyst/workflows)
- [Dapr Workflow SDK](https://docs.dapr.io/developing-applications/building-blocks/workflow/)
- Main project README for overall architecture
