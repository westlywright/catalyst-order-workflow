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
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional, List

# Import resilient runtime wrapper for auto-reconnection
from common.resilient_workflow_runtime import ResilientWorkflowRuntime

APP_PORT = os.getenv("APP_PORT", "3009")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)

# =============================================================================
# DATACLASSES
# =============================================================================

@dataclass
class SagaOrderInput:
    """Input for saga workflow with failure control"""
    id: str
    customer: str
    item: str
    total: float
    destination: str
    fail_at_step: Optional[str] = None      # "reserve", "charge", "ship"
    fail_type: Optional[str] = None         # "timeout", "error", "unavailable"
    simulate_delay_ms: int = 0
    force_success: bool = False


@dataclass
class SagaResult:
    """Result of saga workflow execution"""
    id: str
    success: bool
    message: str
    steps_completed: List[str] = field(default_factory=list)
    compensations_executed: List[str] = field(default_factory=list)
    failure_details: Optional[str] = None


@dataclass
class InventoryResult:
    id: str
    success: bool
    message: str


@dataclass
class PaymentResult:
    id: str
    success: bool
    message: str


@dataclass
class ShipmentResult:
    id: str
    success: bool
    message: str


@dataclass
class CompensationResult:
    step: str
    success: bool
    message: str


# Continue-As-New dataclasses
@dataclass
class MonitorConfig:
    """Configuration for continue-as-new monitoring workflow"""
    order_id: str
    check_interval_seconds: int = 5
    max_checks: int = 10
    current_iteration: int = 0


@dataclass
class MonitorResult:
    """Result of monitoring workflow"""
    order_id: str
    iterations_completed: int
    final_status: str
    message: str


# Multi-Level Workflow dataclasses
@dataclass
class FulfillmentRequest:
    """Parent workflow input"""
    order_id: str
    customer: str
    item: str
    total: float
    destination: str


@dataclass
class FulfillmentResult:
    """Parent workflow result"""
    order_id: str
    success: bool
    message: str
    child_workflows: List[str] = field(default_factory=list)


@dataclass
class ValidationRequest:
    """Child workflow input"""
    order_id: str
    customer: str
    item: str
    total: float
    destination: str


@dataclass
class ValidationResult:
    """Child workflow result"""
    success: bool
    message: str
    address_valid: bool = False
    payment_valid: bool = False


@dataclass
class AddressCheckRequest:
    """Grandchild workflow input"""
    order_id: str
    destination: str


@dataclass
class AddressCheckResult:
    """Grandchild workflow result"""
    valid: bool
    message: str


@dataclass
class PaymentCheckRequest:
    """Grandchild workflow input"""
    order_id: str
    customer: str
    total: float


@dataclass
class PaymentCheckResult:
    """Grandchild workflow result"""
    valid: bool
    message: str


# =============================================================================
# EXCEPTIONS
# =============================================================================

class FatalWorkflowError(Exception):
    """
    Exception for fatal workflow failures that should NOT trigger compensations.
    When raised, the workflow is marked as FAILED and can be rerun.
    Use fail_type="fatal" to trigger this behavior.
    """
    pass


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def should_fail_at_step(order: SagaOrderInput, step: str) -> bool:
    """Check if we should simulate failure at this step"""
    if order.force_success:
        return False
    return order.fail_at_step == step and order.fail_type is not None


def dict_to_saga_input(data) -> SagaOrderInput:
    """Convert dict to SagaOrderInput"""
    if isinstance(data, dict):
        return SagaOrderInput(
            id=data.get('id', ''),
            customer=data.get('customer', ''),
            item=data.get('item', ''),
            total=float(data.get('total', 0)),
            destination=data.get('destination', ''),
            fail_at_step=data.get('fail_at_step'),
            fail_type=data.get('fail_type'),
            simulate_delay_ms=int(data.get('simulate_delay_ms', 0)),
            force_success=bool(data.get('force_success', False))
        )
    return data


# =============================================================================
# SAGA WORKFLOW - Main workflow with compensation pattern
# =============================================================================

