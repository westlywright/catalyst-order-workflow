# Catalyst Order Processing Workflow

This solution demonstrates the capabilities provided by all five Catalyst APIs through a python-based order processing workflow. The end-to-end solution is comprised of five services:

- **order-processor**: Contains the order process workflow definition and all associated activity methods which will be executed as part of the workflow sequence using the Catalyst Workflow API.
- **batch-processor**: Handles bulk orders by implementing parent workflows that spawn child workflows for each item, demonstrating advanced workflow patterns and parallel processing.
- **inventory**: Receives direct invocation requests sent by the order-processor using the Invocation API to manage inventory state in the Diagrid KV Store through the Catalyst State API.
- **notifications**: Subscribes to messages published by the order-processor using the Pub/Sub API and subsequently displays those messages through a simple JavaScript user interface.
- **shipping**: Receives direct invocation requests sent by the order-processor using the Invocation API to simulate the scheduling of order shipments.
- **payments**: Receives direct invocation requests sent by the order-processor using the Invocation API to mock the processing of order payments.
- **returns**: Demonstrates workflow chaining and advanced state management through return processing workflows that reference original orders, utilize child workflows for different return types (defective, standard, expedited), and implement external event handling for manager approvals.
- **chaos-engineer**: Advanced failure simulation and debugging service that demonstrates resilience patterns including retry logic with exponential backoff, circuit breaker patterns, cascading failure scenarios, and rich diagnostic event generation for dashboard consumption. Creates comprehensive failure scenarios to test workflow debugging and monitoring capabilities.

