#!/bin/bash

# =============================================
# SAGA DEMO SCRIPT
# =============================================
# PURPOSE: Automated demonstration of advanced Dapr workflow patterns
# DURATION: ~10-15 minutes for full demonstration
# PATTERNS: Saga with compensation, Continue-as-new, Multi-level workflows
# =============================================
#  Usage:
#   # Full demo (~10-15 min)
#   ./run-saga-demo.sh

#   # Quick mode (halves wait times)
#   ./run-saga-demo.sh -q

#   # Skip monitor demo
#   ./run-saga-demo.sh -s

#   # Quick + skip monitor
#   ./run-saga-demo.sh -qs

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SAGA_SERVICE="http://localhost:3009"
INVENTORY_SERVICE="http://localhost:3013"
NOTIFICATIONS_UI="http://localhost:8080"

# Default options
VERBOSE=true
SKIP_MONITOR=false
QUICK_MODE=false

# Parse command line arguments
while getopts "qsv" opt; do
  case $opt in
    q) QUICK_MODE=true ;;
    s) SKIP_MONITOR=true ;;
    v) VERBOSE=true ;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
  esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}     SAGA DEMO - Advanced Workflow Patterns     ${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to print step headers
print_step() {
    echo -e "\n${YELLOW}STEP $1: $2${NC}"
    echo "----------------------------------------"
}

# Function to print phase headers
print_phase() {
    echo -e "\n${MAGENTA}========================================${NC}"
    echo -e "${MAGENTA}  PHASE $1: $2${NC}"
    echo -e "${MAGENTA}========================================${NC}"
}

# Function to wait with countdown
wait_with_countdown() {
    local seconds=$1
    local message=$2
    if $QUICK_MODE; then
        seconds=$((seconds / 2))
    fi
    echo -e "${BLUE}$message${NC}"
    for ((i=seconds; i>=1; i--)); do
        echo -ne "\r   Waiting... ${i}s remaining"
        sleep 1
    done
    echo -ne "\r   Done!                    \n"
}

# Function to check if service is responding
check_service() {
    local url=$1
    local name=$2
    if curl -s "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}[OK] $name is responding${NC}"
        return 0
    else
        echo -e "${RED}[FAIL] $name is not responding at $url${NC}"
        return 1
    fi
}

# Function to submit saga order and display result
submit_saga_order() {
    local customer=$1
    local item=$2
    local total=$3
    local destination=$4
    local fail_at_step=$5
    local fail_type=$6
    local delay=$7
    local force_success=$8

    local payload="{\"customer\": \"$customer\", \"item\": \"$item\", \"total\": $total, \"destination\": \"$destination\""

    if [ -n "$fail_at_step" ]; then
        payload="$payload, \"fail_at_step\": \"$fail_at_step\""
    fi
    if [ -n "$fail_type" ]; then
        payload="$payload, \"fail_type\": \"$fail_type\""
    fi
    if [ -n "$delay" ] && [ "$delay" != "0" ]; then
        payload="$payload, \"simulate_delay_ms\": $delay"
    fi
    if [ "$force_success" = "true" ]; then
        payload="$payload, \"force_success\": true"
    fi

    payload="$payload}"

    if $VERBOSE; then
        echo -e "${CYAN}Request:${NC} $payload" >&2
    fi

    local response=$(curl -s -X POST "$SAGA_SERVICE/saga/orders" \
        -H "Content-Type: application/json" \
        -d "$payload")

    # Display response to stderr so it's visible but not captured
    echo "$response" | jq '.' >&2

    # Return only the instance_id to stdout for capture
    echo "$response" | jq -r '.instance_id'
}

# Function to check saga status
check_saga_status() {
    local order_id=$1
    echo -e "${CYAN}Checking status for: $order_id${NC}"
    curl -s "$SAGA_SERVICE/saga/orders/$order_id" | jq '.'
}

# =============================================
# PHASE 1: SYSTEM PREPARATION
# =============================================

print_phase "1" "SYSTEM PREPARATION"

print_step "1.1" "Checking Service Health"

echo "Checking saga-demo service availability..."
check_service "$SAGA_SERVICE/healthz" "Saga Demo Service"
check_service "$INVENTORY_SERVICE/api/v1/inventory" "Inventory Service"

print_step "1.2" "Restocking Inventory"

echo "Restocking inventory for demo..."
curl -s -X POST "$INVENTORY_SERVICE/api/v1/inventory/restock" | jq '.'

echo -e "\n${GREEN}System ready for saga demonstrations!${NC}"
echo -e "${YELLOW}TIP: Open notifications UI at $NOTIFICATIONS_UI to watch events${NC}"

wait_with_countdown 3 "Starting saga demonstrations..."

# =============================================
# PHASE 2: SAGA PATTERN - SUCCESS SCENARIO
# =============================================

print_phase "2" "SAGA PATTERN - SUCCESS SCENARIO"

print_step "2.1" "Submitting Successful Order"

echo "Submitting order that will complete all steps successfully..."
SAGA_SUCCESS_ID=$(submit_saga_order "Alice" "laptop" "999.99" "123 Main Street" "" "" "500" "")

wait_with_countdown 5 "Waiting for saga to complete..."

print_step "2.2" "Verifying Success"

check_saga_status "$SAGA_SUCCESS_ID"

echo -e "\n${GREEN}SUCCESS: Saga completed all 3 steps (reserve -> charge -> ship)${NC}"

# =============================================
# PHASE 3: SAGA PATTERN - FAILURE AT RESERVE
# =============================================

print_phase "3" "SAGA PATTERN - FAILURE AT RESERVE STEP"

print_step "3.1" "Submitting Order (Fail at Reserve)"

echo "Submitting order that will fail at inventory reservation..."
echo -e "${YELLOW}Expected: Failure at first step, no compensations needed${NC}"

SAGA_FAIL_RESERVE_ID=$(submit_saga_order "Bob" "phone" "599.99" "456 Oak Avenue" "reserve" "error" "500" "")

wait_with_countdown 4 "Waiting for saga to fail..."

print_step "3.2" "Verifying Failure (No Compensations)"

check_saga_status "$SAGA_FAIL_RESERVE_ID"

echo -e "\n${YELLOW}EXPECTED RESULT: Failure at reserve step, no compensations executed${NC}"

# =============================================
# PHASE 4: SAGA PATTERN - FAILURE AT CHARGE
# =============================================

print_phase "4" "SAGA PATTERN - FAILURE AT CHARGE STEP"

print_step "4.1" "Submitting Order (Fail at Charge)"

echo "Submitting order that will fail at payment step..."
echo -e "${YELLOW}Expected: Inventory reserved, then charge fails${NC}"
echo -e "${YELLOW}Compensation: release_inventory${NC}"

SAGA_FAIL_CHARGE_ID=$(submit_saga_order "Carol" "tablet" "399.99" "789 Pine Road" "charge" "unavailable" "500" "")

wait_with_countdown 5 "Waiting for saga to fail and compensate..."

print_step "4.2" "Verifying Compensation"

check_saga_status "$SAGA_FAIL_CHARGE_ID"

echo -e "\n${YELLOW}EXPECTED RESULT: 1 step completed, 1 compensation executed (release_inventory)${NC}"

# =============================================
# PHASE 5: SAGA PATTERN - FAILURE AT SHIP (FULL COMPENSATION)
# =============================================

print_phase "5" "SAGA PATTERN - FULL COMPENSATION CHAIN"

print_step "5.1" "Submitting Order (Fail at Ship)"

echo "Submitting order that will fail at shipping step..."
echo -e "${YELLOW}Expected: Inventory reserved, payment charged, then ship fails${NC}"
echo -e "${YELLOW}Compensations: refund_payment -> release_inventory${NC}"

SAGA_FAIL_SHIP_ID=$(submit_saga_order "David" "monitor" "299.99" "321 Elm Boulevard" "ship" "timeout" "500" "")

wait_with_countdown 6 "Waiting for saga to fail and run full compensation chain..."

print_step "5.2" "Verifying Full Compensation Chain"

check_saga_status "$SAGA_FAIL_SHIP_ID"

echo -e "\n${YELLOW}EXPECTED RESULT: 2 steps completed, 2 compensations executed${NC}"
echo -e "${YELLOW}Compensations run in reverse: refund_payment, then release_inventory${NC}"

# =============================================
# PHASE 6: SAGA PATTERN - FATAL FAILURE (NO COMPENSATION)
# =============================================

print_phase "6" "SAGA PATTERN - FATAL FAILURE (WORKFLOW FAILED)"

print_step "6.1" "Submitting Order (Fatal Failure at Charge)"

echo "Submitting order that will have a FATAL failure at charge step..."
echo -e "${RED}Expected: Inventory reserved, then FATAL failure at charge${NC}"
echo -e "${RED}Result: NO compensations, workflow marked as FAILED (rerunnable)${NC}"

SAGA_FATAL_ID=$(submit_saga_order "Fatal" "crash-test" "199.99" "777 Crash Lane" "charge" "fatal" "500" "")

wait_with_countdown 4 "Waiting for fatal failure..."

print_step "6.2" "Verifying Fatal Failure (No Compensations)"

check_saga_status "$SAGA_FATAL_ID"

echo -e "\n${RED}EXPECTED RESULT: Workflow status=FAILED, no compensations executed${NC}"
echo -e "${YELLOW}Unlike saga rollback, fatal failures can be rerun via Dapr workflow APIs${NC}"

# =============================================
# PHASE 7: SAGA PATTERN - FORCE SUCCESS
# =============================================

print_phase "7" "SAGA PATTERN - FORCE SUCCESS (RECOVERY)"

print_step "7.1" "Submitting Order with force_success Flag"

echo "Submitting order with failure config but force_success=true..."
echo -e "${YELLOW}Expected: Failure config ignored, order completes successfully${NC}"

SAGA_FORCE_ID=$(submit_saga_order "Eve" "keyboard" "149.99" "555 Tech Lane" "charge" "error" "500" "true")

wait_with_countdown 5 "Waiting for forced success..."

print_step "7.2" "Verifying Forced Success"

check_saga_status "$SAGA_FORCE_ID"

echo -e "\n${GREEN}SUCCESS: force_success flag bypassed the failure configuration${NC}"

# =============================================
# PHASE 8: CONTINUE-AS-NEW PATTERN
# =============================================

if ! $SKIP_MONITOR; then
    print_phase "8" "CONTINUE-AS-NEW PATTERN"

    # 8.1 - Success scenario
    print_step "8.1" "Monitor Success (No Failures)"

    echo "Starting monitor workflow with continue-as-new pattern..."
    echo -e "${YELLOW}This demonstrates workflow history management for long-running processes${NC}"

    MONITOR_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/monitor/start" \
        -H "Content-Type: application/json" \
        -d '{
            "order_id": "'"$SAGA_SUCCESS_ID"'",
            "check_interval_seconds": 2,
            "max_checks": 4
        }')

    echo "$MONITOR_RESPONSE" | jq '.'
    MONITOR_SUCCESS_ID=$(echo "$MONITOR_RESPONSE" | jq -r '.monitor_id')

    wait_with_countdown 10 "Waiting for monitor iterations (observe history resets in Catalyst UI)..."

    echo "Final monitor status:"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_SUCCESS_ID" | jq '.'

    echo -e "\n${GREEN}COMPLETE: Monitor completed all checks with history resets${NC}"

    # 8.2 - Service Error failure
    print_step "8.2" "Monitor Failure - Service Error"

    echo "Starting monitor that will encounter a service error..."
    echo -e "${YELLOW}Expected: Monitor runs 2 checks, then status check service becomes unavailable${NC}"

    MONITOR_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/monitor/start" \
        -H "Content-Type: application/json" \
        -d '{
            "order_id": "'"$SAGA_SUCCESS_ID"'",
            "check_interval_seconds": 2,
            "max_checks": 5,
            "fail_at_iteration": 3,
            "fail_reason": "service_error"
        }')

    echo "$MONITOR_RESPONSE" | jq '.'
    MONITOR_SVC_ERR_ID=$(echo "$MONITOR_RESPONSE" | jq -r '.monitor_id')

    wait_with_countdown 8 "Waiting for monitor to fail at iteration 3..."

    echo "Monitor status:"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_SVC_ERR_ID" | jq '.'

    echo -e "\n${YELLOW}EXPECTED RESULT: Monitor failed with service_error at iteration 3${NC}"

    # 8.3 - Order Lost failure
    print_step "8.3" "Monitor Failure - Order Lost"

    echo "Starting monitor that will discover the order is missing..."
    echo -e "${YELLOW}Expected: Monitor runs 1 check, then order disappears from system${NC}"

    MONITOR_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/monitor/start" \
        -H "Content-Type: application/json" \
        -d '{
            "order_id": "'"$SAGA_SUCCESS_ID"'",
            "check_interval_seconds": 2,
            "max_checks": 5,
            "fail_at_iteration": 2,
            "fail_reason": "order_lost"
        }')

    echo "$MONITOR_RESPONSE" | jq '.'
    MONITOR_LOST_ID=$(echo "$MONITOR_RESPONSE" | jq -r '.monitor_id')

    wait_with_countdown 6 "Waiting for monitor to detect lost order..."

    echo "Monitor status:"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_LOST_ID" | jq '.'

    echo -e "\n${YELLOW}EXPECTED RESULT: Monitor failed with order_lost at iteration 2${NC}"

    # 8.4 - Stuck Order failure
    print_step "8.4" "Monitor Failure - Stuck Order"

    echo "Starting monitor that will detect a stuck order..."
    echo -e "${YELLOW}Expected: Monitor runs 3 checks, then detects order is stuck in processing${NC}"

    MONITOR_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/monitor/start" \
        -H "Content-Type: application/json" \
        -d '{
            "order_id": "'"$SAGA_SUCCESS_ID"'",
            "check_interval_seconds": 2,
            "max_checks": 6,
            "fail_at_iteration": 4,
            "fail_reason": "stuck"
        }')

    echo "$MONITOR_RESPONSE" | jq '.'
    MONITOR_STUCK_ID=$(echo "$MONITOR_RESPONSE" | jq -r '.monitor_id')

    wait_with_countdown 10 "Waiting for monitor to detect stuck order..."

    echo "Monitor status:"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_STUCK_ID" | jq '.'

    echo -e "\n${YELLOW}EXPECTED RESULT: Monitor failed with stuck at iteration 4${NC}"

    # 8.5 - Timeout failure
    print_step "8.5" "Monitor Failure - Timeout"

    echo "Starting monitor that will timeout..."
    echo -e "${YELLOW}Expected: Monitor runs 1 check, then exceeds timeout threshold${NC}"

    MONITOR_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/monitor/start" \
        -H "Content-Type: application/json" \
        -d '{
            "order_id": "'"$SAGA_SUCCESS_ID"'",
            "check_interval_seconds": 2,
            "max_checks": 5,
            "fail_at_iteration": 2,
            "fail_reason": "timeout"
        }')

    echo "$MONITOR_RESPONSE" | jq '.'
    MONITOR_TIMEOUT_ID=$(echo "$MONITOR_RESPONSE" | jq -r '.monitor_id')

    wait_with_countdown 6 "Waiting for monitor to timeout..."

    echo "Monitor status:"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_TIMEOUT_ID" | jq '.'

    echo -e "\n${YELLOW}EXPECTED RESULT: Monitor failed with timeout at iteration 2${NC}"

    # 8.6 - Summary comparison
    print_step "8.6" "Monitor Results Comparison"

    echo -e "${CYAN}Success:${NC}"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_SUCCESS_ID" | jq '{status: .status, iterations: .result.iterations_completed, final_status: .result.final_status, failed: .result.failed}'

    echo -e "\n${CYAN}Service Error:${NC}"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_SVC_ERR_ID" | jq '{status: .status, iterations: .result.iterations_completed, final_status: .result.final_status, failed: .result.failed, fail_reason: .result.fail_reason}'

    echo -e "\n${CYAN}Order Lost:${NC}"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_LOST_ID" | jq '{status: .status, iterations: .result.iterations_completed, final_status: .result.final_status, failed: .result.failed, fail_reason: .result.fail_reason}'

    echo -e "\n${CYAN}Stuck Order:${NC}"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_STUCK_ID" | jq '{status: .status, iterations: .result.iterations_completed, final_status: .result.final_status, failed: .result.failed, fail_reason: .result.fail_reason}'

    echo -e "\n${CYAN}Timeout:${NC}"
    curl -s "$SAGA_SERVICE/monitor/$MONITOR_TIMEOUT_ID" | jq '{status: .status, iterations: .result.iterations_completed, final_status: .result.final_status, failed: .result.failed, fail_reason: .result.fail_reason}'

    echo -e "\n${GREEN}COMPLETE: Monitor demonstrated continue-as-new with 4 failure scenarios${NC}"