def saga_order_workflow(ctx: wf.DaprWorkflowContext, order_input):
    """
    Saga workflow with explicit compensation.
    Steps: Reserve Inventory -> Charge Payment -> Create Shipment
    On failure at any step, execute compensations in reverse order.
    """
    order = dict_to_saga_input(order_input)

    # Track saga state
    inventory_reserved = False
    payment_charged = False
    steps_completed = []
    compensations_executed = []

    yield ctx.call_activity(notify_saga, input=f"[SAGA] Starting saga for order {order.id}")

    # Optional delay for demo visualization
    if order.simulate_delay_ms > 0:
        yield ctx.create_timer(ctx.current_utc_datetime + timedelta(milliseconds=order.simulate_delay_ms))

    try:
        # STEP 1: Reserve Inventory
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 1: Reserving inventory for {order.item}")

        if should_fail_at_step(order, "reserve"):
            if order.fail_type == "fatal":
                raise FatalWorkflowError(f"Fatal failure at reserve step - workflow terminated")
            raise Exception(f"Simulated {order.fail_type} failure at reserve step")

        reserve_result = yield ctx.call_activity(saga_reserve_inventory, input=order)

        if not reserve_result.success:
            raise Exception(f"Inventory reservation failed: {reserve_result.message}")

        inventory_reserved = True
        steps_completed.append("reserve")
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 1 complete: Inventory reserved for {order.item}")

        # STEP 2: Charge Payment
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 2: Charging payment ${order.total}")

        if should_fail_at_step(order, "charge"):
            if order.fail_type == "fatal":
                raise FatalWorkflowError(f"Fatal failure at charge step - workflow terminated")
            raise Exception(f"Simulated {order.fail_type} failure at charge step")

        payment_result = yield ctx.call_activity(saga_charge_payment, input=order)

        if not payment_result.success:
            raise Exception(f"Payment failed: {payment_result.message}")

        payment_charged = True
        steps_completed.append("charge")
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 2 complete: Payment charged ${order.total}")

        # STEP 3: Create Shipment
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 3: Creating shipment to {order.destination}")

        if should_fail_at_step(order, "ship"):
            if order.fail_type == "fatal":
                raise FatalWorkflowError(f"Fatal failure at ship step - workflow terminated")
            raise Exception(f"Simulated {order.fail_type} failure at ship step")

        ship_result = yield ctx.call_activity(saga_create_shipment, input=order)

        if not ship_result.success:
            raise Exception(f"Shipment failed: {ship_result.message}")

        steps_completed.append("ship")
        yield ctx.call_activity(notify_saga, input=f"[SAGA] Step 3 complete: Shipment created to {order.destination}")

        # SUCCESS
        yield ctx.call_activity(notify_saga, input=f"[SAGA] SUCCESS: Order {order.id} completed successfully!")

        return SagaResult(
            id=order.id,
            success=True,
            message="Order processed successfully",
            steps_completed=steps_completed,
            compensations_executed=[]
        )

    except Exception as e:
        # Fatal failures bypass compensations and fail the workflow immediately
        if isinstance(e, FatalWorkflowError):
            yield ctx.call_activity(notify_saga,
                                   input=f"[SAGA] FATAL: {str(e)} - No compensation, workflow marked as FAILED")
            raise

        # FAILURE - Execute compensations in reverse order
        error_msg = str(e)
        yield ctx.call_activity(notify_saga, input=f"[SAGA] FAILURE: {error_msg}. Starting compensations...")

        # Compensate in reverse order
        if payment_charged:
            yield ctx.call_activity(notify_saga, input="[SAGA] Compensation: Refunding payment...")
            yield ctx.call_activity(compensate_refund_payment, input=order)
            compensations_executed.append("refund_payment")
            yield ctx.call_activity(notify_saga, input="[SAGA] Compensation complete: Payment refunded")

        if inventory_reserved:
            yield ctx.call_activity(notify_saga, input="[SAGA] Compensation: Releasing inventory...")
            yield ctx.call_activity(compensate_release_inventory, input=order)
            compensations_executed.append("release_inventory")
            yield ctx.call_activity(notify_saga, input="[SAGA] Compensation complete: Inventory released")

        yield ctx.call_activity(notify_saga,
                               input=f"[SAGA] ROLLBACK COMPLETE: All compensations executed for order {order.id}")

        return SagaResult(
            id=order.id,
            success=False,
            message=f"Saga rolled back: {error_msg}",
            steps_completed=steps_completed,
            compensations_executed=compensations_executed,
            failure_details=error_msg
        )


# =============================================================================
# CONTINUE-AS-NEW WORKFLOW - Demonstrates history management
# =============================================================================

