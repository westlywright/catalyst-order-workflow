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
from datetime import timedelta, datetime
from typing import List, Optional
from enum import Enum

APP_PORT = os.getenv("APP_PORT", "3008")
PUBSUB_NAME = os.getenv("PUBSUB_NAME", "pubsub")
TOPIC_NAME = os.getenv("TOPIC_NAME", "notifications")

app = Flask(__name__)

class ReturnReason(Enum):
    DEFECTIVE = "defective"
    WRONG_SIZE = "wrong_size"
    CHANGED_MIND = "changed_mind"
    NOT_AS_DESCRIBED = "not_as_described"
    DAMAGED_SHIPPING = "damaged_shipping"

class ReturnStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REFUNDED = "refunded"
    COMPLETED = "completed"

@dataclass
class ReturnRequest:
    id: str
    original_order_id: str
    customer: str
    item: str
    reason: str
    description: str
    return_value: float
    requested_date: str

@dataclass
class ReturnResult:
    id: str
    success: bool
    message: str
    status: str
    refund_amount: float
    restocked: bool

@dataclass
class ValidationResult:
    valid: bool
    message: str
    requires_approval: bool

@dataclass
class RefundResult:
    id: str
    success: bool
    message: str
    amount: float

@dataclass
class Approval:
    approver: str
    approved: bool

# Main Return Processing Workflow
def process_return_workflow(ctx: wf.DaprWorkflowContext, return_request: ReturnRequest):
    """
    Main return processing workflow that demonstrates workflow chaining and state management
    """
    # Handle serialization/deserialization
    if isinstance(return_request, dict):
        return_request = ReturnRequest(
            id=return_request.get("id"),
            original_order_id=return_request.get("original_order_id"),
            customer=return_request.get("customer"),
            item=return_request.get("item"),
            reason=return_request.get("reason"),
            description=return_request.get("description"),
            return_value=return_request.get("return_value", 0.0),
            requested_date=return_request.get("requested_date")
        )

    yield ctx.call_activity(announce_return_request_received, input=f"🔄 Processing return request {return_request.id} for {return_request.customer}")
    yield ctx.call_activity(announce_return_details_logged, input=f"📋 Return details: {return_request.item} (${return_request.return_value:.2f}) - Reason: {return_request.reason}")

    # Step 1: Validate return request
    yield ctx.call_activity(announce_return_validation_started, input=f"✅ Validating return eligibility...")
    validation_result = yield ctx.call_activity(validate_return_eligibility, input=return_request)

    if not validation_result.valid:
        yield ctx.call_activity(announce_return_validation_failed, input=f"❌ Return validation failed: {validation_result.message}")
        return ReturnResult(
            id=return_request.id,
            success=False,
            message=validation_result.message,
            status=ReturnStatus.REJECTED.value,
            refund_amount=0.0,
            restocked=False
        )

    yield ctx.call_activity(announce_return_validation_passed, input=f"✅ Return request validated successfully")

    # Step 2: Check if approval is needed
    if validation_result.requires_approval:
        yield ctx.call_activity(announce_return_approval_required, input=f"⏳ Return requires manager approval (high value or special circumstances)")

        # Wait for approval with 24-hour timeout
        approval_deadline = ctx.current_utc_datetime + timedelta(hours=24)
        approval_task = ctx.wait_for_external_event("return_approval")
        timeout_task = ctx.create_timer(approval_deadline)

        winner = yield wf.when_any([approval_task, timeout_task])

        if winner == timeout_task:
            message = "Return approval deadline expired"
            yield ctx.call_activity(announce_return_approval_timeout, input=f"❌ {message}")
            return ReturnResult(
                id=return_request.id,
                success=False,
                message=message,
                status=ReturnStatus.REJECTED.value,
                refund_amount=0.0,
                restocked=False
            )

        approval = yield approval_task
        if not approval.approved:
            message = f"Return was rejected by {approval.approver}"
            yield ctx.call_activity(announce_return_approval_rejected, input=f"❌ {message}")
            return ReturnResult(
                id=return_request.id,
                success=False,
                message=message,
                status=ReturnStatus.REJECTED.value,
                refund_amount=0.0,
                restocked=False
            )

        yield ctx.call_activity(announce_return_approval_received, input=f"✅ Return approved by {approval.approver}")

    # Step 3: Determine return processing type and spawn child workflow
    yield ctx.call_activity(announce_return_type_determination, input=f"🔄 Determining return processing type...")

    return_type = determine_return_type(return_request.reason)
    child_workflow_id = f"{return_request.id}_child_{return_type}"

    yield ctx.call_activity(announce_return_child_workflow_spawned, input=f"🚀 Spawning {return_type} return processing workflow")

    # Call appropriate child workflow based on return type
    if return_type == "defective":
        processing_result = yield ctx.call_child_workflow(
            process_defective_return_workflow,
            input=return_request,
            instance_id=child_workflow_id
        )
    elif return_type == "standard":
        processing_result = yield ctx.call_child_workflow(
            process_standard_return_workflow,
            input=return_request,
            instance_id=child_workflow_id
        )
    else:  # expedited
        processing_result = yield ctx.call_child_workflow(
            process_expedited_return_workflow,
            input=return_request,
            instance_id=child_workflow_id
        )

    # Step 4: Finalize return
    if processing_result and getattr(processing_result, 'success', False):
        yield ctx.call_activity(announce_return_processing_completed, input=f"🎉 Return {return_request.id} completed successfully!")
        yield ctx.call_activity(announce_return_refund_summary, input=f"💰 Refund amount: ${processing_result.refund_amount:.2f}")
        yield ctx.call_activity(announce_return_inventory_summary, input=f"📦 Inventory restocked: {processing_result.restocked}")

        return ReturnResult(
            id=return_request.id,
            success=True,
            message="Return processed successfully",
            status=ReturnStatus.COMPLETED.value,
            refund_amount=processing_result.refund_amount,
            restocked=processing_result.restocked
        )
    else:
        failure_msg = getattr(processing_result, 'message', 'Unknown error') if processing_result else 'No result returned'
        yield ctx.call_activity(announce_return_processing_failed, input=f"❌ Return processing failed: {failure_msg}")

        return ReturnResult(
            id=return_request.id,
            success=False,
            message=failure_msg,
            status=ReturnStatus.REJECTED.value,
            refund_amount=0.0,
            restocked=False
        )

