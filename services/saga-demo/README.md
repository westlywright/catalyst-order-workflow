# Saga Demo Service

Advanced Dapr workflow patterns for showcasing Diagrid Catalyst UI capabilities.

**Port:** 3009
**Language:** Python (Flask)
**Version:** 1.0.0

## Overview

The saga-demo service demonstrates three advanced Dapr 1.16 workflow patterns designed for repeatable demonstrations in the Diagrid Catalyst UI:

| Pattern | Purpose | Key Feature |
|---------|---------|-------------|
| Saga with Compensation | Distributed transaction rollback | Reverse-order compensating actions |
| Continue-As-New | Long-running workflow management | History reset between iterations |
| Multi-Level Workflows | Parent-child-grandchild hierarchy | Parallel grandchild execution |

All workflows support **input-driven failure control** for deterministic demo scenarios.

---

## Quick Start

```bash
# Install dependencies
cd services/saga-demo
pip3 install -r requirements.txt

# Start all services (from project root)
export WORKFLOW_PROJECT_NAME="your-project-name"
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME

# Test health
curl http://localhost:3009/healthz
```

---

## Workflow Patterns

### 1. Saga Pattern with Compensation

Executes a three-step order process with explicit compensation on failure.

```
SUCCESS PATH:
  reserve_inventory --> charge_payment --> create_shipment --> SUCCESS
         |                   |                   |
       step 1              step 2              step 3

FAILURE PATH (at ship step):
  reserve_inventory --> charge_payment --> create_shipment [FAIL]
         |                   |                   |
       step 1              step 2              step 3
                                                 |
                            <--------------------+
                            |
  release_inventory <-- refund_payment <-- COMPENSATE
       comp 2              comp 1
                            |
                            v
                    ROLLBACK COMPLETE
```

**Compensation Order:** Compensations execute in reverse order of completed steps:
- Ship fails: refund_payment -> release_inventory
- Charge fails: release_inventory
- Reserve fails: no compensation needed

### 2. Continue-As-New Pattern

Monitors an order with periodic status checks while managing workflow history.

```
Iteration 1          Iteration 2          Iteration 3
+-----------+        +-----------+        +-----------+
| check     |        | check     |        | check     |
| status    |        | status    |        | status    |
|           |        |           |        |           |
| wait 5s   |        | wait 5s   |        | COMPLETE  |
|           |        |           |        | (max=3)   |
| continue  | -----> | continue  | -----> |           |
| as new    |  fresh | as new    |  fresh +-----------+
+-----------+ history+-----------+ history
```

**Benefits:**
- Prevents unbounded history growth
- State preserved in config dataclass
- Each iteration starts with clean history

### 3. Multi-Level Workflow Hierarchy

Parent-child-grandchild structure with parallel grandchild execution.

```
fulfill_xxx (Parent: Fulfillment)
|
+-- fulfill_xxx_validation (Child: Validation)
    |
    +-- fulfill_xxx_address_check (Grandchild) --+
    |                                            | parallel
    +-- fulfill_xxx_payment_check (Grandchild) --+   via
                                                 | when_all
                                                 v
                                            [Both complete]
                                                 |
                                                 v
                                       execute_fulfillment
```

**Workflow IDs Generated:**
```
fulfill_frank_abc12            (parent)
fulfill_frank_abc12_validation (child)
fulfill_frank_abc12_address_check (grandchild)
fulfill_frank_abc12_payment_check (grandchild)
```

---

## Input-Driven Failure Control

Control workflow behavior through request parameters:

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `fail_at_step` | string | `"reserve"`, `"charge"`, `"ship"` | Step to fail at |
| `fail_type` | string | `"timeout"`, `"error"`, `"unavailable"`, `"fatal"` | Type of failure |
| `simulate_delay_ms` | int | 0-5000 | Delay for visualization |
| `force_success` | bool | true/false | Bypass configured failures |

