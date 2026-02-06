# Chaos Engineering & Failure Simulation Guide

A comprehensive guide to environment variables and failure scenarios for resilience testing in the Catalyst Order Workflow system.

## Quick Start

```bash
# Enable chaos detection in order processor (10% random failure)
export ENABLE_CHAOS_DETECTION=true

# Enable chaos mode with 50% failure rate
export ENABLE_CHAOS=true
export FAILURE_RATE=0.5

# Start the system
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

## Environment Variables

### Core Service Configuration

| Variable | Service(s) | Default | Description |
|----------|-----------|---------|-------------|
| `APP_PORT` | All | Service-specific | HTTP port for the service |
| `PUBSUB_NAME` | All Python | `pubsub` | Dapr pub/sub component name |
| `TOPIC_NAME` | All | `notifications` | Notification topic name |
| `STATESTORE_NAME` | inventory | `statestore` | Dapr state store component |

### Chaos Engineering Variables

| Variable | Service | Default | Description |
|----------|---------|---------|-------------|
| `ENABLE_CHAOS` | chaos-engineer | `false` | Master switch for chaos mode |
| `FAILURE_RATE` | chaos-engineer | `0.3` | Base failure probability (0.0-1.0) |
| `ENABLE_CHAOS_DETECTION` | order-processor | `false` | Enable random failure simulation |
| `CHAOS_ENGINEER_URL` | order-processor | `http://localhost:3010` | Chaos service endpoint |

### Order Processing Variables

| Variable | Service | Default | Description |
|----------|---------|---------|-------------|
| `APPROVAL_THRESHOLD` | order-processor | `1000.0` | Order total requiring approval |
| `APPROVAL_TIMEOUT` | order-processor | `24 hours` | Time to wait for approval |

## Failure Types

### Basic Failure Types

| Type | Description | Target Services |
|------|-------------|-----------------|
| `timeout` | Service response delays | payments, shipping |
| `service_unavailable` | Complete service outage | Any service |
| `rate_limited` | API throttling simulation | payments |
| `network_error` | Network connectivity issues | order-processor |
| `database_error` | Database failures | inventory |
| `memory_error` | Memory exhaustion | inventory, shipping |
| `authentication_error` | Auth failures | payments |
| `dependency_failure` | Upstream service failure | Any service |
| `resource_exhausted` | Resource limits hit | Any service |
| `intermittent_error` | Transient failures | Any service |

### Advanced Workflow Failure Types

| Type | Description | Use Case |
|------|-------------|----------|
| `external_event_starvation` | Workflows waiting for events that never arrive | Approval systems, webhooks |
| `child_workflow_zombie` | Child workflows that never complete | Batch processing, fan-out |
| `activity_execution_limbo` | Activities hang indefinitely | External API calls, DB ops |
| `distributed_transaction_failure` | Saga compensation failures | E-commerce, financial txns |

## Circuit Breaker Configuration

The order processor implements circuit breaker patterns for resilience:

```
Circuit Breaker States:
  CLOSED  ──(failure)──▶  track failure count
     │                         │
     │                  (threshold=3)
     │                         │
     ▼                         ▼
  SUCCESS ◀──(timeout)─── OPEN ───▶ fail fast
                            │
                     (1 min timeout)
                            │
                            ▼
                      HALF-OPEN ───▶ test recovery
```

**Configuration:**
- Threshold: 3 consecutive failures opens the circuit
- Timeout: 1 minute before attempting recovery
- Tracked services: inventory, payments, shipping

**Retry Policies per Service:**

| Service | Max Attempts | Base Delay | Multiplier | Notes |
|---------|-------------|------------|------------|-------|
| inventory | 3 | 200ms | 2.0 | Standard backoff |
| shipping | 4 | 300ms | 1.5 | More attempts, slower backoff |
| payments | 2 | 500ms | 2.0 | Fewer retries to avoid double-charge |

## Using Failure Scenarios

### Method 1: Environment Variables (Simple)

Enable random failures in the order processor:

```bash
# Enable 10% random failure rate for chaos testing
export ENABLE_CHAOS_DETECTION=true

# Start services
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

### Method 2: Chaos Engineer API (Advanced)

#### Create a Scenario

```bash
curl -X POST http://localhost:3010/chaos/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Payment Timeout Test",
    "description": "Simulate payment processing delays",
    "failure_type": "timeout",
    "target_service": "payments",
    "failure_rate": 0.7,
    "duration_seconds": 60,
    "enabled": true
  }'
```

#### Execute the Scenario

```bash
# Get the scenario ID from creation response
curl -X POST http://localhost:3010/chaos/scenarios/{scenario_id}/execute
```

#### Quick Injection (No Workflow)

```bash
# Inject immediate failure - 80% failure rate for 30 seconds
curl -X POST http://localhost:3010/chaos/inject/timeout/payments \
  -H "Content-Type: application/json" \
  -d '{"failure_rate": 0.8, "duration_seconds": 30}'
```

### Method 3: Demo Scripts (Automated)

```bash
# Quick demo (3-5 minutes)
./run-chaos-demo.sh

# Comprehensive demo (8-12 minutes)
./run-advanced-chaos-demo.sh

# Advanced workflow failures (15-20 minutes)
./run-advanced-workflow-chaos-demo.sh
```

### Method 4: HTTP Test Files (VS Code REST Client)

- `chaos-demo.http` - Basic chaos scenarios
- `advanced-chaos-demo.http` - Advanced workflow failures

## Common Scenarios

### Scenario 1: Payment Service Timeout

Test retry patterns and circuit breaker behavior:

```bash
# Create scenario
curl -X POST http://localhost:3010/chaos/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Payment Timeout",
    "description": "Test payment retry logic",
    "failure_type": "timeout",
    "target_service": "payments",
    "failure_rate": 0.7,
    "duration_seconds": 90
  }'