# Child Workflow: Defective Return Processing
def process_defective_return_workflow(ctx: wf.DaprWorkflowContext, return_request: ReturnRequest):
    """
    Child workflow for processing defective items - requires special handling
    """
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    yield ctx.call_activity(announce_defective_return_started, input=f"🔧 Processing DEFECTIVE return for {return_request.item}")

    # For defective items, we provide full refund without restocking
    yield ctx.call_activity(announce_defective_refund_processing, input=f"💳 Processing full refund (defective item)")
    refund_result = yield ctx.call_activity(process_return_refund, input=return_request)

    if not refund_result.success:
        yield ctx.call_activity(announce_defective_refund_failed, input=f"❌ Refund failed: {refund_result.message}")
        return ReturnResult(
            id=return_request.id,
            success=False,
            message=refund_result.message,
            status=ReturnStatus.REJECTED.value,
            refund_amount=0.0,
            restocked=False
        )

    yield ctx.call_activity(announce_defective_return_completed, input=f"✅ Defective return processed - item will be disposed of")

    return ReturnResult(
        id=return_request.id,
        success=True,
        message="Defective return processed successfully",
        status=ReturnStatus.COMPLETED.value,
        refund_amount=refund_result.amount,
        restocked=False  # Defective items are not restocked
    )