**Failure Types:**
- `"timeout"`, `"error"`, `"unavailable"` - Trigger saga compensation pattern (rollback)
- `"fatal"` - Workflow marked as FAILED immediately, no compensations, allows rerun

**Example Combinations:**

```json
// Fail at charge step with error
{
  "fail_at_step": "charge",
  "fail_type": "error"
}

// Slow execution for demo visualization
{
  "simulate_delay_ms": 1000
}

// Force success despite failure config
{
  "fail_at_step": "ship",
  "fail_type": "timeout",
  "force_success": true
}

// Fatal failure - workflow FAILED, no compensations, can be rerun
{
  "fail_at_step": "charge",
  "fail_type": "fatal"
}
```

---

## API Endpoints

### Saga Workflows

#### POST /saga/orders

Submit an order to be processed via saga pattern.

**Request:**
```json
{
  "customer": "Alice",
  "item": "laptop",
  "total": 999.99,
  "destination": "123 Main Street",
  "fail_at_step": "charge",
  "fail_type": "error",
  "simulate_delay_ms": 500,
  "force_success": false
}
```

**Response (202 Accepted):**
```json
{
  "instance_id": "saga_alice_abc12",
  "order_id": "saga_alice_abc12",
  "failure_config": {
    "fail_at_step": "charge",
    "fail_type": "error",
    "simulate_delay_ms": 500,
    "force_success": false
  }
}
```

#### GET /saga/orders/{order_id}

Get saga workflow status and result.

**Response (200 OK):**
```json
{
  "id": "saga_alice_abc12",
  "status": "COMPLETED",
  "created_time": "2024-01-22T10:00:00.000000",
  "last_updated_time": "2024-01-22T10:00:05.000000",
  "result": {
    "id": "saga_alice_abc12",
    "success": false,
    "message": "Saga rolled back: Simulated error failure at charge step",
    "steps_completed": ["reserve"],
    "compensations_executed": ["release_inventory"],
    "failure_details": "Simulated error failure at charge step"
  }
}
```

### Monitor Workflows (Continue-As-New)

#### POST /monitor/start

Start monitoring an order with periodic status checks.

**Request:**
```json
{
  "order_id": "saga_alice_abc12",
  "check_interval_seconds": 5,
  "max_checks": 10
}
```

**Response (202 Accepted):**
```json
{
  "instance_id": "monitor_saga_alice_abc12_1234",
  "monitor_id": "monitor_saga_alice_abc12_1234",
  "config": {
    "order_id": "saga_alice_abc12",
    "check_interval_seconds": 5,
    "max_checks": 10
  }
}
```

#### GET /monitor/{monitor_id}

Get monitor workflow status.

**Response (200 OK):**
```json
{
  "id": "monitor_saga_alice_abc12_1234",
  "status": "COMPLETED",
  "created_time": "2024-01-22T10:00:00.000000",
  "last_updated_time": "2024-01-22T10:00:50.000000",
  "result": {
    "order_id": "saga_alice_abc12",
    "iterations_completed": 10,
    "final_status": "delivered",
    "message": "Monitoring completed after 10 iterations"
  }
}
```

### Fulfillment Workflows (Multi-Level)

#### POST /fulfillment/orders

Submit order for multi-level workflow processing.

**Request:**
```json
{
  "customer": "Frank",
  "item": "headphones",
  "total": 199.99,
  "destination": "888 Audio Drive"
}
```

**Response (202 Accepted):**
```json
{
  "instance_id": "fulfill_frank_xyz98",
  "order_id": "fulfill_frank_xyz98",
  "workflow_hierarchy": [
    "fulfill_frank_xyz98 (fulfillment - parent)",
    "fulfill_frank_xyz98_validation (validation - child)",
    "fulfill_frank_xyz98_address_check (address - grandchild)",
    "fulfill_frank_xyz98_payment_check (payment - grandchild)"
  ]
}
```

#### GET /fulfillment/orders/{order_id}

Get fulfillment workflow status.

