# Saga Demo Service Implementation Report

**Date:** 2026-01-22
**Feature:** Advanced Workflow Patterns for Diagrid Catalyst UI Demos
**Service:** saga-demo (Port 3009)

---

## Executive Summary

Implemented a new `saga-demo` service demonstrating advanced Dapr 1.16 workflow patterns with input-driven failure control for repeatable demonstrations. The service showcases saga pattern with compensation, continue-as-new for history management, and multi-level parent-child-grandchild workflow hierarchies.

---

## Requirements

The user requested:
1. Advanced workflow patterns focusing on child/sub-workflow patterns
2. Rerunnable workflows for showcasing in Diagrid Catalyst UI
3. Input-driven failures and successes for demo control
4. Multi-app workflows calling existing services
5. KISS compliant implementation

---

## Implementation Details

### Files Created

#### 1. `services/saga-demo/app.py` (750+ lines)

Main service file containing:

**Dataclasses (14 total):**
- `SagaOrderInput` - Saga workflow input with failure control fields
- `SagaResult` - Saga execution result with compensation tracking
- `InventoryResult`, `PaymentResult`, `ShipmentResult` - Service call results
- `CompensationResult` - Compensation activity result
- `MonitorConfig`, `MonitorResult` - Continue-as-new configuration
- `FulfillmentRequest`, `FulfillmentResult` - Parent workflow types
- `ValidationRequest`, `ValidationResult` - Child workflow types
- `AddressCheckRequest`, `AddressCheckResult` - Grandchild workflow types
- `PaymentCheckRequest`, `PaymentCheckResult` - Grandchild workflow types

**Workflows (6 total):**

| Workflow | Type | Purpose |
|----------|------|---------|
| `saga_order_workflow` | Main | Saga pattern with compensation |
| `order_monitor_workflow` | Monitor | Continue-as-new pattern |
| `fulfillment_workflow` | Parent | Multi-level orchestration |
| `validation_workflow` | Child | Spawns grandchildren |
| `address_check_workflow` | Grandchild | Parallel address validation |
| `payment_check_workflow` | Grandchild | Parallel payment validation |

**Activities (12 total):**

| Activity | Category | Purpose |
|----------|----------|---------|
| `notify_saga` | Notification | Pub/sub event publishing |
| `saga_reserve_inventory` | Forward | Calls inventory service |
| `saga_charge_payment` | Forward | Calls payments service |
| `saga_create_shipment` | Forward | Calls shipping service |
| `compensate_release_inventory` | Compensation | Rollback inventory |
| `compensate_refund_payment` | Compensation | Calls payments refund endpoint |
| `compensate_cancel_shipment` | Compensation | Rollback shipment |
| `check_order_status` | Monitor | Status check for continue-as-new |
| `validate_address` | Validation | Address validation logic |
| `validate_payment` | Validation | Payment validation logic |
| `execute_fulfillment` | Fulfillment | Final fulfillment execution |

**Flask Endpoints (8 total):**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `POST /saga/orders` | Submit saga order with failure config |
| `GET /saga/orders/<id>` | Get saga order status |
| `POST /monitor/start` | Start continue-as-new monitor |
| `GET /monitor/<id>` | Get monitor status |
| `POST /fulfillment/orders` | Submit multi-level workflow |
| `GET /fulfillment/orders/<id>` | Get fulfillment status |
| `GET /health` | Health check |
| `GET /healthz` | Health check (alternate) |

#### 2. `services/saga-demo/requirements.txt`

```
dapr==1.16.0
dapr-ext-workflow==1.16.0
Flask==3.1.1
MarkupSafe==2.1.5
```

#### 3. `saga-demo.http` (300+ lines)

Comprehensive test file with 9 phases:
1. System Preparation
2. Saga Pattern - Successful Order
3. Saga Pattern - Failure at RESERVE Step
4. Saga Pattern - Failure at CHARGE Step
5. Saga Pattern - Failure at SHIP Step
6. Saga Pattern - Force Success
7. Continue-As-New Pattern
8. Multi-Level Workflows
9. Rerun Demos

---

### Files Modified