# Child Workflow: Standard Return Processing
def process_standard_return_workflow(ctx: wf.DaprWorkflowContext, return_request: ReturnRequest):
    """
    Child workflow for processing standard returns - refund and restock
    """
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    yield ctx.call_activity(announce_standard_return_started, input=f"📦 Processing STANDARD return for {return_request.item}")

    # Process refund
    yield ctx.call_activity(announce_standard_refund_processing, input=f"💳 Processing refund")
    refund_result = yield ctx.call_activity(process_return_refund, input=return_request)

    if not refund_result.success:
        yield ctx.call_activity(announce_standard_refund_failed, input=f"❌ Refund failed: {refund_result.message}")
        return ReturnResult(
            id=return_request.id,
            success=False,
            message=refund_result.message,
            status=ReturnStatus.REJECTED.value,
            refund_amount=0.0,
            restocked=False
        )

    # Restock inventory
    yield ctx.call_activity(announce_standard_restocking_started, input=f"📋 Restocking inventory")
    restock_result = yield ctx.call_activity(restock_returned_inventory, input=return_request)

    if not restock_result:
        yield ctx.call_activity(announce_standard_restocking_warning, input=f"⚠️ Warning: Refund processed but inventory restock failed")

    yield ctx.call_activity(announce_standard_return_completed, input=f"✅ Standard return processed successfully")

    return ReturnResult(
        id=return_request.id,
        success=True,
        message="Standard return processed successfully",
        status=ReturnStatus.COMPLETED.value,
        refund_amount=refund_result.amount,
        restocked=restock_result
    )

# Child Workflow: Expedited Return Processing
def process_expedited_return_workflow(ctx: wf.DaprWorkflowContext, return_request: ReturnRequest):
    """
    Child workflow for expedited returns - parallel processing for speed
    """
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    yield ctx.call_activity(announce_expedited_return_started, input=f"⚡ Processing EXPEDITED return for {return_request.item}")

    # Process refund and restock in parallel for speed
    yield ctx.call_activity(announce_expedited_parallel_processing, input=f"🚀 Processing refund and inventory restock in parallel")

    refund_task = ctx.call_activity(process_return_refund, input=return_request)
    restock_task = ctx.call_activity(restock_returned_inventory, input=return_request)

    # Wait for both to complete
    results = yield wf.when_all([refund_task, restock_task])
    refund_result, restock_result = results

    if not refund_result.success:
        yield ctx.call_activity(announce_expedited_refund_failed, input=f"❌ Expedited refund failed: {refund_result.message}")
        return ReturnResult(
            id=return_request.id,
            success=False,
            message=refund_result.message,
            status=ReturnStatus.REJECTED.value,
            refund_amount=0.0,
            restocked=False
        )

    yield ctx.call_activity(announce_expedited_return_completed, input=f"✅ Expedited return processed in parallel")

    return ReturnResult(
        id=return_request.id,
        success=True,
        message="Expedited return processed successfully",
        status=ReturnStatus.COMPLETED.value,
        refund_amount=refund_result.amount,
        restocked=restock_result
    )

