import json
import logging
import os
import random
import string
import time
import dapr.ext.workflow as wf
from dapr.clients import DaprClient
from flask import Flask, request, url_for
from markupsafe import escape
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

APP_PORT = os.getenv("APP_PORT", "3006")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

APPROVAL_THRESHOLD = 1000.0
APPROVAL_TIMEOUT = timedelta(hours=24)

# Chaos engineering configuration
ENABLE_CHAOS_DETECTION = os.getenv("ENABLE_CHAOS_DETECTION", "false").lower() == "true"
CHAOS_ENGINEER_URL = os.getenv("CHAOS_ENGINEER_URL", "http://localhost:3010")

app = Flask(__name__)

# Circuit breaker configuration
circuit_breaker_states = {
    "inventory": {"failures": 0, "last_failure": None, "is_open": False},
    "payments": {"failures": 0, "last_failure": None, "is_open": False},
    "shipping": {"failures": 0, "last_failure": None, "is_open": False}
}
CIRCUIT_BREAKER_THRESHOLD = 3
CIRCUIT_BREAKER_TIMEOUT = timedelta(minutes=1)


@dataclass
class Order:
    id: str
    customer: str
    item: str
    total: float

@dataclass
class Approval:
    approver: str
    approved: bool

@dataclass
class OrderResult:
    id: str
    success: bool
    message: str

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
class RetryConfig:
    max_attempts: int = 3
    base_delay_ms: int = 100
    backoff_multiplier: float = 2.0
    max_delay_ms: int = 5000

def should_simulate_failure(service_name: str) -> bool:
    """Check if we should simulate a failure for chaos engineering"""
    if not ENABLE_CHAOS_DETECTION:
        return False

    # Simple random failure simulation - in a real system, this would check
    # with the chaos engineering service for active failure scenarios
    return random.random() < 0.1  # 10% failure rate for demo

def is_circuit_breaker_open(service_name: str) -> bool:
    """Check if circuit breaker is open for a service"""
    state = circuit_breaker_states.get(service_name, {})

    if not state.get("is_open", False):
        return False

    # Check if timeout has expired
    last_failure = state.get("last_failure")
    if last_failure and datetime.now() - last_failure > CIRCUIT_BREAKER_TIMEOUT:
        # Reset circuit breaker
        circuit_breaker_states[service_name] = {"failures": 0, "last_failure": None, "is_open": False}
        return False

    return True

def record_service_failure(service_name: str):
    """Record a service failure for circuit breaker logic"""
    if service_name not in circuit_breaker_states:
        circuit_breaker_states[service_name] = {"failures": 0, "last_failure": None, "is_open": False}

    state = circuit_breaker_states[service_name]
    state["failures"] += 1
    state["last_failure"] = datetime.now()

    if state["failures"] >= CIRCUIT_BREAKER_THRESHOLD:
        state["is_open"] = True
        logging.warning(f"Circuit breaker opened for service: {service_name}")

def record_service_success(service_name: str):
    """Record a service success - reset failure count"""
    if service_name in circuit_breaker_states:
        circuit_breaker_states[service_name]["failures"] = 0

def retry_with_backoff(func, retry_config: RetryConfig, service_name: str, *args, **kwargs):
    """Execute a function with exponential backoff retry logic"""
    last_exception = None

    for attempt in range(retry_config.max_attempts):
        try:
            # Check circuit breaker
            if is_circuit_breaker_open(service_name):
                raise Exception(f"Circuit breaker is open for service: {service_name}")

            # Simulate chaos engineering failure
            if should_simulate_failure(service_name):
                raise Exception(f"Simulated failure for service: {service_name} (chaos engineering)")

            result = func(*args, **kwargs)
            record_service_success(service_name)
            return result

        except Exception as e:
            last_exception = e
            record_service_failure(service_name)

            if attempt < retry_config.max_attempts - 1:
                delay_ms = min(
                    retry_config.base_delay_ms * (retry_config.backoff_multiplier ** attempt),
                    retry_config.max_delay_ms
                )
                logging.warning(f"Attempt {attempt + 1} failed for {service_name}: {str(e)}. Retrying in {delay_ms}ms...")
                time.sleep(delay_ms / 1000.0)
            else:
                logging.error(f"All {retry_config.max_attempts} attempts failed for {service_name}: {str(e)}")

    raise last_exception

# Dapr Workflow Definition for Order Processing