**Response (200 OK):**
```json
{
  "id": "fulfill_frank_xyz98",
  "status": "COMPLETED",
  "created_time": "2024-01-22T10:00:00.000000",
  "last_updated_time": "2024-01-22T10:00:03.000000",
  "result": {
    "order_id": "fulfill_frank_xyz98",
    "success": true,
    "message": "Fulfillment completed successfully",
    "child_workflows": ["fulfill_frank_xyz98_validation"]
  }
}
```

### Health Check

#### GET /healthz

**Response (200 OK):**
```json
{
  "service": "saga-demo",
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## Demo Scenarios

### Scenario 1: Saga Success

Demonstrates complete saga flow without failures.

```bash
curl -X POST http://localhost:3009/saga/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "Alice",
    "item": "laptop",
    "total": 999.99,
    "destination": "123 Main Street"
  }'
```

**Expected Notifications:**
```
[SAGA] Starting saga for order saga_alice_xxxxx
[SAGA] Step 1: Reserving inventory for laptop
[SAGA] Step 1 complete: Inventory reserved for laptop
[SAGA] Step 2: Charging payment $999.99
[SAGA] Step 2 complete: Payment charged $999.99
[SAGA] Step 3: Creating shipment to 123 Main Street
[SAGA] Step 3 complete: Shipment created to 123 Main Street
[SAGA] SUCCESS: Order saga_alice_xxxxx completed successfully!
```

### Scenario 2: Saga with Full Compensation

Demonstrates failure at ship step with full compensation chain.

```bash
curl -X POST http://localhost:3009/saga/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "Bob",
    "item": "phone",
    "total": 599.99,
    "destination": "456 Oak Avenue",
    "fail_at_step": "ship",
    "fail_type": "timeout",
    "simulate_delay_ms": 500
  }'
```

**Expected Notifications:**
```
[SAGA] Starting saga for order saga_bob_xxxxx
[SAGA] Step 1: Reserving inventory for phone
[SAGA] Step 1 complete: Inventory reserved for phone
[SAGA] Step 2: Charging payment $599.99
[SAGA] Step 2 complete: Payment charged $599.99
[SAGA] Step 3: Creating shipment to 456 Oak Avenue
[SAGA] FAILURE: Simulated timeout failure at ship step. Starting compensations...
[SAGA] Compensation: Refunding payment...
[SAGA] Compensation complete: Payment refunded
[SAGA] Compensation: Releasing inventory...
[SAGA] Compensation complete: Inventory released
[SAGA] ROLLBACK COMPLETE: All compensations executed for order saga_bob_xxxxx
```

### Scenario 3: Continue-As-New Monitor

Demonstrates workflow history management.

```bash
curl -X POST http://localhost:3009/monitor/start \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "saga_alice_xxxxx",
    "check_interval_seconds": 3,
    "max_checks": 5
  }'
```

**Expected Notifications:**
```
[MONITOR] Iteration 1/5 for order saga_alice_xxxxx
[MONITOR] Order saga_alice_xxxxx status: processing
[MONITOR] Continuing as new - resetting history at iteration 1
[MONITOR] Iteration 2/5 for order saga_alice_xxxxx
[MONITOR] Order saga_alice_xxxxx status: in_transit
...
[MONITOR] Iteration 5/5 for order saga_alice_xxxxx
[MONITOR] Order saga_alice_xxxxx status: delivered
[MONITOR] Monitoring complete for order saga_alice_xxxxx after 5 checks
```

### Scenario 4: Multi-Level Workflows

Demonstrates parent-child-grandchild hierarchy.

```bash
curl -X POST http://localhost:3009/fulfillment/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "Carol",
    "item": "monitor",
    "total": 299.99,
    "destination": "789 Pine Road"
  }'