# Activity Functions - Stage-Specific Notification Activities
def announce_return_request_received(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return request has been received"""
    logging.info(f"[RETURN RECEIVED] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_details_logged(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return details have been logged"""
    logging.info(f"[RETURN DETAILS] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_validation_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return validation has started"""
    logging.info(f"[VALIDATION START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_validation_passed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return validation passed"""
    logging.info(f"[VALIDATION OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_validation_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return validation failed"""
    logging.info(f"[VALIDATION FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_approval_required(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return approval is required"""
    logging.info(f"[APPROVAL REQ] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_approval_received(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return approval was received"""
    logging.info(f"[APPROVAL OK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_approval_rejected(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return approval was rejected"""
    logging.info(f"[APPROVAL REJECT] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_approval_timeout(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return approval timeout"""
    logging.info(f"[APPROVAL TIMEOUT] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_type_determination(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return type determination"""
    logging.info(f"[TYPE DETERMINATION] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_child_workflow_spawned(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce child workflow has been spawned"""
    logging.info(f"[CHILD SPAWN] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_processing_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return processing completed"""
    logging.info(f"[RETURN COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_processing_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return processing failed"""
    logging.info(f"[RETURN FAILED] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_refund_summary(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return refund summary"""
    logging.info(f"[REFUND SUMMARY] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_return_inventory_summary(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce return inventory summary"""
    logging.info(f"[INVENTORY SUMMARY] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

# Defective Return Notification Activities
def announce_defective_return_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce defective return processing started"""
    logging.info(f"[DEFECTIVE START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_defective_refund_processing(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce defective refund processing"""
    logging.info(f"[DEFECTIVE REFUND] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_defective_refund_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce defective refund failed"""
    logging.info(f"[DEFECTIVE REFUND FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_defective_return_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce defective return completed"""
    logging.info(f"[DEFECTIVE COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

# Standard Return Notification Activities
def announce_standard_return_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard return processing started"""
    logging.info(f"[STANDARD START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_standard_refund_processing(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard refund processing"""
    logging.info(f"[STANDARD REFUND] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_standard_refund_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard refund failed"""
    logging.info(f"[STANDARD REFUND FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_standard_restocking_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard restocking started"""
    logging.info(f"[STANDARD RESTOCK] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_standard_restocking_warning(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard restocking warning"""
    logging.info(f"[STANDARD RESTOCK WARN] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_standard_return_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce standard return completed"""
    logging.info(f"[STANDARD COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

# Expedited Return Notification Activities
def announce_expedited_return_started(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce expedited return processing started"""
    logging.info(f"[EXPEDITED START] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_expedited_parallel_processing(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce expedited parallel processing"""
    logging.info(f"[EXPEDITED PARALLEL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_expedited_refund_failed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce expedited refund failed"""
    logging.info(f"[EXPEDITED REFUND FAIL] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

def announce_expedited_return_completed(ctx: wf.WorkflowActivityContext, message: str):
    """Activity to announce expedited return completed"""
    logging.info(f"[EXPEDITED COMPLETE] {message}")
    with DaprClient() as d:
        d.publish_event(PUBSUB_NAME, TOPIC_NAME, json.dumps({
            "order_id": ctx.workflow_id,
            "message": f"[RETURN] {message}",
            "data-content-type": "application/json"
        }))

# Business Logic Activities (Renamed for Clarity)
def validate_return_eligibility(_, return_request: ReturnRequest) -> ValidationResult:
    """Activity to validate if a return request is eligible"""
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    logging.info(f"Validating return request: {return_request}")

    # Check if return is within 30-day window
    try:
        requested_date = datetime.fromisoformat(return_request.requested_date.replace('Z', '+00:00'))
        days_since_request = (datetime.now().replace(tzinfo=requested_date.tzinfo) - requested_date).days

        if days_since_request > 30:
            return ValidationResult(
                valid=False,
                message="Return request is outside the 30-day return window",
                requires_approval=False
            )
    except:
        # If date parsing fails, assume it's valid
        pass

    # Check if high-value item requires approval
    requires_approval = return_request.return_value > 500.0

    # Always approve for demo purposes, but flag high-value items
    return ValidationResult(
        valid=True,
        message="Return request is valid",
        requires_approval=requires_approval
    )

def process_return_refund(_, return_request: ReturnRequest) -> RefundResult:
    """Activity to process refund through payments service"""
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    logging.info(f"Processing refund for return: {return_request}")

    # In a real system, we would check the original order first
    # For demo, we'll directly process the refund
    with DaprClient() as d:
        try:
            resp = d.invoke_method(
                "payments",
                f"api/v1/payments/{return_request.original_order_id}/refunds",
                http_verb="POST",
                data=json.dumps({
                    "id": return_request.id,
                    "original_order_id": return_request.original_order_id,
                    "amount": return_request.return_value,
                    "reason": return_request.reason
                })
            )

            if resp.status_code == 200:
                return RefundResult(
                    id=return_request.id,
                    success=True,
                    message="Refund processed successfully",
                    amount=return_request.return_value
                )
            else:
                return RefundResult(
                    id=return_request.id,
                    success=False,
                    message=f"Refund failed with status {resp.status_code}",
                    amount=0.0
                )

        except Exception as e:
            logging.error(f"Error processing refund: {str(e)}")
            return RefundResult(
                id=return_request.id,
                success=False,
                message=f"Refund processing error: {str(e)}",
                amount=0.0
            )

def restock_returned_inventory(_, return_request: ReturnRequest) -> bool:
    """Activity to restock inventory for returned items"""
    if isinstance(return_request, dict):
        return_request = ReturnRequest(**return_request)

    logging.info(f"Restocking inventory for return: {return_request}")

    # For demo purposes, we'll always succeed
    # In a real system, this would call the inventory service to add back stock
    try:
        # Could call inventory service here to increment stock
        logging.info(f"Successfully restocked {return_request.item}")
        return True
    except Exception as e:
        logging.error(f"Error restocking inventory: {str(e)}")
        return False

# Helper Functions
def determine_return_type(reason: str) -> str:
    """Determine return processing type based on reason"""
    if reason in [ReturnReason.DEFECTIVE.value, ReturnReason.DAMAGED_SHIPPING.value]:
        return "defective"
    elif reason == ReturnReason.CHANGED_MIND.value:
        return "expedited"  # Fast processing for changed mind
    else:
        return "standard"

# API Endpoints
@app.route("/returns", methods=["POST"])
def submit_return_request():
    """Submit a new return request"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Invalid request. Expected JSON body"}), 400

    required_fields = ["original_order_id", "customer", "item", "reason", "return_value"]
    for field in required_fields:
        if not request_data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Generate unique return ID
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return_id = f"return_{request_data['customer'].lower()}_{random_suffix}"

    return_request = ReturnRequest(
        id=return_id,
        original_order_id=request_data["original_order_id"],
        customer=request_data["customer"],
        item=request_data["item"],
        reason=request_data["reason"],
        description=request_data.get("description", ""),
        return_value=float(request_data["return_value"]),
        requested_date=datetime.now().isoformat()
    )

    try:
        wf_client = wf.DaprWorkflowClient()
        instance_id = wf_client.schedule_new_workflow(
            process_return_workflow,
            input=return_request,
            instance_id=return_id
        )

        logging.info(f"Started return workflow: {instance_id}")

        return jsonify({
            "instance_id": instance_id,
            "return_id": return_id,
            "original_order_id": return_request.original_order_id,
            "return_value": return_request.return_value
        }), 202, {
            'Content-Type': 'application/json',
            'Location': url_for('check_return_status', return_id=instance_id, _external=True)
        }

    except Exception as e:
        logging.error(f"Error starting return workflow: {str(e)}")
        return jsonify({"error": f"Failed to start return processing: {str(e)}"}), 500

@app.route("/returns/<return_id>", methods=["GET"])
def check_return_status(return_id):
    """Check the status of a return request"""
    try:
        wf_client = wf.DaprWorkflowClient()
        state = wf_client.get_workflow_state(return_id)

        if not state:
            return jsonify({"error": f"Return not found: {escape(return_id)}"}), 404

        # Parse the input to get return details
        return_info = json.loads(state.serialized_input)

        response = {
            "id": state.instance_id,
            "status": state.runtime_status.name,
            "created_time": state.created_at.isoformat(),
            "last_updated_time": state.last_updated_at.isoformat(),
            "return_details": return_info
        }

        # Add result if workflow is completed
        if state.serialized_output:
            try:
                result_data = json.loads(state.serialized_output)
                response["return_result"] = result_data
            except json.JSONDecodeError:
                response["return_result"] = {"message": "Result parsing error"}

        # Add failure details if any
        if state.failure_details:
            response["failure_details"] = {
                "message": state.failure_details.message,
                "error_type": state.failure_details.error_type,
                "stack_trace": state.failure_details.stack_trace
            }

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error checking return status: {str(e)}")
        return jsonify({"error": f"Failed to check status: {str(e)}"}), 500

@app.route("/returns/<return_id>/approve", methods=["POST"])
def approve_return(return_id):
    """Approve a return request that requires manager approval"""
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
        wf_client.raise_workflow_event(return_id, "return_approval", data=approval)

        logging.info(f"Return approval sent for: {return_id} by {approval.approver}")

        return jsonify({
            "message": f"Approval sent for return: {escape(return_id)}",
            "return_id": escape(return_id),
            "approver": escape(approval.approver),
            "approved": approval.approved
        }), 200

    except Exception as e:
        logging.error(f"Error sending return approval: {str(e)}")
        return jsonify({"error": f"Failed to send approval: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({
        "service": "returns-service",
        "status": "healthy",
        "version": "1.0.0"
    })

def main():
    # Start the workflow runtime with auto-reconnection
    logging.info("Starting returns workflow runtime...")
    wf_runtime = ResilientWorkflowRuntime(
        reconnect_delay_seconds=2.0,
        health_check_interval_seconds=10.0
    )
    wf_runtime.register_workflow(process_return_workflow)
    wf_runtime.register_workflow(process_defective_return_workflow)
    wf_runtime.register_workflow(process_standard_return_workflow)
    wf_runtime.register_workflow(process_expedited_return_workflow)

    # Register main workflow notification activities
    wf_runtime.register_activity(announce_return_request_received)
    wf_runtime.register_activity(announce_return_details_logged)
    wf_runtime.register_activity(announce_return_validation_started)
    wf_runtime.register_activity(announce_return_validation_passed)
    wf_runtime.register_activity(announce_return_validation_failed)
    wf_runtime.register_activity(announce_return_approval_required)
    wf_runtime.register_activity(announce_return_approval_received)
    wf_runtime.register_activity(announce_return_approval_rejected)
    wf_runtime.register_activity(announce_return_approval_timeout)
    wf_runtime.register_activity(announce_return_type_determination)
    wf_runtime.register_activity(announce_return_child_workflow_spawned)
    wf_runtime.register_activity(announce_return_processing_completed)
    wf_runtime.register_activity(announce_return_processing_failed)
    wf_runtime.register_activity(announce_return_refund_summary)
    wf_runtime.register_activity(announce_return_inventory_summary)

    # Register defective return notification activities
    wf_runtime.register_activity(announce_defective_return_started)
    wf_runtime.register_activity(announce_defective_refund_processing)
    wf_runtime.register_activity(announce_defective_refund_failed)
    wf_runtime.register_activity(announce_defective_return_completed)

    # Register standard return notification activities
    wf_runtime.register_activity(announce_standard_return_started)
    wf_runtime.register_activity(announce_standard_refund_processing)
    wf_runtime.register_activity(announce_standard_refund_failed)
    wf_runtime.register_activity(announce_standard_restocking_started)
    wf_runtime.register_activity(announce_standard_restocking_warning)
    wf_runtime.register_activity(announce_standard_return_completed)

    # Register expedited return notification activities
    wf_runtime.register_activity(announce_expedited_return_started)
    wf_runtime.register_activity(announce_expedited_parallel_processing)
    wf_runtime.register_activity(announce_expedited_refund_failed)
    wf_runtime.register_activity(announce_expedited_return_completed)

    # Register business logic activities
    wf_runtime.register_activity(validate_return_eligibility)
    wf_runtime.register_activity(process_return_refund)
    wf_runtime.register_activity(restock_returned_inventory)

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
