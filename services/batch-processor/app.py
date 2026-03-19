import json
import logging
import os
import random
import string
import sys

# Add parent directory to path for common imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import dapr.ext.workflow as wf
from common.resilient_workflow_runtime import ResilientWorkflowRuntime
from dapr.clients import DaprClient
from flask import Flask, request, jsonify, make_response, url_for
from markupsafe import escape
from dataclasses import dataclass
from datetime import timedelta
from typing import List

APP_PORT = os.getenv("APP_PORT", "3007")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)

@dataclass
class OrderItem:
    item: str
    quantity: int = 1
    price: float = 0.0

@dataclass
class SingleOrder:
    id: str
    customer: str
    item: str
    total: float

@dataclass
class BulkOrder:
    id: str
    customer: str
    items: List[OrderItem]
    total: float

@dataclass
class BulkOrderResult:
    id: str
    success: bool
    message: str
    completed_items: List[str]
    failed_items: List[str]
    child_workflow_ids: List[str]

@dataclass
class ChildOrderResult:
    item_name: str
    success: bool
    message: str
    child_workflow_id: str

@dataclass
class SingleOrderResult:
    id: str
    success: bool
    message: str

@dataclass
class Approval:
    approver: str
    approved: bool

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

# Bulk Order Processing Workflow (Parent Workflow)
def process_bulk_order_workflow(ctx: wf.DaprWorkflowContext, bulk_order: BulkOrder):
    """
    Parent workflow that processes a bulk order by spawning child workflows for each item
    """
    # Handle case where bulk_order might be a dict (from serialization/deserialization)
    if isinstance(bulk_order, dict):
        customer = bulk_order.get("customer")
        items = bulk_order.get("items", [])
        bulk_order_id = bulk_order.get("id")
        total = bulk_order.get("total", 0.0)
    else:
        # bulk_order is a BulkOrder dataclass
        customer = bulk_order.customer
        items = bulk_order.items
        bulk_order_id = bulk_order.id
        total = bulk_order.total

    yield ctx.call_activity(announce_bulk_order_started, input=f"Starting bulk order processing for {customer}. Items: {len(items)}")

    child_tasks = []
    child_workflow_ids = []

    # Spawn child workflow for each item in the bulk order
    for i, order_item in enumerate(items):
        # Handle case where order_item might be a dict (from serialization/deserialization)
        if isinstance(order_item, dict):
            item_name = order_item.get("item")
            item_price = order_item.get("price", 100.0)
            item_quantity = order_item.get("quantity", 1)
        else:
            # order_item is an OrderItem dataclass
            item_name = order_item.item
            item_price = order_item.price
            item_quantity = order_item.quantity

                # Create a single order for this item
        single_order = SingleOrder(
            id=f"{bulk_order_id}_item_{i}_{item_name}",
            customer=customer,
            item=item_name,
            total=item_price * item_quantity
        )

        # Spawn child workflow
        child_workflow_id = f"{bulk_order_id}_child_{i}_{item_name}"
        child_workflow_ids.append(child_workflow_id)

        yield ctx.call_activity(announce_child_workflow_spawned, input=f"Spawning child workflow for item: {item_name} (ID: {child_workflow_id})")

        # Call child workflow (this will invoke the existing order processor)
        child_task = ctx.call_child_workflow(
            process_single_item_workflow,
            input=single_order,
            instance_id=child_workflow_id
        )
        child_tasks.append((child_task, item_name, child_workflow_id))

    yield ctx.call_activity(announce_waiting_for_children, input=f"All {len(child_tasks)} child workflows spawned. Waiting for completion...")

    # Wait for all child workflows to complete
    completed_items = []
    failed_items = []

    try:
        # Process child workflow results
        for child_task, item_name, child_workflow_id in child_tasks:
            try:
                child_result = yield child_task
                if child_result and getattr(child_result, 'success', False):
                    completed_items.append(item_name)
                    yield ctx.call_activity(announce_item_success, input=f"✅ Item '{item_name}' processed successfully")
                else:
                    failed_items.append(item_name)
                    failure_msg = getattr(child_result, 'message', 'Unknown error') if child_result else 'No result returned'
                    yield ctx.call_activity(announce_item_failure, input=f"❌ Item '{item_name}' failed: {failure_msg}")
            except Exception as e:
                failed_items.append(item_name)
                yield ctx.call_activity(announce_item_failure, input=f"❌ Item '{item_name}' failed with exception: {str(e)}")

        # Determine overall success
        overall_success = len(failed_items) == 0

        if overall_success:
            yield ctx.call_activity(announce_bulk_order_completed, input=f"🎉 Bulk order completed successfully! All {len(completed_items)} items processed.")
        else:
            yield ctx.call_activity(announce_bulk_order_partial_success, input=f"⚠️ Bulk order partially completed. Success: {len(completed_items)}, Failed: {len(failed_items)}")

        return BulkOrderResult(
            id=bulk_order_id,
            success=overall_success,
            message=f"Bulk order processed. Success: {len(completed_items)}, Failed: {len(failed_items)}",
            completed_items=completed_items,
            failed_items=failed_items,
            child_workflow_ids=child_workflow_ids
        )

    except Exception as e:
        yield ctx.call_activity(announce_bulk_order_failed, input=f"💥 Bulk order workflow failed: {str(e)}")
        return BulkOrderResult(
            id=bulk_order_id,
            success=False,
            message=f"Bulk order workflow failed: {str(e)}",
            completed_items=completed_items,
            failed_items=[
                (item.get("item") if isinstance(item, dict) else item.item)
                for item in items
                if (item.get("item") if isinstance(item, dict) else item.item) not in completed_items
            ],
            child_workflow_ids=child_workflow_ids
        )