else
    echo -e "\n${YELLOW}Skipping monitor demo (use without -s flag to include)${NC}"
fi

# =============================================
# PHASE 9: MULTI-LEVEL WORKFLOWS
# =============================================

print_phase "9" "MULTI-LEVEL WORKFLOW HIERARCHY"

print_step "9.1" "Submitting Fulfillment Order"

echo "Submitting order for multi-level workflow processing..."
echo -e "${CYAN}Workflow Hierarchy:${NC}"
echo "  Parent: fulfillment_workflow"
echo "    Child: validation_workflow"
echo "      Grandchild: address_check_workflow (parallel)"
echo "      Grandchild: payment_check_workflow (parallel)"

FULFILLMENT_RESPONSE=$(curl -s -X POST "$SAGA_SERVICE/fulfillment/orders" \
    -H "Content-Type: application/json" \
    -d '{
        "customer": "Frank",
        "item": "headphones",
        "total": 199.99,
        "destination": "888 Audio Drive, Building C"
    }')

echo "$FULFILLMENT_RESPONSE" | jq '.'
FULFILLMENT_ID=$(echo "$FULFILLMENT_RESPONSE" | jq -r '.instance_id')

wait_with_countdown 5 "Waiting for multi-level workflow to complete..."

print_step "9.2" "Verifying Workflow Hierarchy"