```

**Expected Notifications:**
```
[FULFILLMENT] Starting fulfillment for order fulfill_carol_xxxxx
[FULFILLMENT] Spawning child workflow: fulfill_carol_xxxxx_validation
[VALIDATION] Starting validation for order fulfill_carol_xxxxx
[VALIDATION] Spawning grandchild workflows in parallel
[ADDRESS CHECK] Validating address for order fulfill_carol_xxxxx
[PAYMENT CHECK] Validating payment for order fulfill_carol_xxxxx
[ADDRESS CHECK] Result: Valid
[PAYMENT CHECK] Result: Valid
[VALIDATION] Address check: True, Payment check: True
[VALIDATION] All validations passed for order fulfill_carol_xxxxx
[FULFILLMENT] Validation passed, executing fulfillment
[FULFILLMENT] Order fulfill_carol_xxxxx fulfilled successfully!
```

---

## Service Integration

The saga-demo service integrates with existing services via Dapr service invocation:

| Target Service | Port | Endpoint | Saga Step |
|----------------|------|----------|-----------|
| inventory | 3002 | `POST /api/v1/inventory/reserve` | Reserve inventory |
| payments | 3003 | `POST /api/v1/payments` | Charge payment |
| payments | 3003 | `POST /api/v1/payments/{id}/refunds` | Refund compensation |
| shipping | 3004 | `POST /shipping/ship` | Create shipment |

---

## Catalyst UI Demonstration Guide

### Preparation
1. Run health check and restock inventory
2. Open notifications UI at `http://localhost:8080`
3. Open Diagrid Catalyst UI for workflow visualization

### Demo Flow (10-15 minutes)

**Part 1: Saga Pattern (5 min)**
1. Submit successful order - watch all steps complete
2. Submit order failing at charge - see single compensation
3. Submit order failing at ship - see full compensation chain
4. Use `force_success` to demonstrate recovery

**Part 2: Continue-As-New (3 min)**
1. Start monitor workflow
2. Watch iterations in Catalyst UI
3. Observe history resets between iterations

**Part 3: Multi-Level Workflows (3 min)**
1. Submit fulfillment order
2. View parent-child-grandchild hierarchy in Catalyst UI
3. Observe parallel grandchild execution

**Part 4: Rerun Demos (2 min)**
1. Run same order 3 times with different failure configs
2. Compare outcomes side-by-side in Catalyst UI

---


