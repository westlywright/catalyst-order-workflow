# Catalyst Order Processing Workflow

This solution demonstrates all five Catalyst APIs through a comprehensive order processing workflow with advanced patterns including bulk processing, returns, and chaos engineering.

## Services Overview

**Core Services:**
- **order-processor**: Main workflow engine with approval handling and circuit breaker patterns
- **inventory**: Inventory management using Catalyst State API
- **payments**: Payment processing with failure simulation
- **shipping**: Shipping coordination service
- **notifications**: React UI for real-time workflow monitoring

**Advanced Workflow Services:**
- **batch-processor**: Bulk order processing with parent-child workflows
- **returns**: Return processing with workflow chaining and external events
- **chaos-engineer**: Failure simulation and resilience testing for dashboard debugging

## Prerequisites
- [Sign up](https://catalyst.diagrid.io) for Diagrid Catalyst
- Install latest [Diagrid CLI](https://docs.diagrid.io/catalyst/references/cli-reference/intro#installing-the-cli)
- Install [Python3](https://www.python.org/downloads/)
- Install [Node.js](https://nodejs.org/) (version 20 or higher) and npm

## Setup

### Prepare applications

Make the build script executable and run it:

```bash
chmod +x build-apps.sh
./build-apps.sh
```

### Deploy Catalyst resources

Replace `unique-project-name` with your project name:

```bash
export WORKFLOW_PROJECT_NAME="unique-project-name"
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

## Core Workflows

### 1. Basic Order Processing
- Standard order workflow with inventory, payment, and shipping
- Approval workflow for high-value orders (>$1000)
- Circuit breaker patterns for service resilience

### 2. Bulk Order Processing (Parent-Child Workflows)
- **Parent Workflow**: Orchestrates multiple items in a single order
- **Child Workflows**: Each item processed independently with parallel execution
- **Approval Integration**: High-value items require individual approval
- **Failure Isolation**: Partial failures don't affect other items

**Example Usage:**
```json
POST http://localhost:3007/bulk-orders
{
  "customer": "alice",
  "items": [
    {"item": "apple", "quantity": 2, "price": 50.0},
    {"item": "orange", "quantity": 1, "price": 75.0}
  ]
}
```

### 3. Return Processing (Workflow Chaining)
- **Workflow Chaining**: Returns reference and validate against original orders
- **Dynamic Child Workflows**: Different processing paths by return type:
  - **Defective**: Full refund, no restocking (disposal)
  - **Standard**: Sequential refund then inventory restocking
  - **Expedited**: Parallel refund and restocking for speed
- **External Events**: Manager approval for high-value returns (>$500)

**Example Usage:**
```json
POST http://localhost:3008/returns
{
  "original_order_id": "order_john_abc123",
  "customer": "john",
  "item": "apple",
  "reason": "defective",
  "return_value": 75.0
}
```

### 4. Chaos Engineering & Failure Simulation
- **Comprehensive Failure Types**: Timeouts, network errors, database failures, memory issues
- **Advanced Workflow Failures**: External event starvation, zombie child workflows, activity limbo
- **Circuit Breaker Testing**: Real-time monitoring of service resilience
- **Dashboard Integration**: Rich diagnostic events for monitoring systems

## Testing & Demo Files

### Manual Testing (VS Code REST Client)
- **`test-commands.http`**: Basic workflow testing (orders, approvals, status checks)
- **`bulk-demo.http`**: Bulk order processing demonstration (5-10 minutes)
- **`return-demo.http`**: Return workflow testing (8-12 minutes)
- **`chaos-demo.http`**: Basic chaos engineering patterns (10-15 minutes)
- **`advanced-chaos-demo.http`**: Advanced workflow failures (15-20 minutes)

### Automated Testing (Bash Scripts)
- **`run-chaos-demo.sh`**: Basic chaos patterns (8-12 minutes)
- **`run-advanced-chaos-demo.sh`**: Multi-service failures (8-12 minutes)
- **`run-advanced-workflow-chaos-demo.sh`**: Advanced workflow debugging (15-20 minutes)

## Key Features

### Enhanced Activity Naming
All workflows use descriptive activity names for clear dashboard visualization:

**Bulk Processing:**
- `announce_bulk_order_started` → `announce_child_workflow_spawned` → `announce_waiting_for_children`
- `announce_item_success` / `announce_item_failure` → `announce_bulk_order_completed`

**Returns Processing:**
- `announce_return_request_received` → `announce_return_validation_started` → `announce_return_approval_required`
- `announce_defective_return_started` / `announce_standard_refund_processing` / `announce_expedited_parallel_processing`

**Chaos Engineering:**
- `announce_failure_injection_started` → `execute_retry_policy_test` → `execute_circuit_breaker_test`
- `announce_external_event_starvation_started` → `announce_child_workflow_zombie_detected`

### Circuit Breaker Monitoring
Real-time circuit breaker status available at:
```http
GET http://localhost:3006/circuit-breakers
```

States: `closed` (healthy) → `open` (failing) → `half-open` (testing recovery)

### Dashboard Integration
- **Correlation IDs**: End-to-end workflow tracing
- **Severity Levels**: INFO, WARNING, ERROR, CRITICAL
- **Rich Context**: Execution times, retry counts, failure details
- **Real-time Updates**: Live notifications via pub/sub

## Advanced Scenarios

### Chaos Engineering Failure Types
- **Basic**: Timeouts, network errors, service unavailability
- **Advanced**: External event starvation, zombie child workflows, activity execution limbo, distributed transaction failures
- **Recovery**: Manual intervention simulation and automated recovery procedures

### Monitoring Endpoints
- `/chaos/events` - Diagnostic events for dashboards
- `/chaos/advanced-failures` - Advanced failure states
- `/chaos/zombie-workflows` - Zombie workflow detection
- `/chaos/missed-events` - External event tracking

## Quick Start

1. **Basic Order**: Use `test-commands.http` for simple workflow testing
2. **Bulk Orders**: Use `bulk-demo.http` for parent-child workflow patterns
3. **Returns**: Use `return-demo.http` for workflow chaining examples
4. **Chaos Testing**: Use `chaos-demo.http` for resilience validation
5. **Advanced Debugging**: Use `advanced-chaos-demo.http` for complex failure scenarios

**Live Monitoring**: Keep `http://localhost:8080` open during demos for real-time notifications.