# Single Item Processing Workflow (Child Workflow)
def process_single_item_workflow(ctx: wf.DaprWorkflowContext, single_order: SingleOrder):
    """
    Child workflow that processes a single item using the full order processing logic
    """
    APPROVAL_THRESHOLD = 1000.0
    APPROVAL_TIMEOUT = timedelta(hours=24)

        # Handle case where single_order might be a dict (from serialization/deserialization)
    if isinstance(single_order, dict):
        # Convert dict to SingleOrder object
        single_order = SingleOrder(
            id=single_order.get("id"),
            customer=single_order.get("customer"),
            item=single_order.get("item"),
            total=single_order.get("total", 0.0)
        )

    yield ctx.call_activity(announce_item_processing_started, input=f"🔄 Processing single item: {single_order.item} for {single_order.customer}")

    # Step 1: Reserve inventory
    result = yield ctx.call_activity(reserve_item_inventory, input=single_order)

    if not result.success:
        yield ctx.call_activity(announce_inventory_reservation_failed, input=f"❌ Failed to reserve inventory for {single_order.item}: {result.message}")
        return SingleOrderResult(single_order.id, False, result.message)

    yield ctx.call_activity(announce_inventory_reserved, input=f"✅ Reserved inventory for: {single_order.item}")

    # Step 2: Check if approval is needed for high-value items
    if single_order.total >= APPROVAL_THRESHOLD:
        approval_deadline = ctx.current_utc_datetime + APPROVAL_TIMEOUT
        yield ctx.call_activity(announce_approval_required, input=f"⏳ Waiting for approval for {single_order.item} (${single_order.total:.2f} >= ${APPROVAL_THRESHOLD:.2f})")

        # Block the workflow on either an approval event or a timeout
        approval_task = ctx.wait_for_external_event("approval")
        timeout_expired_task = ctx.create_timer(approval_deadline)
        winner = yield wf.when_any([approval_task, timeout_expired_task])

        if winner == timeout_expired_task:
            message = f"Approval deadline expired for {single_order.item}"
            yield ctx.call_activity(announce_approval_timeout, input=f"❌ {message}")
            return SingleOrderResult(single_order.id, False, message)

        # Check the approval result
        approval = yield approval_task
        if not approval.approved:
            message = f"Order for {single_order.item} was rejected by {approval.approver}"
            yield ctx.call_activity(announce_approval_rejected, input=f"❌ {message}")
            return SingleOrderResult(single_order.id, False, message)

        yield ctx.call_activity(announce_approval_received, input=f"✅ Order for {single_order.item} was approved by {approval.approver}")

    # Step 3: Process payment
    yield ctx.call_activity(announce_payment_processing, input=f"💳 Processing payment for {single_order.item}")

    try:
        result = yield ctx.call_activity(process_item_payment, input=single_order)
        if not result.success:
            yield ctx.call_activity(announce_payment_failed, input=f"❌ Payment failed for {single_order.item}: {result.message}")
            return SingleOrderResult(single_order.id, False, result.message)
    except Exception as e:
        yield ctx.call_activity(announce_payment_failed, input=f"❌ Error processing payment for {single_order.item}: {str(e)}")
        raise

    yield ctx.call_activity(announce_payment_completed, input=f"✅ Payment processed for {single_order.item}")

    # Step 4: Submit for shipping
    yield ctx.call_activity(announce_shipping_submission, input=f"🚚 Submitting {single_order.item} for shipping")

    try:
        yield ctx.call_activity(submit_item_for_shipping, input=single_order)
    except Exception as e:
        # Shipping failed, so we need to refund the payment
        yield ctx.call_activity(announce_shipping_failed, input=f"❌ Shipping failed for {single_order.item}: {str(e)}")
        yield ctx.call_activity(process_item_refund, input=single_order)
        yield ctx.call_activity(announce_payment_refunded, input=f"💰 Payment refunded for {single_order.item}")
        raise

    yield ctx.call_activity(announce_shipping_scheduled, input=f"✅ {single_order.item} shipment scheduled")
    yield ctx.call_activity(announce_item_processing_completed, input=f"🎉 Order completed for {single_order.customer}: {single_order.item} (${single_order.total:.2f})")

    return SingleOrderResult(single_order.id, True, "Order processed successfully")