def process_order_workflow(ctx: wf.DaprWorkflowContext, order: Order):
    yield ctx.call_activity(notify, input=f"Processing order for {order.customer}. Item: {order.item}, Total: {order.total}")

    # Call into the inventory service to reserve the items in this order
    result = yield ctx.call_activity(reserve_inventory, input=order)

    if not result.success:
        yield ctx.call_activity(notify, input=f"Failed to reserve inventory: {result.message}")
        return OrderResult(order.id, False, result.message)

    yield ctx.call_activity(notify, input=f"Reserved inventory: {order.item}")

    # Orders over $1,000 require human approval
    if order.total >= APPROVAL_THRESHOLD:
        approval_deadline = ctx.current_utc_datetime + APPROVAL_TIMEOUT
        yield ctx.call_activity(notify, input=f"Waiting for approval since order >= {APPROVAL_THRESHOLD}. Deadline = {approval_deadline}.")

        # Block the workflow on either an approval event or a timeout
        approval_task = ctx.wait_for_external_event("approval")
        timeout_expired_task = ctx.create_timer(approval_deadline)
        winner = yield wf.when_any([approval_task, timeout_expired_task])

        if winner == timeout_expired_task:
            message = "Approval deadline expired."
            yield ctx.call_activity(notify, input=message)
            return OrderResult(order.id, False, message)

        # Check the approval result
        approval: Approval = yield approval_task
        if not approval.approved:
            message = f"Order was rejected by {approval.approver}."
            yield ctx.call_activity(notify, input=message)
            return OrderResult(order.id, False, message)

        yield ctx.call_activity(notify, input=f"Order was approved by {approval.approver}.")

    yield ctx.call_activity(notify, input="Attempting to take payment")

    # Submit the order to the payment service
    try:
        result = yield ctx.call_activity(submit_payment, input=order)
        if not result.success:
            yield ctx.call_activity(notify, input=f"Payment failed for order: {result.message}")
            return OrderResult(order.id, False, result.message)
    except Exception as e:
        yield ctx.call_activity(notify, input=f"Error taking payment: {str(e)}")
        raise

    yield ctx.call_activity(notify, input="Payment processed")

    yield ctx.call_activity(notify, input="Order submitted for shipping")

    # Submit the order for shipping
    try:
        yield ctx.call_activity(submit_order_to_shipping, input=order)
    except Exception as e:
        # Shipping failed, so we need to refund the payment
        yield ctx.call_activity(notify, input=f"Error submitting order for shipping: {str(e)}")
        yield ctx.call_activity(refund_payment, input=order)
        yield ctx.call_activity(notify, input="Payment refunded")

        # Allow the workflow to fail with the original failure details
        raise

    yield ctx.call_activity(notify, input="Shipment scheduled")

    yield ctx.call_activity(notify, input=f"Order processed for {order.customer}. Item: {order.item}, Total: {order.total}")

    return OrderResult(order.id, True, "Order processed")

def notify(ctx: wf.WorkflowActivityContext, message: str):
    logging.info(f"Sending notification: {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": message,
            "data-content-type": "application/json"
        }))


def reserve_inventory(_, order: Order) -> InventoryResult:
    """Reserve inventory with retry logic and circuit breaker"""
    def _reserve_inventory_call():
        logging.info(f"Reserving inventory for order: {order}")
        with DaprClient() as d:
            resp = d.invoke_method("inventory", "api/v1/inventory/reserve",  http_verb="POST",  data=json.dumps(order.__dict__))
            if resp.status_code != 200:
                raise Exception(f"Error calling inventory service: {resp.status_code}")
            inventory_result = InventoryResult(**json.loads(resp.data.decode("utf-8")))
            logging.info(f"Inventory result: {inventory_result}")
            return inventory_result

    # Use retry with backoff for resilience
    retry_config = RetryConfig(max_attempts=3, base_delay_ms=200, backoff_multiplier=2.0)
    return retry_with_backoff(_reserve_inventory_call, retry_config, "inventory")

def submit_order_to_shipping(_, order: Order):
    """Submit order to shipping with retry logic and circuit breaker"""
    def _submit_shipping_call():
        logging.info(f"Submitting order to shipping: {order}")
        with DaprClient() as d:
            resp = d.invoke_method("shipping", "shipping/ship",  http_verb="POST",  data=json.dumps(order.__dict__))
            if resp.status_code != 200:
                raise Exception(f"Error calling shipping service: {resp.status_code}: {resp.text()}")

    # Use retry with backoff for resilience
    retry_config = RetryConfig(max_attempts=4, base_delay_ms=300, backoff_multiplier=1.5)
    return retry_with_backoff(_submit_shipping_call, retry_config, "shipping")

def submit_payment(_, order: Order) -> PaymentResult:
    """Submit payment with retry logic and circuit breaker"""
    def _submit_payment_call():
        logging.info(f"Submitting payment for order: {order}")
        with DaprClient() as d:
            resp = d.invoke_method("payments", "api/v1/payments",  http_verb="POST",  data=json.dumps(order.__dict__))
            payment_result = PaymentResult(**json.loads(resp.data.decode("utf-8")))

            if resp._status_code != 201:
                if 'declined' not in payment_result.message:
                    raise Exception(f"Error calling payment service: {resp.status_code}: {resp.text()}")

            logging.info(f"Payment result: {payment_result}")
            return payment_result

    # Use retry with backoff for resilience (fewer retries for payments to avoid double-charging)
    retry_config = RetryConfig(max_attempts=2, base_delay_ms=500, backoff_multiplier=2.0)
    return retry_with_backoff(_submit_payment_call, retry_config, "payments")