## Prerequisites
- [Sign up](https://catalyst.diagrid.io) for Diagrid Catalyst
- Install latest [Diagrid CLI](https://docs.diagrid.io/catalyst/references/cli-reference/intro#installing-the-cli)
- Install [Python3](https://www.python.org/downloads/)
- Install [Node.js](https://nodejs.org/) (version 20 or higher) and npm

### Prepare applications

The build apps file will go through each application directory and run any app commands necessary to prepare the applications to run. Make sure it is executable using the below command:

```bash
chmod +X build-apps.sh
```

Run the script:

```bash
./build-apps.sh
```

## Deploy Catalyst resources

Replace `unique-project-name` with a name for your workflow project

```bash
export WORKFLOW_PROJECT_NAME="unique-project-name"
```

Execute the following command to run your applications locally and create the dependent Catalyst resources:

```bash
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

## Use the APIs

### Testing Files

Two comprehensive testing files are available at the root of this repository for use with the VS Code `Rest Client` extension:

- **`test-commands.http`**: Basic workflow testing including orders, bulk orders, returns, and circuit breaker monitoring
- **`chaos-demo.http`**: Comprehensive chaos engineering demonstration script with 8 phases of failure simulation, perfect for showcasing dashboard debugging capabilities

    ![Rest Client](/images/rest-client.png)

## Bulk Order Processing (Child Workflows)

The application now includes advanced workflow patterns with **parent-child workflows** via the `batch-processor` service:

### Features:
- **Parent Workflow**: Processes bulk orders containing multiple items
- **Child Workflows**: Each item spawns its own workflow for parallel processing
- **Real-time Notifications**: Track progress of both parent and child workflows
- **Failure Handling**: Graceful handling of partial failures in bulk orders
- **Clear Activity Names**: Descriptive activity names for easy workflow visualization in Catalyst dashboards

### Example Bulk Order Request:
```json
POST http://localhost:3007/bulk-orders
Content-Type: application/json

{
  "customer": "alice",
  "items": [
    {"item": "apple", "quantity": 2, "price": 50.0},
    {"item": "orange", "quantity": 1, "price": 75.0},
    {"item": "pear", "quantity": 3, "price": 30.0}
  ]
}
```

### Check Bulk Order Status:
```http
GET http://localhost:3007/bulk-orders/{instance_id}
```

This demonstrates how Dapr workflows can orchestrate complex business processes using parent-child relationships, making it perfect for scenarios like:
- Multi-item order processing
- Batch operations
- Parallel task execution
- Coordinated microservice interactions

### Improved Activity Naming for Workflow Visualization

Both `batch-processor` and `returns` services use **descriptive, stage-specific activity names** that make workflow diagrams in Catalyst much easier to follow:

#### Batch Processing Activities:
- `announce_bulk_order_started` → Clear workflow initiation
- `announce_child_workflow_spawned` → Track child workflow creation
- `announce_waiting_for_children` → Parent workflow coordination point
- `announce_item_success` / `announce_item_failure` → Individual item outcomes
- `announce_inventory_reserved` → Business logic completion
- `announce_payment_processing` → Payment stage identification
- `announce_shipping_scheduled` → Final fulfillment step

#### Returns Processing Activities:
- `announce_return_request_received` → Return workflow entry point
- `announce_return_validation_started` → Eligibility checking
- `announce_return_approval_required` → High-value return handling
- `announce_return_child_workflow_spawned` → Type-specific processing
- `announce_defective_return_started` → Defective item workflow
- `announce_standard_refund_processing` → Standard return path
- `announce_expedited_parallel_processing` → Fast-track processing

**Previous Problem**: Generic activity names like `notify_bulk` and `notify_return` were used repeatedly, making workflow diagrams unclear.

**Solution**: Each workflow stage now has a specific, descriptive activity name that clearly indicates its purpose in the business process, making Catalyst workflow visualizations much more informative for developers.

#### Chaos Engineering Activities:
- `announce_chaos_workflow_started` → Clear workflow entry point
- `announce_baseline_health_check_started` → Pre-failure assessment
- `announce_failure_injection_started` → Chaos injection phase
- `announce_resilience_test_round_started` → Retry policy testing
- `announce_circuit_breaker_test_started` → Circuit breaker validation
- `announce_cascade_failure_test_started` → Cascade failure testing
- `announce_recovery_test_started` → System recovery testing
- `execute_retry_policy_test` → Specific retry strategy execution
- `execute_circuit_breaker_test` → Circuit breaker pattern execution
- `execute_cascade_failure_simulation` → Cascade failure execution
- `execute_system_recovery_test` → Recovery procedure execution

**Previous Problem**: Generic activity names like `emit_diagnostic_event` were used 8+ times and activities like `test_service_with_retries` were unclear about their purpose.

**Solution**: Each chaos engineering phase now has distinct activities that clearly indicate the testing stage and purpose, making workflow debugging much more effective.

#### Best Practices for Activity Naming:
1. **Use Action Verbs**: `announce_`, `validate_`, `process_`, `submit_`, `execute_`
2. **Include Context**: `_bulk_order_`, `_return_`, `_payment_`, `_inventory_`, `_chaos_`, `_failure_`
3. **Indicate Stage**: `_started`, `_completed`, `_failed`, `_required`, `_test_`, `_simulation`
4. **Avoid Generic Names**: Instead of `notify` or `process`, use specific names like `announce_approval_received`
5. **Group Related Activities**: Use consistent prefixes (`announce_defective_*`, `announce_standard_*`, `execute_*_test`)

### Summary of Activity Naming Improvements

All three advanced workflow services now follow consistent, descriptive naming patterns:

| **Service** | **Before** | **After** | **Benefit** |
|-------------|------------|-----------|-------------|
| **Batch Processor** | `notify_bulk` (15+ times) | `announce_bulk_order_started`, `announce_child_workflow_spawned`, etc. | Clear parent/child workflow stages |
| **Returns Service** | `notify_return` (20+ times) | `announce_return_request_received`, `announce_defective_return_started`, etc. | Distinct return type processing |
| **Chaos Engineer** | `emit_diagnostic_event` (8+ times) | `announce_failure_injection_started`, `execute_retry_policy_test`, etc. | Clear chaos testing phases |

**Impact**: Your Catalyst workflow diagrams now tell a clear story of your business processes, making debugging, monitoring, and onboarding significantly easier for development teams.

## Return Workflows (Workflow Chaining & State Management)

The application now includes **Return Workflows** via the `returns` service, showcasing **workflow chaining** and advanced **state management** patterns:

### Architecture:
- **Main Return Workflow**: Orchestrates the entire return process with multiple validation and processing steps
- **Child Workflows**: Specialized processing based on return type:
  - **Defective Returns**: Full refund, no restocking (item disposed)
  - **Standard Returns**: Sequential refund + inventory restocking
  - **Expedited Returns**: Parallel processing for faster completion
- **External Events**: Manager approval system for high-value returns (>$500)
- **State Management**: Comprehensive tracking through validation → approval → processing → completion

### Key Features:
- **Workflow Chaining**: Returns reference and validate against original orders
- **Dynamic Child Workflows**: Different processing paths based on return reason
- **External Event Handling**: 24-hour approval timeouts with automatic rejection
- **Parallel Processing**: Expedited returns handle refund + restocking simultaneously
- **Real-time Notifications**: Live progress updates with `[RETURN]` prefix
- **Comprehensive Validation**: Time-based eligibility, value thresholds, and business rules

### Example Return Requests:

**Standard Return:**
```json
POST http://localhost:3008/returns
Content-Type: application/json

{
  "original_order_id": "order_john_abc123",
  "customer": "john",
  "item": "apple",
  "reason": "wrong_size",
  "description": "Item was too small",
  "return_value": 75.0
}
```

**Defective Item Return:**
```json
POST http://localhost:3008/returns
Content-Type: application/json

{
  "original_order_id": "order_sarah_xyz789",
  "customer": "sarah",
  "item": "orange",
  "reason": "defective",
  "description": "Item arrived damaged",
  "return_value": 45.0
}
```

**High-Value Return (Requires Approval):**
```json
POST http://localhost:3008/returns
Content-Type: application/json

{
  "original_order_id": "order_alice_def456",
  "customer": "alice",
  "item": "kiwi",
  "reason": "not_as_described",
  "description": "Product quality not as expected",
  "return_value": 850.0
}
```

### Check Return Status:
```http
GET http://localhost:3008/returns/{return_id}
```

### Approve High-Value Return:
```json
POST http://localhost:3008/returns/{return_id}/approve
Content-Type: application/json

{
  "approver": "manager_jane",
  "approved": true
}
```

Return workflows demonstrate advanced Dapr patterns including:
- **Workflow Chaining**: Connecting return processes to original order data
- **State Management**: Multi-step state transitions with persistence
- **Event-Driven Approvals**: External events with timeouts and fallbacks
- **Parallel Execution**: Concurrent activities for performance optimization
- **Business Logic Orchestration**: Complex decision trees and compensation patterns

## Chaos Engineering & Failure Simulation (Enhanced Debugging)

The application now includes **Chaos Engineering** capabilities via the `chaos-engineer` service, specifically designed to demonstrate advanced **workflow debugging and monitoring** for dashboard interfaces. The service has been enhanced with **descriptive, phase-specific activity names** for crystal-clear workflow visualization:

### Architecture:
- **Chaos Resilience Workflows**: Complex workflows that inject failures and test system resilience patterns
- **Failure Injection Engine**: Configurable failure scenarios targeting specific services
- **Diagnostic Event Generation**: Rich, structured events perfect for dashboard consumption
- **Enhanced Service Resilience**: Existing services upgraded with circuit breaker and retry patterns

### Failure Types Supported:
- **timeout**: Service response timeouts
- **service_unavailable**: Service downtime simulation
- **rate_limited**: Rate limiting and throttling scenarios
- **network_error**: Network connectivity issues
- **database_error**: Database connection/query failures
- **memory_error**: Out of memory conditions
- **authentication_error**: Auth and permission failures
- **dependency_failure**: Downstream service failures
- **resource_exhausted**: Resource pool exhaustion
- **intermittent_error**: Random transient failures

### Key Features:

**🎯 Chaos Scenarios**: Create comprehensive failure scenarios that run workflows demonstrating:
- Pre-failure system health assessments
- Controlled failure injection with configurable rates and duration
- Resilience testing with multiple retry policies (exponential backoff, fixed interval, linear backoff)
- Circuit breaker triggering and recovery patterns
- Cascade failure containment testing
- System recovery validation
- Post-failure health comparison

**📊 Dashboard-Ready Events**: All diagnostic events include:
- **Correlation IDs** for end-to-end tracing
- **Severity Levels** (INFO, WARNING, ERROR, CRITICAL)
- **Execution Times** and retry counts
- **Rich Context** for debugging (service details, failure types, retry attempts)
- **Real-time Notifications** via pub/sub for live dashboard updates

**🔧 Enhanced Service Resilience**: The `order-processor` service demonstrates production-ready patterns:
- **Circuit Breaker Implementation** for inventory, payments, and shipping services
- **Configurable Retry Logic** with exponential backoff and jitter
- **Failure Detection and Recording** with automatic recovery
- **Circuit Breaker Status API** for real-time monitoring

### Example Chaos Scenarios:

**Create Payment Timeout Scenario:**
```json
POST http://localhost:3010/chaos/scenarios
Content-Type: application/json

{
  "name": "Payment Service Timeout",
  "description": "Simulate timeout failures in payment processing",
  "failure_type": "timeout",
  "target_service": "payments",
  "failure_rate": 0.7,
  "duration_seconds": 45,
  "enabled": true
}
```

**Execute Chaos Scenario:**
```http
POST http://localhost:3010/chaos/scenarios/{scenario_id}/execute
```

**Quick Failure Injection:**
```json
POST http://localhost:3010/chaos/inject/network_error/order-processor
Content-Type: application/json

{
  "failure_rate": 0.8,
  "duration_seconds": 20
}
```

**Monitor Circuit Breakers:**
```http
GET http://localhost:3006/circuit-breakers
```

**Get Diagnostic Events (Dashboard Data):**
```http
GET http://localhost:3010/chaos/events?limit=50&severity=error
```

### Dashboard Integration:
The chaos engineering service generates structured diagnostic events perfect for workflow debugging dashboards:

```json
{
  "id": "evt_12345",
  "timestamp": "2024-01-15T10:30:00Z",
  "severity": "error",
  "service": "order-processor",
  "workflow_id": "order_alice_abc123",
  "event_type": "retry_attempt",
  "message": "Payment service timeout - retrying with exponential backoff",
  "details": {
    "retry_attempt": 2,
    "delay_ms": 400,
    "failure_type": "timeout",
    "target_service": "payments"
  },
  "correlation_id": "chaos_scenario_payment_timeout_1234",
  "retry_count": 2,
  "execution_time_ms": 1250
}
```

### Comprehensive Chaos Demo Script

The `chaos-demo.http` file provides a **professional-grade demonstration script** with 8 distinct phases:

1. **Baseline System Health Assessment** - Pre-failure service verification
2. **Scenario Creation & Configuration** - Multiple failure type setup
3. **Workflow Execution & Monitoring** - Live chaos scenario orchestration
4. **Live System Stress Testing** - Real order processing during failures
5. **Quick Failure Injection Tests** - Immediate failure simulation
6. **Real-Time Monitoring & Diagnostics** - Dashboard data consumption
7. **Correlation & Tracing Analysis** - End-to-end workflow tracking
8. **Advanced Failure Scenarios** - Complex multi-service testing

**Key Dashboard Debugging Features:**
- **10 Different Monitoring Endpoints**: From health checks to detailed diagnostic events
- **Correlation ID Tracking**: Complete end-to-end workflow visibility
- **Severity-Based Filtering**: INFO, WARNING, ERROR, CRITICAL event streams
- **Rich Contextual Data**: Execution times, retry patterns, cascade effects
- **Real-Time Updates**: Live pub/sub integration for instant dashboard updates

**Demo Duration**: 10-15 minutes for complete professional demonstration
**Event Volume**: 20-50 diagnostic events per minute during active chaos
**Concurrent Scenarios**: Up to 4 failure scenarios running simultaneously

This comprehensive chaos engineering setup provides the perfect foundation for demonstrating:
- **Workflow Debugging**: Rich diagnostic data for identifying failure patterns
- **Resilience Monitoring**: Real-time visibility into retry attempts and circuit breaker states
- **Performance Analysis**: Execution times and failure correlation
- **System Health**: Service dependencies and cascade failure visualization
- **Recovery Tracking**: End-to-end failure and recovery lifecycle monitoring

### Circuit Breaker Testing Workflow

The `test-commands.http` file includes an enhanced circuit breaker testing section that demonstrates:

- **Baseline Monitoring**: Check circuit breaker states before failures
- **Stress Testing**: Submit orders during active chaos scenarios
- **Real-time Monitoring**: Watch circuit breaker state transitions (closed → open → half-open)
- **Protection Verification**: Observe how circuit breakers prevent cascade failures

**Recommended Testing Flow:**

1. Check baseline circuit breaker status: `GET http://localhost:3006/circuit-breakers`
2. Start chaos scenarios from `chaos-demo.http`
3. Submit test orders to trigger circuit breaker protection
4. Monitor state changes in real-time