echo "Parent workflow status:"
curl -s "$SAGA_SERVICE/fulfillment/orders/$FULFILLMENT_ID" | jq '.'

echo -e "\n${GREEN}COMPLETE: Multi-level workflow executed with parallel grandchildren${NC}"

# =============================================
# PHASE 10: RERUN DEMONSTRATION
# =============================================

print_phase "10" "RERUN DEMONSTRATION"

print_step "10.1" "Same Order - Three Different Outcomes"

echo "Demonstrating deterministic behavior with input-driven failures..."
echo ""

echo -e "${CYAN}Run 1: Success (no failure config)${NC}"
RERUN1_ID=$(submit_saga_order "RerunDemo" "speaker" "249.99" "111 Demo Lane" "" "" "300" "")
wait_with_countdown 3 "Processing..."

echo -e "\n${CYAN}Run 2: Fail at charge (with compensation)${NC}"
RERUN2_ID=$(submit_saga_order "RerunDemo" "speaker" "249.99" "111 Demo Lane" "charge" "error" "300" "")
wait_with_countdown 3 "Processing..."

echo -e "\n${CYAN}Run 3: Force success (recovery)${NC}"
RERUN3_ID=$(submit_saga_order "RerunDemo" "speaker" "249.99" "111 Demo Lane" "charge" "error" "300" "true")
wait_with_countdown 3 "Processing..."