def order_monitor_workflow(ctx: wf.DaprWorkflowContext, config_input):
    """
    Continue-as-new pattern: Monitor an order with periodic checks.
    Demonstrates workflow history management for long-running processes.
    """
    if isinstance(config_input, dict):
        config = MonitorConfig(
            order_id=config_input.get('order_id', ''),
            check_interval_seconds=int(config_input.get('check_interval_seconds', 5)),
            max_checks=int(config_input.get('max_checks', 10)),
            current_iteration=int(config_input.get('current_iteration', 0))
        )
    else:
        config = config_input

    iteration = config.current_iteration + 1

    yield ctx.call_activity(notify_saga,
                           input=f"[MONITOR] Iteration {iteration}/{config.max_checks} for order {config.order_id}")

    # Perform status check
    status = yield ctx.call_activity(check_order_status, input=config.order_id)

    yield ctx.call_activity(notify_saga,
                           input=f"[MONITOR] Order {config.order_id} status: {status}")

    # Check if we've reached max iterations
    if iteration >= config.max_checks:
        yield ctx.call_activity(notify_saga,
                               input=f"[MONITOR] Monitoring complete for order {config.order_id} after {iteration} checks")
        return MonitorResult(
            order_id=config.order_id,
            iterations_completed=iteration,
            final_status=status,
            message=f"Monitoring completed after {iteration} iterations"
        )

    # Wait for next check interval
    yield ctx.create_timer(ctx.current_utc_datetime + timedelta(seconds=config.check_interval_seconds))

    yield ctx.call_activity(notify_saga,
                           input=f"[MONITOR] Continuing as new - resetting history at iteration {iteration}")

    # Continue-as-new: Restart workflow with fresh history
    ctx.continue_as_new(MonitorConfig(
        order_id=config.order_id,
        check_interval_seconds=config.check_interval_seconds,
        max_checks=config.max_checks,
        current_iteration=iteration
    ))


# =============================================================================
# MULTI-LEVEL WORKFLOWS - Parent -> Child -> Grandchild
# =============================================================================

def fulfillment_workflow(ctx: wf.DaprWorkflowContext, request_input):
    """
    Parent workflow: Orchestrates fulfillment through validation child.
    Hierarchy: Fulfillment -> Validation -> (Address Check, Payment Check)
    """
    if isinstance(request_input, dict):
        request = FulfillmentRequest(
            order_id=request_input.get('order_id', ''),
            customer=request_input.get('customer', ''),
            item=request_input.get('item', ''),
            total=float(request_input.get('total', 0)),
            destination=request_input.get('destination', '')
        )
    else:
        request = request_input

    child_workflows = []

    yield ctx.call_activity(notify_saga,
                           input=f"[FULFILLMENT] Starting fulfillment for order {request.order_id}")

    # Spawn CHILD workflow: Validation
    validation_id = f"{request.order_id}_validation"
    child_workflows.append(validation_id)

    yield ctx.call_activity(notify_saga,
                           input=f"[FULFILLMENT] Spawning child workflow: {validation_id}")

    validation_request = ValidationRequest(
        order_id=request.order_id,
        customer=request.customer,
        item=request.item,
        total=request.total,
        destination=request.destination
    )

    validation_result = yield ctx.call_child_workflow(
        validation_workflow,
        input=validation_request,
        instance_id=validation_id
    )

    if not validation_result.success:
        yield ctx.call_activity(notify_saga,
                               input=f"[FULFILLMENT] Validation failed: {validation_result.message}")
        return FulfillmentResult(
            order_id=request.order_id,
            success=False,
            message=f"Validation failed: {validation_result.message}",
            child_workflows=child_workflows
        )

    yield ctx.call_activity(notify_saga,
                           input=f"[FULFILLMENT] Validation passed, executing fulfillment")

    # Execute fulfillment
    yield ctx.call_activity(execute_fulfillment, input=request)

    yield ctx.call_activity(notify_saga,
                           input=f"[FULFILLMENT] Order {request.order_id} fulfilled successfully!")

    return FulfillmentResult(
        order_id=request.order_id,
        success=True,
        message="Fulfillment completed successfully",
        child_workflows=child_workflows
    )