#### 1. `dapr.yaml`

Added saga-demo service configuration:
```yaml
- appID: saga-demo
  appPort: 3009
  appDirPath: ./services/saga-demo
  command: ["python3", "app.py"]
  enableAppHealthCheck: true
  appHealthCheckPath: /healthz
  appHealthProbeInterval: 10
  appHealthProbeTimeout: 2000
  appHealthThreshold: 3
```

#### 2. `build-apps.sh`

Added saga-demo dependency installation:
```bash
cd ../saga-demo
pip3 install -r requirements.txt
```

#### 3. `test-commands.http`

Added reference to saga-demo.http in advanced demos section.

---

## Pattern Implementations

### 1. Saga Pattern with Explicit Compensation

**Flow:**
```
SUCCESS PATH:
  reserve_inventory ✓ → charge_payment ✓ → create_shipment ✓ → SUCCESS

FAILURE AT SHIP (compensation in reverse):
  reserve_inventory ✓ → charge_payment ✓ → create_shipment ✗
                                        ↓
  COMPENSATE: refund_payment → release_inventory → ROLLBACK COMPLETE
```

**Implementation Details:**
- Boolean flags track completed steps (`inventory_reserved`, `payment_charged`)
- On exception, compensations execute in reverse order
- Each compensation is a separate activity for visibility
- All steps emit `[SAGA]` prefixed notifications

### 2. Input-Driven Failure Control

**SagaOrderInput Fields:**
```python
@dataclass
class SagaOrderInput:
    id: str
    customer: str
    item: str
    total: float
    destination: str
    # Failure control
    fail_at_step: Optional[str] = None   # "reserve", "charge", "ship"
    fail_type: Optional[str] = None      # "timeout", "error", "unavailable"
    simulate_delay_ms: int = 0           # Slow execution for demos
    force_success: bool = False          # Bypass failures
```

**Usage Examples:**
```json
// Fail at charge step
{"fail_at_step": "charge", "fail_type": "error"}

// Force success despite config
{"fail_at_step": "charge", "fail_type": "error", "force_success": true}

// Add delay for visualization
{"simulate_delay_ms": 1000}
```

### 3. Continue-As-New Pattern

**Purpose:** Demonstrates workflow history management for long-running processes.

**Implementation:**
```python
def order_monitor_workflow(ctx, config):
    # Perform iteration
    yield ctx.call_activity(notify_saga, input=f"Iteration {iteration}")
    status = yield ctx.call_activity(check_order_status, input=config.order_id)

    # Wait for next interval
    yield ctx.create_timer(ctx.current_utc_datetime + timedelta(seconds=interval))

    # Continue-as-new: restart with fresh history
    ctx.continue_as_new(MonitorConfig(
        order_id=config.order_id,
        current_iteration=iteration
    ))
```

**Benefits:**
- Prevents unbounded history growth
- Each iteration starts with clean history
- State preserved in config dataclass

### 4. Multi-Level Workflow Hierarchy

**Structure:**
```
fulfillment_workflow (Parent)
├── validation_workflow (Child)
│   ├── address_check_workflow (Grandchild) ─┐
│   └── payment_check_workflow (Grandchild) ─┼─ parallel via when_all
└── execute_fulfillment (Activity)
```

**Implementation:**
```python
# Parent spawns child
validation_result = yield ctx.call_child_workflow(
    validation_workflow,
    input=validation_request,
    instance_id=f"{order_id}_validation"
)

# Child spawns grandchildren in parallel
address_task = ctx.call_child_workflow(address_check_workflow, ...)
payment_task = ctx.call_child_workflow(payment_check_workflow, ...)
results = yield wf.when_all([address_task, payment_task])
```

**Workflow IDs Generated:**
- `fulfill_frank_abc12` (parent)
- `fulfill_frank_abc12_validation` (child)
- `fulfill_frank_abc12_address_check` (grandchild)
- `fulfill_frank_abc12_payment_check` (grandchild)

---

## Service Integration

The saga-demo service integrates with existing services via Dapr service invocation:

| Target Service | Endpoint | Usage |
|----------------|----------|-------|
| inventory (3002) | `POST /api/v1/inventory/reserve` | Reserve inventory step |
| payments (3003) | `POST /api/v1/payments` | Charge payment step |
| payments (3003) | `POST /api/v1/payments/{id}/refunds` | Refund compensation |
| shipping (3004) | `POST /shipping/ship` | Create shipment step |

---

## Testing Guide

### Quick Start
```bash
# Install dependencies
cd services/saga-demo && pip3 install -r requirements.txt

# Start all services
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME

# Test saga success
curl -X POST http://localhost:3009/saga/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"Alice","item":"laptop","total":999.99,"destination":"123 Main St"}'
```

### Demo Scenarios

**Scenario 1: Saga Success**
```bash
curl -X POST http://localhost:3009/saga/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"Alice","item":"laptop","total":999.99,"destination":"123 Main St"}'
```

**Scenario 2: Saga Failure with Compensation**
```bash
curl -X POST http://localhost:3009/saga/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"Bob","item":"phone","total":599.99,"destination":"456 Oak","fail_at_step":"ship","fail_type":"error"}'
```

**Scenario 3: Continue-As-New Monitor**
```bash
curl -X POST http://localhost:3009/monitor/start \
  -H "Content-Type: application/json" \
  -d '{"order_id":"saga_alice_xxxxx","check_interval_seconds":3,"max_checks":5}'
```

**Scenario 4: Multi-Level Workflows**
```bash
curl -X POST http://localhost:3009/fulfillment/orders \
  -H "Content-Type: application/json" \
  -d '{"customer":"David","item":"monitor","total":299.99,"destination":"321 Elm"}'
```

---

## Catalyst UI Demonstration Points

1. **Saga Compensation Visibility**
   - Watch workflow steps execute in sequence
   - See compensation activities fire on failure
   - Compare successful vs. failed saga outcomes

2. **Rerunnable Workflows**
   - Run same order with different `fail_at_step` values
   - Use `force_success` to demonstrate recovery
   - Show deterministic behavior based on inputs

3. **Workflow Hierarchy**
   - View parent-child-grandchild relationships
   - See parallel grandchild execution via `when_all`
   - Track workflow IDs through the hierarchy

4. **Continue-As-New History Management**
   - Monitor iteration counter incrementing
   - Observe history reset between iterations
   - Demonstrate long-running workflow patterns

---

## Architecture Alignment

The implementation follows existing codebase patterns:

| Pattern | Source Reference | Implementation |
|---------|------------------|----------------|
| Dataclasses | `order-processor/app.py:38-73` | All input/output types |
| Workflow registration | `order-processor/app.py:413-423` | `main()` function |
| Service invocation | `order-processor/app.py:234-288` | Activity functions |
| Pub/sub notifications | `order-processor/app.py:224-231` | `notify_saga()` |
| Flask routes | `order-processor/app.py:291-386` | All endpoints |
| Health checks | `order-processor/app.py:388-391` | `/healthz` endpoint |
| Child workflows | `batch-processor/app.py:130-135` | Multi-level workflows |
| Parallel execution | `returns/app.py` | `when_all` pattern |

---

## File Summary

| File | Lines | Status |
|------|-------|--------|
| `services/saga-demo/app.py` | ~750 | Created |
| `services/saga-demo/requirements.txt` | 4 | Created |
| `saga-demo.http` | ~300 | Created |
| `dapr.yaml` | +9 | Modified |
| `build-apps.sh` | +3 | Modified |
| `test-commands.http` | +2 | Modified |

---

## Conclusion

The saga-demo service successfully implements all requested advanced workflow patterns:

1. **Saga Pattern** - Full compensation chain with explicit rollback steps
2. **Input-Driven Failures** - Deterministic failure injection for repeatable demos
3. **Continue-As-New** - History management for long-running workflows
4. **Multi-Level Workflows** - Parent → Child → Grandchild hierarchy
5. **Multi-App Integration** - Calls existing inventory, payments, shipping services

The implementation is KISS compliant, follows existing codebase conventions, and provides comprehensive demo scenarios for showcasing Diagrid Catalyst UI workflow capabilities.