# Activity Functions - Notification Activities (Stage-Specific)
def announce_bulk_order_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce bulk order processing has started"""
    logging.info(f"[BULK START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_child_workflow_spawned(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce a child workflow has been spawned"""
    logging.info(f"[CHILD SPAWN] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_waiting_for_children(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce waiting for child workflows to complete"""
    logging.info(f"[WAITING] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_item_success(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce successful item processing"""
    logging.info(f"[ITEM SUCCESS] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_item_failure(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce failed item processing"""
    logging.info(f"[ITEM FAILURE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_bulk_order_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce bulk order completion"""
    logging.info(f"[BULK COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_bulk_order_partial_success(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce bulk order partial completion"""
    logging.info(f"[BULK PARTIAL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_bulk_order_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce bulk order failure"""
    logging.info(f"[BULK FAILED] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

# Child Workflow Notification Activities
def announce_item_processing_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce item processing has started"""
    logging.info(f"[ITEM START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_inventory_reserved(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce inventory reservation success"""
    logging.info(f"[INVENTORY OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_inventory_reservation_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce inventory reservation failure"""
    logging.info(f"[INVENTORY FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_approval_required(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce approval is required"""
    logging.info(f"[APPROVAL REQ] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_approval_received(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce approval was received"""
    logging.info(f"[APPROVAL OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_approval_rejected(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce approval was rejected"""
    logging.info(f"[APPROVAL REJECT] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_approval_timeout(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce approval timeout"""
    logging.info(f"[APPROVAL TIMEOUT] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_payment_processing(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce payment processing has started"""
    logging.info(f"[PAYMENT START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_payment_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce payment completion"""
    logging.info(f"[PAYMENT OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_payment_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce payment failure"""
    logging.info(f"[PAYMENT FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_shipping_submission(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce shipping submission"""
    logging.info(f"[SHIPPING START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_shipping_scheduled(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce shipping was scheduled"""
    logging.info(f"[SHIPPING OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_shipping_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce shipping failure"""
    logging.info(f"[SHIPPING FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_payment_refunded(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce payment refund"""
    logging.info(f"[REFUND OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

def announce_item_processing_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce item processing completion"""
    logging.info(f"[ITEM COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[BULK] {message}",
            "data-content-type": "application/json"
        }))

# Business Logic Activities (Renamed for Clarity)
def reserve_item_inventory(_, single_order: SingleOrder) -> InventoryResult:
    """Activity to reserve inventory for a single item in bulk order"""
    # Handle case where single_order might be a dict
    if isinstance(single_order, dict):
        single_order = SingleOrder(
            id=single_order.get("id"),
            customer=single_order.get("customer"),
            item=single_order.get("item"),
            total=single_order.get("total", 0.0)
        )

    logging.info(f"Reserving inventory for: {single_order}")
    with DaprClient() as d:
        resp = d.invoke_method("inventory", "api/v1/inventory/reserve", http_verb="POST", data=json.dumps({
            "id": single_order.id,
            "item": single_order.item,
            "customer": single_order.customer,
            "total": single_order.total
        }))
        if resp.status_code != 200:
            raise Exception(f"Error calling inventory service: {resp.status_code}")
        inventory_result = InventoryResult(**json.loads(resp.data.decode("utf-8")))
        logging.info(f"Inventory result: {inventory_result}")
        return inventory_result

def process_item_payment(_, single_order: SingleOrder) -> PaymentResult:
    """Activity to process payment for a single item in bulk order"""
    # Handle case where single_order might be a dict
    if isinstance(single_order, dict):
        single_order = SingleOrder(
            id=single_order.get("id"),
            customer=single_order.get("customer"),
            item=single_order.get("item"),
            total=single_order.get("total", 0.0)
        )

    logging.info(f"Processing payment for: {single_order}")
    with DaprClient() as d:
        resp = d.invoke_method("payments", "api/v1/payments", http_verb="POST", data=json.dumps({
            "id": single_order.id,
            "customer": single_order.customer,
            "item": single_order.item,
            "total": single_order.total
        }))
        payment_result = PaymentResult(**json.loads(resp.data.decode("utf-8")))

        if resp.status_code != 201:
            if 'declined' not in payment_result.message:
                raise Exception(f"Error calling payment service: {resp.status_code}")

        logging.info(f"Payment result: {payment_result}")
        return payment_result

def submit_item_for_shipping(_, single_order: SingleOrder):
    """Activity to submit order to shipping for a single item in bulk order"""
    # Handle case where single_order might be a dict
    if isinstance(single_order, dict):
        single_order = SingleOrder(
            id=single_order.get("id"),
            customer=single_order.get("customer"),
            item=single_order.get("item"),
            total=single_order.get("total", 0.0)
        )

    logging.info(f"Submitting order to shipping: {single_order}")
    with DaprClient() as d:
        resp = d.invoke_method("shipping", "shipping/ship", http_verb="POST", data=json.dumps({
            "id": single_order.id,
            "customer": single_order.customer,
            "item": single_order.item,
            "total": single_order.total
        }))
        if resp.status_code != 200:
            raise Exception(f"Error calling shipping service: {resp.status_code}")

def process_item_refund(_, single_order: SingleOrder):
    """Activity to refund payment for a single item in bulk order"""
    # Handle case where single_order might be a dict
    if isinstance(single_order, dict):
        single_order = SingleOrder(
            id=single_order.get("id"),
            customer=single_order.get("customer"),
            item=single_order.get("item"),
            total=single_order.get("total", 0.0)
        )

    logging.info(f"Refunding payment for: {single_order}")
    with DaprClient() as d:
        resp = d.invoke_method("payments", f"api/v1/payments/{single_order.id}/refunds", http_verb="POST", data=json.dumps({
            "id": single_order.id,
            "customer": single_order.customer,
            "item": single_order.item,
            "total": single_order.total
        }))
        if resp.status_code != 200:
            raise Exception(f"Error calling payment service: {resp.status_code}")

# API Endpoints
@app.route("/bulk-orders", methods=["POST"])
def submit_bulk_order():
    """Submit a bulk order with multiple items"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request. Expected JSON body"}), 400

    if not request_data.get("customer"):
        return jsonify({"error": "Missing customer name"}), 400

    if not request_data.get("items") or not isinstance(request_data.get("items"), list):
        return jsonify({"error": "Missing or invalid items array"}), 400

    # Parse items
    items = []
    total_cost = 0.0

    for item_data in request_data["items"]:
        if not isinstance(item_data, dict) or not item_data.get("item"):
            return jsonify({"error": "Each item must have 'item' field"}), 400

        quantity = item_data.get("quantity", 1)
        price = item_data.get("price", 100.0)  # Default price

        order_item = OrderItem(
            item=item_data["item"],
            quantity=quantity,
            price=price
        )
        items.append(order_item)
        total_cost += price * quantity

    # Generate unique bulk order ID
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    bulk_order_id = f"bulk_{request_data['customer'].lower()}_{random_suffix}"

    bulk_order = BulkOrder(
        id=bulk_order_id,
        customer=request_data["customer"],
        items=items,
        total=total_cost
    )

    # Start the bulk order workflow
    try:
        wf_client = wf.DaprWorkflowClient()
        instance_id = wf_client.schedule_new_workflow(
            process_bulk_order_workflow,
            input=bulk_order,
            instance_id=bulk_order_id
        )

        logging.info(f"Started bulk order workflow: {instance_id}")

        return jsonify({
            "instance_id": instance_id,
            "bulk_order_id": bulk_order_id,
            "items_count": len(items),
            "total_cost": total_cost
        }), 202, {
            'Content-Type': 'application/json',
            'Location': url_for('check_bulk_order_status', order_id=instance_id, _external=True)
        }

    except Exception as e:
        logging.error(f"Error starting bulk order workflow: {str(e)}")
        return jsonify({"error": f"Failed to start bulk order: {str(e)}"}), 500

@app.route("/bulk-orders/<order_id>", methods=["GET"])
def check_bulk_order_status(order_id):
    """Check the status of a bulk order"""
    try:
        wf_client = wf.DaprWorkflowClient()
        state = wf_client.get_workflow_state(order_id)

        if not state:
            return jsonify({"error": f"Bulk order not found: {escape(order_id)}"}), 404

        # Parse the input to get bulk order details
        bulk_order_info = json.loads(state.serialized_input)

        response = {
            "id": state.instance_id,
            "status": state.runtime_status.name,
            "created_time": state.created_at.isoformat(),
            "last_updated_time": state.last_updated_at.isoformat(),
            "bulk_order_details": {
                "customer": bulk_order_info.get("customer"),
                "items_count": len(bulk_order_info.get("items", [])),
                "total": bulk_order_info.get("total"),
                "items": bulk_order_info.get("items", [])
            }
        }

        # Add result if workflow is completed
        if state.serialized_output:
            try:
                result_data = json.loads(state.serialized_output)
                response["bulk_order_result"] = result_data
            except json.JSONDecodeError:
                response["bulk_order_result"] = {"message": "Result parsing error"}

        # Add failure details if any
        if state.failure_details:
            response["failure_details"] = {
                "message": state.failure_details.message,
                "error_type": state.failure_details.error_type,
                "stack_trace": state.failure_details.stack_trace
            }

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error checking bulk order status: {str(e)}")
        return jsonify({"error": f"Failed to check status: {str(e)}"}), 500

@app.route("/bulk-orders/<order_id>/items/<item_workflow_id>/approve", methods=["POST"])
def approve_bulk_order_item(order_id, item_workflow_id):
    """Approve a specific item in a bulk order (for child workflows that need approval)"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request. Expected JSON body with approver and approved fields"}), 400

    if not request_data.get("approver"):
        return jsonify({"error": "Missing approver name"}), 400

    if "approved" not in request_data:
        return jsonify({"error": "Missing approved flag"}), 400

    approval = Approval(
        request_data.get("approver"),
        request_data.get("approved")
    )

    try:
        wf_client = wf.DaprWorkflowClient()
        wf_client.raise_workflow_event(item_workflow_id, "approval", data=approval)

        logging.info(f"Approval sent for bulk order item: {item_workflow_id} by {approval.approver}")

        return jsonify({
            "message": f"Approval sent for item workflow: {escape(item_workflow_id)}",
            "bulk_order_id": escape(order_id),
            "item_workflow_id": escape(item_workflow_id),
            "approver": escape(approval.approver),
            "approved": approval.approved
        }), 200

    except Exception as e:
        logging.error(f"Error sending approval for item workflow {item_workflow_id}: {str(e)}")
        return jsonify({"error": f"Failed to send approval: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({
        "service": "batch-processor",
        "status": "healthy",
        "version": "1.0.0"
    })

def main():
    # Start the workflow runtime with auto-reconnection
    logging.info("Starting batch processor workflow runtime...")
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )
    wf_runtime.register_workflow(process_bulk_order_workflow)
    wf_runtime.register_workflow(process_single_item_workflow)

    # Register stage-specific notification activities
    wf_runtime.register_activity(announce_bulk_order_started)
    wf_runtime.register_activity(announce_child_workflow_spawned)
    wf_runtime.register_activity(announce_waiting_for_children)
    wf_runtime.register_activity(announce_item_success)
    wf_runtime.register_activity(announce_item_failure)
    wf_runtime.register_activity(announce_bulk_order_completed)
    wf_runtime.register_activity(announce_bulk_order_partial_success)
    wf_runtime.register_activity(announce_bulk_order_failed)

    # Register child workflow notification activities
    wf_runtime.register_activity(announce_item_processing_started)
    wf_runtime.register_activity(announce_inventory_reserved)
    wf_runtime.register_activity(announce_inventory_reservation_failed)
    wf_runtime.register_activity(announce_approval_required)
    wf_runtime.register_activity(announce_approval_received)
    wf_runtime.register_activity(announce_approval_rejected)
    wf_runtime.register_activity(announce_approval_timeout)
    wf_runtime.register_activity(announce_payment_processing)
    wf_runtime.register_activity(announce_payment_completed)
    wf_runtime.register_activity(announce_payment_failed)
    wf_runtime.register_activity(announce_shipping_submission)
    wf_runtime.register_activity(announce_shipping_scheduled)
    wf_runtime.register_activity(announce_shipping_failed)
    wf_runtime.register_activity(announce_payment_refunded)
    wf_runtime.register_activity(announce_item_processing_completed)

    # Register business logic activities
    wf_runtime.register_activity(reserve_item_inventory)
    wf_runtime.register_activity(process_item_payment)
    wf_runtime.register_activity(submit_item_for_shipping)
    wf_runtime.register_activity(process_item_refund)

    wf_runtime.start()  # non-blocking with auto-reconnect

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