def refund_payment(_, order: Order):
    logging.info(f"Refunding payment for order: {order}")
    with DaprClient() as d:
        resp = d.invoke_method("payments", f"api/v1/payments/{order.id}/refunds",  http_verb="POST",  data=json.dumps(order.__dict__))
        if resp.status_code != 200:
            raise Exception(f"Error calling payment service: {resp.status_code}: {resp.text()}")


# API to submit a new order
@app.route("/orders", methods=["POST"])
def submit_order():

    request_data = request.get_json()
    if not request_data:
        return """Invalid request. Should be in the form of {
            \"customer\": \"joe\", \"item\": \"apples\", \"total\": 100.0}""", 400
    if not request_data.get("customer"):
        return "Missing customer name", 400
    if not request_data.get("item"):
        return "Missing item", 400
    if not request_data.get("total"):
        return "Missing total", 400

    order = Order(
        None,
        request_data.get("customer"),
        request_data.get("item"),
        request_data.get("total"))

    # Generate a unique ID for this order
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    order.id = f"order_{order.customer.lower()}_{random_suffix}"

    wf_client = wf.DaprWorkflowClient()
    instance_id = wf_client.schedule_new_workflow(
        process_order_workflow,
        input=order,
        instance_id=order.id)

    logging.info(f"Started workflow instance: {instance_id}")

    return json.dumps({"instance_id": instance_id}), 202, {
        'Content-Type': 'application/json',
        'Location': url_for('check_order_status', order_id=instance_id, _external=True)
    }


@app.route("/orders/<order_id>", methods=["GET"])
def check_order_status(order_id):
    wf_client = wf.DaprWorkflowClient()
    state = wf_client.get_workflow_state(order_id)
    if not state:
        return f"Order not found: {escape(order_id)}", 404

    order_info = json.loads(state.serialized_input)
    order = Order(
        order_info.get('id'),
        order_info.get('customer'),
        order_info.get('item'),
        order_info.get('total'))
    resp = {
        "id": state.instance_id,
        "details": order.__dict__,
        "status": state.runtime_status.name,
        "created_time": state.created_at.isoformat(),
        "last_updated_time": state.last_updated_at.isoformat(),
    }

    if state.serialized_output:
        order_result_details = json.loads(state.serialized_output)
        order_result = OrderResult(
            order_result_details.get('id'),
            order_result_details.get('success'),
            order_result_details.get('message'))
        resp["order_result"] = order_result.__dict__

    if state.failure_details:
        resp["failure_details"] = {
            "message": state.failure_details.message,
            "error_type": state.failure_details.error_type,
            "stack_trace": state.failure_details.stack_trace
        }

    return resp, 200


@app.route("/orders/<order_id>/approve", methods=["POST"])
def approve_order(order_id):
    request_data = request.get_json()
    if not request_data:
        return """Invalid request. Should be in the form of { \"approver\": \"joe\", \"approved\": true }""", 400
    if not request_data.get("approver"):
        return "Missing approver name", 400
    if "approved" not in request_data:
        return "Missing approved flag", 400

    approval = Approval(
        request_data.get("approver"),
        request_data.get("approved"))

    wf_client = wf.DaprWorkflowClient()
    wf_client.raise_workflow_event(order_id, "approval", data=approval)

    return f"Approval sent for order: {escape(order_id)}", 200


@app.route("/", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def hello():
    return f"Hello from {__name__}", 200

@app.route("/circuit-breakers", methods=["GET"])
def get_circuit_breaker_status():
    """Get circuit breaker status for debugging"""
    status = {}
    for service, state in circuit_breaker_states.items():
        status[service] = {
            "is_open": state.get("is_open", False),
            "failure_count": state.get("failures", 0),
            "last_failure": state.get("last_failure").isoformat() if state.get("last_failure") else None,
            "threshold": CIRCUIT_BREAKER_THRESHOLD,
            "timeout_minutes": CIRCUIT_BREAKER_TIMEOUT.total_seconds() / 60
        }

    return {
        "circuit_breakers": status,
        "chaos_detection_enabled": ENABLE_CHAOS_DETECTION,
        "timestamp": datetime.now().isoformat()
    }


def main():
    # Start the workflow runtime
    logging.info("Starting workflow runtime...")
    wf_runtime = wf.WorkflowRuntime()  # host/port comes from env vars
    wf_runtime.register_workflow(process_order_workflow)
    wf_runtime.register_activity(notify)
    wf_runtime.register_activity(reserve_inventory)
    wf_runtime.register_activity(submit_payment)
    wf_runtime.register_activity(submit_order_to_shipping)
    wf_runtime.register_activity(refund_payment)
    wf_runtime.start()  # non-blocking

    # Start the Flask app server
    app.run(host='0.0.0.0', port=APP_PORT, debug=False, use_reloader=False)

    # Stop the workflow runtime to allow the process to terminate
    wf_runtime.shutdown()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    main()