# Execute and submit orders to observe behavior
curl -X POST http://localhost:3006/orders \
  -H "Content-Type: application/json" \
  -d '{"customer": "test", "item": "widget", "total": 100}'
```

### Scenario 2: Database Cascade Failure

Test how inventory failures cascade through the system:

```bash
curl -X POST http://localhost:3010/chaos/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Database Cascade",
    "description": "Inventory database failures",
    "failure_type": "database_error",
    "target_service": "inventory",
    "failure_rate": 0.8,
    "duration_seconds": 120
  }'
```

### Scenario 3: External Event Starvation

Test workflows waiting for approvals that never arrive:

```bash
# Create scenario
curl -X POST http://localhost:3010/chaos/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Approval Starvation",
    "description": "Test workflows waiting for external events",
    "failure_type": "external_event_starvation",
    "target_service": "order-processor",
    "failure_rate": 0.9,
    "duration_seconds": 120
  }'

# Submit high-value order requiring approval
curl -X POST http://localhost:3006/orders \
  -H "Content-Type: application/json" \
  -d '{"customer": "test", "item": "expensive", "total": 2500}'
```

### Scenario 4: Child Workflow Zombies

Test batch processing with zombie child workflows:

```bash
curl -X POST http://localhost:3010/chaos/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Zombie Children",
    "description": "Child workflows that never complete",
    "failure_type": "child_workflow_zombie",
    "target_service": "batch-processor",
    "failure_rate": 0.8,
    "duration_seconds": 90
  }'
```

## Monitoring & Diagnostics

### Check System Status

```bash
# Overall chaos status
curl http://localhost:3010/chaos/status

# Circuit breaker states
curl http://localhost:3006/circuit-breakers

# Diagnostic events
curl http://localhost:3010/chaos/events?limit=50

# Filter by severity
curl http://localhost:3010/chaos/events?severity=error&limit=25
```

### Advanced Failure Monitoring

```bash
# All advanced failure states
curl http://localhost:3010/chaos/advanced-failures

# Zombie workflows
curl http://localhost:3010/chaos/zombie-workflows

# Missed external events
curl http://localhost:3010/chaos/missed-events

# Hanging activities
curl http://localhost:3010/chaos/hanging-activities
```

### Event Correlation

Track complete workflow execution using correlation IDs:

```bash
# Get events for specific scenario execution
curl http://localhost:3010/chaos/events?correlation_id={scenario_id}&limit=100
```

## Recovery Procedures

### Automatic Recovery

- Circuit breakers reset after 1-minute timeout
- Failure scenarios expire based on `duration_seconds`
- System health recovers automatically post-expiration

### Manual Recovery

Simulate recovery actions for advanced failures:

```bash
# Recover from external event starvation
curl -X POST http://localhost:3010/chaos/advanced-failures/{workflow_id}/recover

# This simulates:
# - Manual event injection
# - Zombie child termination
# - Hanging activity cleanup
```

## Combining Env Vars and Scenarios

### Development Testing

```bash
# Light chaos for development
export ENABLE_CHAOS_DETECTION=true  # 10% random failures
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

### Integration Testing

```bash
# Enable base chaos, then layer scenarios
export ENABLE_CHAOS=true
export FAILURE_RATE=0.2  # 20% base rate

# Start services, then add targeted scenarios via API
curl -X POST http://localhost:3010/chaos/inject/timeout/payments \
  -d '{"failure_rate": 0.5, "duration_seconds": 60}'
```

### Stress Testing

```bash
# High failure rate for stress testing
export ENABLE_CHAOS=true
export FAILURE_RATE=0.7  # 70% failures

# Run multiple concurrent scenarios
# See chaos-demo.http for multi-scenario examples
```

## API Reference

### Chaos Scenarios

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chaos/scenarios` | POST | Create scenario |
| `/chaos/scenarios` | GET | List all scenarios |
| `/chaos/scenarios/{id}` | GET | Get scenario details |
| `/chaos/scenarios/{id}/execute` | POST | Execute scenario |

### Quick Injection

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chaos/inject/{type}/{service}` | POST | Quick failure injection |

### Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chaos/status` | GET | Overall system status |
| `/chaos/events` | GET | Diagnostic events (filterable) |
| `/chaos/advanced-failures` | GET | Advanced failure states |
| `/chaos/zombie-workflows` | GET | Zombie workflow info |
| `/chaos/missed-events` | GET | Missed external events |
| `/chaos/hanging-activities` | GET | Hanging activities by service |

### Recovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chaos/advanced-failures/{id}/recover` | POST | Simulate recovery |

## Best Practices

1. **Start Small**: Begin with `ENABLE_CHAOS_DETECTION=true` (10% failures)
2. **Monitor First**: Check `/chaos/status` and `/circuit-breakers` before scenarios
3. **Use Durations**: Set reasonable `duration_seconds` to auto-expire scenarios
4. **Layer Scenarios**: Combine env vars (base rate) with API scenarios (targeted)
5. **Track Correlation**: Use correlation IDs for end-to-end tracing
6. **Watch Circuit Breakers**: Monitor state transitions during testing
7. **Clean Up**: Scenarios auto-expire, but verify with `/chaos/status`

## Related Documentation

- [Main README](../README.md) - Project overview
- [AGENT_WORKFLOW.md](./AGENT_WORKFLOW.md) - Agent workflow patterns
- `chaos-demo.http` - Interactive HTTP test scenarios
- `advanced-chaos-demo.http` - Advanced workflow failure demos