def validation_workflow(ctx: wf.DaprWorkflowContext, request_input):
    """
    Child workflow: Runs parallel grandchild workflows for validation.
    Spawns: Address Check + Payment Check (parallel via when_all)
    """
    if isinstance(request_input, dict):
        request = ValidationRequest(
            order_id=request_input.get('order_id', ''),
            customer=request_input.get('customer', ''),
            item=request_input.get('item', ''),
            total=float(request_input.get('total', 0)),
            destination=request_input.get('destination', '')
        )
    else:
        request = request_input

    yield ctx.call_activity(notify_saga,
                           input=f"[VALIDATION] Starting validation for order {request.order_id}")

    # Prepare grandchild requests
    address_request = AddressCheckRequest(
        order_id=request.order_id,
        destination=request.destination
    )

    payment_request = PaymentCheckRequest(
        order_id=request.order_id,
        customer=request.customer,
        total=request.total
    )

    yield ctx.call_activity(notify_saga,
                           input=f"[VALIDATION] Spawning grandchild workflows in parallel")

    # Spawn GRANDCHILD workflows in parallel
    address_task = ctx.call_child_workflow(
        address_check_workflow,
        input=address_request,
        instance_id=f"{request.order_id}_address_check"
    )

    payment_task = ctx.call_child_workflow(
        payment_check_workflow,
        input=payment_request,
        instance_id=f"{request.order_id}_payment_check"
    )

    # Wait for both grandchildren using when_all
    results = yield wf.when_all([address_task, payment_task])
    address_result, payment_result = results

    yield ctx.call_activity(notify_saga,
                           input=f"[VALIDATION] Address check: {address_result.valid}, Payment check: {payment_result.valid}")

    if not address_result.valid:
        return ValidationResult(
            success=False,
            message=f"Address validation failed: {address_result.message}",
            address_valid=False,
            payment_valid=payment_result.valid
        )

    if not payment_result.valid:
        return ValidationResult(
            success=False,
            message=f"Payment validation failed: {payment_result.message}",
            address_valid=True,
            payment_valid=False
        )

    yield ctx.call_activity(notify_saga,
                           input=f"[VALIDATION] All validations passed for order {request.order_id}")

    return ValidationResult(
        success=True,
        message="All validations passed",
        address_valid=True,
        payment_valid=True
    )


def address_check_workflow(ctx: wf.DaprWorkflowContext, request_input):
    """Grandchild workflow: Validate shipping address"""
    if isinstance(request_input, dict):
        request = AddressCheckRequest(
            order_id=request_input.get('order_id', ''),
            destination=request_input.get('destination', '')
        )
    else:
        request = request_input

    yield ctx.call_activity(notify_saga,
                           input=f"[ADDRESS CHECK] Validating address for order {request.order_id}")

    result = yield ctx.call_activity(validate_address, input=request)

    yield ctx.call_activity(notify_saga,
                           input=f"[ADDRESS CHECK] Result: {'Valid' if result.valid else 'Invalid'}")

    return result


def payment_check_workflow(ctx: wf.DaprWorkflowContext, request_input):
    """Grandchild workflow: Validate payment method"""
    if isinstance(request_input, dict):
        request = PaymentCheckRequest(
            order_id=request_input.get('order_id', ''),
            customer=request_input.get('customer', ''),
            total=float(request_input.get('total', 0))
        )
    else:
        request = request_input

    yield ctx.call_activity(notify_saga,
                           input=f"[PAYMENT CHECK] Validating payment for order {request.order_id}")

    result = yield ctx.call_activity(validate_payment, input=request)

    yield ctx.call_activity(notify_saga,
                           input=f"[PAYMENT CHECK] Result: {'Valid' if result.valid else 'Invalid'}")

    return result


# =============================================================================
# SAGA ACTIVITIES - Forward operations calling existing services
# =============================================================================

def notify_saga(ctx: wf.WorkflowActivityContext, message: str):
    """Send notification for saga events"""
    logging.info(f"Notification: {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": message,
            "data-content-type": "application/json"
        }))