### Input-Driven Failure Control

  The saga-demo service allows you to control workflow behavior through request parameters, making demos predictable and repeatable. Instead of relying on random
  failures or external conditions, you specify exactly when and how failures should occur.

  ---
  Parameters
  ┌───────────────────┬────────┬─────────────────────────────────────────────┬─────────────────────────────┐
  │     Parameter     │  Type  │                   Values                    │         Description         │
  ├───────────────────┼────────┼─────────────────────────────────────────────┼─────────────────────────────┤
  │ fail_at_step      │ string │ "reserve", "charge", "ship"                 │ Which step should fail      │
  ├───────────────────┼────────┼─────────────────────────────────────────────┼─────────────────────────────┤
  │ fail_type         │ string │ "timeout", "error", "unavailable", "fatal"  │ What kind of failure        │
  ├───────────────────┼────────┼─────────────────────────────────────────────┼─────────────────────────────┤
  │ simulate_delay_ms │ int    │ 0-5000                                      │ Add delay for visualization │
  ├───────────────────┼────────┼─────────────────────────────────────────────┼─────────────────────────────┤
  │ force_success     │ bool   │ true/false                                  │ Bypass configured failures  │
  └───────────────────┴────────┴─────────────────────────────────────────────┴─────────────────────────────┘

  Note: "fatal" failures mark the workflow as FAILED without compensations, allowing rerun.
  ---
  Usage Examples

  1. Successful Order (No Failure Control)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "Alice",
      "item": "laptop",
      "total": 999.99,
      "destination": "123 Main Street"
    }'
  Result: All 3 steps complete: reserve -> charge -> ship -> SUCCESS

  ---
  2. Fail at Reserve Step (No Compensations)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "Bob",
      "item": "phone",
      "total": 599.99,
      "destination": "456 Oak Avenue",
      "fail_at_step": "reserve",
      "fail_type": "error"
    }'
  Result: Fails immediately at step 1, no compensations needed.

  ---
  3. Fail at Charge Step (1 Compensation)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "Carol",
      "item": "tablet",
      "total": 399.99,
      "destination": "789 Pine Road",
      "fail_at_step": "charge",
      "fail_type": "unavailable",
      "simulate_delay_ms": 1000
    }'
  Result:
  - Step 1 (reserve): SUCCESS
  - Step 2 (charge): FAIL
  - Compensation: release_inventory

  ---
  4. Fail at Ship Step (Full Compensation Chain)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "David",
      "item": "monitor",
      "total": 299.99,
      "destination": "321 Elm Boulevard",
      "fail_at_step": "ship",
      "fail_type": "timeout",
      "simulate_delay_ms": 500
    }'
  Result:
  - Step 1 (reserve): SUCCESS
  - Step 2 (charge): SUCCESS
  - Step 3 (ship): FAIL
  - Compensations (reverse order): refund_payment -> release_inventory

  ---
  5. Force Success (Bypass Failure Config)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "Eve",
      "item": "keyboard",
      "total": 149.99,
      "destination": "555 Tech Lane",
      "fail_at_step": "charge",
      "fail_type": "error",
      "force_success": true
    }'
  Result: Succeeds despite fail_at_step being set. Useful for demonstrating recovery scenarios.

  ---
  6. Fatal Failure (Workflow FAILED, No Compensations)

  curl -X POST http://localhost:3009/saga/orders \
    -H "Content-Type: application/json" \
    -d '{
      "customer": "Frank",
      "item": "monitor",
      "total": 299.99,
      "destination": "777 Crash Lane",
      "fail_at_step": "charge",
      "fail_type": "fatal"
    }'
  Result:
  - Step 1 (reserve): SUCCESS
  - Step 2 (charge): FATAL - workflow terminated
  - No compensations executed
  - Workflow status: FAILED (can be rerun)

  ---
  How It Works (Code Logic)

  The workflow checks the input before each step:

  def should_fail_at_step(order: SagaOrderInput, step: str) -> bool:
      if order.force_success:
          return False  # Bypass all failures
      return order.fail_at_step == step and order.fail_type is not None

  In the workflow:
  # Before each step, check if we should fail
  if should_fail_at_step(order, "reserve"):
      raise Exception(f"Simulated {order.fail_type} failure at reserve step")

  ---
  Checking Results

  After submitting an order, check its status:

  curl http://localhost:3009/saga/orders/{order_id}

  Response shows steps completed and compensations executed:
  {
    "status": "COMPLETED",
    "result": {
      "success": false,
      "message": "Saga rolled back: Simulated timeout failure at ship step",
      "steps_completed": ["reserve", "charge"],
      "compensations_executed": ["refund_payment", "release_inventory"]
    }
  }

  ---
  Demo Script

  The ./run-saga-demo.sh script runs through all these scenarios automatically. Use -q for quick mode:

  ./run-saga-demo.sh      # Full demo (~10-15 min)
  ./run-saga-demo.sh -q   # Quick mode (halves wait times)
  ./run-saga-demo.sh -s   # Skip monitor demo

## Testing

Use the comprehensive test file:

```bash
# VS Code REST Client
code saga-demo.http
```

Test phases included:
1. System Preparation
2. Saga Pattern - Success
3. Saga Pattern - Fail at Reserve
4. Saga Pattern - Fail at Charge
5. Saga Pattern - Fail at Ship
6. Saga Pattern - Force Success
7. Continue-As-New Pattern
8. Multi-Level Workflows
9. Rerun Demos

---

## Dependencies

```
dapr==1.16.0
dapr-ext-workflow==1.16.0
Flask==3.1.1
MarkupSafe==2.1.5
```

---

## Related Documentation

- [Implementation Report](/reports/SAGA_DEMO_IMPLEMENTATION_REPORT.md)
- [Test Scenarios](/saga-demo.http)
- [Project README](/README.md)