print_step "10.2" "Comparing Results"

echo -e "${CYAN}Run 1 Result:${NC}"
curl -s "$SAGA_SERVICE/saga/orders/$RERUN1_ID" | jq '{status: .status, success: .result.success, steps: .result.steps_completed, compensations: .result.compensations_executed}'

echo -e "\n${CYAN}Run 2 Result:${NC}"
curl -s "$SAGA_SERVICE/saga/orders/$RERUN2_ID" | jq '{status: .status, success: .result.success, steps: .result.steps_completed, compensations: .result.compensations_executed}'

echo -e "\n${CYAN}Run 3 Result:${NC}"
curl -s "$SAGA_SERVICE/saga/orders/$RERUN3_ID" | jq '{status: .status, success: .result.success, steps: .result.steps_completed, compensations: .result.compensations_executed}'

echo -e "\n${GREEN}COMPLETE: Same order, three different outcomes based on input configuration${NC}"

# =============================================
# DEMO SUMMARY
# =============================================

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}          SAGA DEMO COMPLETE!                   ${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\n${BLUE}Demo Summary:${NC}"
echo "  [Phase 2] Saga Success: All 3 steps completed"
echo "  [Phase 3] Fail at Reserve: No compensations needed"
echo "  [Phase 4] Fail at Charge: 1 compensation (release_inventory)"
echo "  [Phase 5] Fail at Ship: 2 compensations (refund + release)"
echo "  [Phase 6] Fatal Failure: Workflow FAILED, no compensations (rerunnable)"
echo "  [Phase 7] Force Success: Bypassed failure configuration"
if ! $SKIP_MONITOR; then
echo "  [Phase 8] Continue-As-New: Success + 4 failure scenarios (service_error, order_lost, stuck, timeout)"
fi
echo "  [Phase 9] Multi-Level: Parent -> Child -> Grandchildren (parallel)"
echo "  [Phase 10] Rerun Demo: Same input, different outcomes"

echo -e "\n${YELLOW}Workflow IDs for Reference:${NC}"
echo "  Saga Success:    $SAGA_SUCCESS_ID"
echo "  Fail Reserve:    $SAGA_FAIL_RESERVE_ID"
echo "  Fail Charge:     $SAGA_FAIL_CHARGE_ID"
echo "  Fail Ship:       $SAGA_FAIL_SHIP_ID"
echo "  Fatal Failure:   $SAGA_FATAL_ID"
echo "  Force Success:   $SAGA_FORCE_ID"
if ! $SKIP_MONITOR; then
echo "  Monitor Success: $MONITOR_SUCCESS_ID"
echo "  Monitor SvcErr:  $MONITOR_SVC_ERR_ID"
echo "  Monitor Lost:    $MONITOR_LOST_ID"
echo "  Monitor Stuck:   $MONITOR_STUCK_ID"
echo "  Monitor Timeout: $MONITOR_TIMEOUT_ID"
fi
echo "  Fulfillment:     $FULFILLMENT_ID"

echo -e "\n${YELLOW}Next Steps:${NC}"
echo "  - Review workflows in Diagrid Catalyst UI"
echo "  - Check notifications at $NOTIFICATIONS_UI"
echo "  - Run individual scenarios with saga-demo.http"
echo "  - Try different failure combinations"

echo -e "\n${GREEN}Demo completed successfully!${NC}"
echo ""