def saga_reserve_inventory(ctx, order_input) -> InventoryResult:
    """Reserve inventory via inventory service"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA] Reserving inventory for order: {order.id}")

    try:
        with DaprClient() as d:
            resp = d.invoke_method(
                "inventory",
                "api/v1/inventory/reserve",
                http_verb="POST",
                data=json.dumps({"id": order.id, "item": order.item})
            )
            if resp.status_code != 200:
                return InventoryResult(order.id, False, f"Inventory service error: {resp.status_code}")
            result = json.loads(resp.data.decode("utf-8"))
            return InventoryResult(
                id=result.get('id', order.id),
                success=result.get('success', False),
                message=result.get('message', '')
            )
    except Exception as e:
        logging.error(f"Error reserving inventory: {e}")
        return InventoryResult(order.id, False, str(e))


def saga_charge_payment(ctx, order_input) -> PaymentResult:
    """Charge payment via payments service"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA] Charging payment for order: {order.id}")

    try:
        with DaprClient() as d:
            resp = d.invoke_method(
                "payments",
                "api/v1/payments",
                http_verb="POST",
                data=json.dumps({
                    "id": order.id,
                    "customer": order.customer,
                    "amount": order.total
                })
            )
            if resp.status_code not in [200, 201]:
                return PaymentResult(order.id, False, f"Payment service error: {resp.status_code}")
            result = json.loads(resp.data.decode("utf-8"))
            return PaymentResult(
                id=result.get('id', order.id),
                success=result.get('success', True),
                message=result.get('message', 'Payment processed')
            )
    except Exception as e:
        logging.error(f"Error charging payment: {e}")
        return PaymentResult(order.id, False, str(e))


def saga_create_shipment(ctx, order_input) -> ShipmentResult:
    """Create shipment via shipping service"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA] Creating shipment for order: {order.id}")

    try:
        with DaprClient() as d:
            resp = d.invoke_method(
                "shipping",
                "shipping/ship",
                http_verb="POST",
                data=json.dumps({
                    "id": order.id,
                    "destination": order.destination
                })
            )
            if resp.status_code != 200:
                return ShipmentResult(order.id, False, f"Shipping service error: {resp.status_code}")
            return ShipmentResult(order.id, True, "Shipment created")
    except Exception as e:
        logging.error(f"Error creating shipment: {e}")
        return ShipmentResult(order.id, False, str(e))


# =============================================================================
# COMPENSATION ACTIVITIES - Rollback operations
# =============================================================================

def compensate_release_inventory(ctx, order_input) -> CompensationResult:
    """Compensation: Release reserved inventory"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA COMPENSATE] Releasing inventory for order: {order.id}")
    # In a real system, would call inventory release endpoint
    return CompensationResult("release_inventory", True, f"Inventory released for {order.item}")


def compensate_refund_payment(ctx, order_input) -> CompensationResult:
    """Compensation: Refund charged payment"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA COMPENSATE] Refunding payment for order: {order.id}")

    try:
        with DaprClient() as d:
            resp = d.invoke_method(
                "payments",
                f"api/v1/payments/{order.id}/refunds",
                http_verb="POST",
                data=json.dumps({
                    "amount": order.total,
                    "reason": "saga_compensation"
                })
            )
            if resp.status_code != 200:
                return CompensationResult("refund_payment", False, f"Refund failed: {resp.status_code}")
            return CompensationResult("refund_payment", True, f"Payment refunded ${order.total}")
    except Exception as e:
        logging.error(f"Error refunding payment: {e}")
        return CompensationResult("refund_payment", False, str(e))


def compensate_cancel_shipment(ctx, order_input) -> CompensationResult:
    """Compensation: Cancel created shipment"""
    order = dict_to_saga_input(order_input)
    logging.info(f"[SAGA COMPENSATE] Canceling shipment for order: {order.id}")
    # In a real system, would call shipping cancel endpoint
    return CompensationResult("cancel_shipment", True, f"Shipment canceled for order {order.id}")


# =============================================================================
# MONITOR/VALIDATION ACTIVITIES
# =============================================================================

def check_order_status(ctx, order_id: str) -> str:
    """Activity to check order status"""
    logging.info(f"[MONITOR] Checking status for order: {order_id}")
    statuses = ["processing", "in_transit", "out_for_delivery", "delivered"]
    return random.choice(statuses)


def validate_address(ctx, request_input) -> AddressCheckResult:
    """Validate shipping address"""
    if isinstance(request_input, dict):
        destination = request_input.get('destination', '')
    else:
        destination = request_input.destination

    logging.info(f"[ADDRESS] Validating address: {destination}")

    # Simple validation: address must have some content
    if destination and len(destination) > 5:
        return AddressCheckResult(True, "Address validated successfully")
    return AddressCheckResult(False, "Invalid address format")


def validate_payment(ctx, request_input) -> PaymentCheckResult:
    """Validate payment method"""
    if isinstance(request_input, dict):
        customer = request_input.get('customer', '')
        total = float(request_input.get('total', 0))
    else:
        customer = request_input.customer
        total = request_input.total

    logging.info(f"[PAYMENT] Validating payment for customer: {customer}, amount: ${total}")

    # Simple validation: customer must exist and total must be positive
    if customer and total > 0:
        return PaymentCheckResult(True, "Payment method validated")
    return PaymentCheckResult(False, "Invalid payment details")


def execute_fulfillment(ctx, request_input):
    """Execute the actual fulfillment after validation"""
    if isinstance(request_input, dict):
        order_id = request_input.get('order_id', '')
    else:
        order_id = request_input.order_id

    logging.info(f"[FULFILLMENT] Executing fulfillment for order: {order_id}")
    return {"status": "fulfilled", "order_id": order_id}


# =============================================================================
# FLASK ENDPOINTS
# =============================================================================

@app.route("/saga/orders", methods=["POST"])
def submit_saga_order():
    """Submit an order to be processed via saga pattern"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request", "message": "Request must be JSON"}), 400

    for field in ["customer", "item", "total", "destination"]:
        if not request_data.get(field):
            return jsonify({"error": "Bad Request", "message": f"Missing required field: {field}"}), 400

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    order_id = f"saga_{request_data['customer'].lower()}_{random_suffix}"

    order = SagaOrderInput(
        id=order_id,
        customer=request_data["customer"],
        item=request_data["item"],
        total=float(request_data["total"]),
        destination=request_data["destination"],
        fail_at_step=request_data.get("fail_at_step"),
        fail_type=request_data.get("fail_type"),
        simulate_delay_ms=int(request_data.get("simulate_delay_ms", 0)),
        force_success=bool(request_data.get("force_success", False))
    )

    wf_client = wf.DaprWorkflowClient()
    instance_id = wf_client.schedule_new_workflow(
        saga_order_workflow,
        input=order,
        instance_id=order_id
    )

    logging.info(f"Started saga workflow: {instance_id}")

    return jsonify({
        "instance_id": instance_id,
        "order_id": order_id,
        "failure_config": {
            "fail_at_step": order.fail_at_step,
            "fail_type": order.fail_type,
            "simulate_delay_ms": order.simulate_delay_ms,
            "force_success": order.force_success
        }
    }), 202


@app.route("/saga/orders/<order_id>", methods=["GET"])
def get_saga_order_status(order_id):
    """Get saga order status"""
    wf_client = wf.DaprWorkflowClient()
    state = wf_client.get_workflow_state(order_id)
    if not state:
        return jsonify({"error": "Not Found", "message": f"Order not found: {order_id}"}), 404

    response = {
        "id": state.instance_id,
        "status": state.runtime_status.name,
        "created_time": state.created_at.isoformat(),
        "last_updated_time": state.last_updated_at.isoformat()
    }

    if state.serialized_output:
        response["result"] = json.loads(state.serialized_output)

    if state.failure_details:
        response["failure_details"] = {
            "message": state.failure_details.message,
            "error_type": state.failure_details.error_type
        }

    return jsonify(response), 200


@app.route("/monitor/start", methods=["POST"])
def start_order_monitor():
    """Start monitoring an order with continue-as-new pattern"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request"}), 400

    order_id = request_data.get("order_id")
    if not order_id:
        return jsonify({"error": "Bad Request", "message": "Missing order_id"}), 400

    config = MonitorConfig(
        order_id=order_id,
        check_interval_seconds=int(request_data.get("check_interval_seconds", 5)),
        max_checks=int(request_data.get("max_checks", 10)),
        current_iteration=0
    )

    monitor_id = f"monitor_{order_id}_{random.randint(1000, 9999)}"
    wf_client = wf.DaprWorkflowClient()
    instance_id = wf_client.schedule_new_workflow(
        order_monitor_workflow,
        input=config,
        instance_id=monitor_id
    )

    logging.info(f"Started monitor workflow: {instance_id}")

    return jsonify({
        "instance_id": instance_id,
        "monitor_id": monitor_id,
        "config": {
            "order_id": config.order_id,
            "check_interval_seconds": config.check_interval_seconds,
            "max_checks": config.max_checks
        }
    }), 202


@app.route("/monitor/<monitor_id>", methods=["GET"])
def get_monitor_status(monitor_id):
    """Get monitor workflow status"""
    wf_client = wf.DaprWorkflowClient()
    state = wf_client.get_workflow_state(monitor_id)
    if not state:
        return jsonify({"error": "Not Found", "message": f"Monitor not found: {monitor_id}"}), 404

    response = {
        "id": state.instance_id,
        "status": state.runtime_status.name,
        "created_time": state.created_at.isoformat(),
        "last_updated_time": state.last_updated_at.isoformat()
    }

    if state.serialized_output:
        response["result"] = json.loads(state.serialized_output)

    return jsonify(response), 200


@app.route("/fulfillment/orders", methods=["POST"])
def submit_fulfillment_order():
    """Submit order for fulfillment (multi-level workflow)"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request"}), 400

    for field in ["customer", "item", "total", "destination"]:
        if not request_data.get(field):
            return jsonify({"error": "Bad Request", "message": f"Missing required field: {field}"}), 400

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    order_id = f"fulfill_{request_data['customer'].lower()}_{random_suffix}"

    fulfillment_request = FulfillmentRequest(
        order_id=order_id,
        customer=request_data["customer"],
        item=request_data["item"],
        total=float(request_data["total"]),
        destination=request_data["destination"]
    )

    wf_client = wf.DaprWorkflowClient()
    instance_id = wf_client.schedule_new_workflow(
        fulfillment_workflow,
        input=fulfillment_request,
        instance_id=order_id
    )

    logging.info(f"Started fulfillment workflow: {instance_id}")

    return jsonify({
        "instance_id": instance_id,
        "order_id": order_id,
        "workflow_hierarchy": [
            f"{order_id} (fulfillment - parent)",
            f"{order_id}_validation (validation - child)",
            f"{order_id}_address_check (address - grandchild)",
            f"{order_id}_payment_check (payment - grandchild)"
        ]
    }), 202


@app.route("/fulfillment/orders/<order_id>", methods=["GET"])
def get_fulfillment_status(order_id):
    """Get fulfillment workflow status"""
    wf_client = wf.DaprWorkflowClient()
    state = wf_client.get_workflow_state(order_id)
    if not state:
        return jsonify({"error": "Not Found", "message": f"Order not found: {order_id}"}), 404

    response = {
        "id": state.instance_id,
        "status": state.runtime_status.name,
        "created_time": state.created_at.isoformat(),
        "last_updated_time": state.last_updated_at.isoformat()
    }

    if state.serialized_output:
        response["result"] = json.loads(state.serialized_output)

    return jsonify(response), 200


@app.route("/health", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "service": "saga-demo",
        "status": "healthy",
        "version": "1.0.0"
    }), 200


# =============================================================================
# MAIN
# =============================================================================

def main():
    logging.info("Starting Saga Demo Service...")

    # Use resilient runtime with auto-reconnection for Diagrid idle timeout handling
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )

    # Register Saga Workflow
    wf_runtime.register_workflow(saga_order_workflow)

    # Register Continue-As-New Workflow
    wf_runtime.register_workflow(order_monitor_workflow)

    # Register Multi-Level Workflows
    wf_runtime.register_workflow(fulfillment_workflow)
    wf_runtime.register_workflow(validation_workflow)
    wf_runtime.register_workflow(address_check_workflow)
    wf_runtime.register_workflow(payment_check_workflow)

    # Register Saga Activities
    wf_runtime.register_activity(notify_saga)
    wf_runtime.register_activity(saga_reserve_inventory)
    wf_runtime.register_activity(saga_charge_payment)
    wf_runtime.register_activity(saga_create_shipment)
    wf_runtime.register_activity(compensate_release_inventory)
    wf_runtime.register_activity(compensate_refund_payment)
    wf_runtime.register_activity(compensate_cancel_shipment)

    # Register Monitor/Validation Activities
    wf_runtime.register_activity(check_order_status)
    wf_runtime.register_activity(validate_address)
    wf_runtime.register_activity(validate_payment)
    wf_runtime.register_activity(execute_fulfillment)

    wf_runtime.start()

    app.run(host='0.0.0.0', port=int(APP_PORT), debug=False, use_reloader=False)

    wf_runtime.shutdown()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    main()
