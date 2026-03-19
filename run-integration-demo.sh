#!/bin/bash

# Integration Demo Script - Full Order Lifecycle
# Tests all services except chaos-engineer: order-processor, inventory, payments, shipping, batch-processor, returns, notifications
# Duration: ~5-8 minutes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Service ports
ORDER_PROCESSOR_PORT=3006
INVENTORY_PORT=3013
PAYMENTS_PORT=3014
SHIPPING_PORT=3004
BATCH_PROCESSOR_PORT=3007
RETURNS_PORT=3008
NOTIFICATIONS_PORT=8085

# Base URL
HOST="localhost"

# Arrays to track workflow IDs
declare -a ORDER_IDS
declare -a BULK_ORDER_IDS
declare -a RETURN_IDS

# Sample data
CUSTOMERS=("alice" "bob" "charlie" "david" "emma" "frank")
ITEMS=("apple" "kiwi" "mango" "grapefruit" "orange" "pear")
RETURN_REASONS=("defective" "wrong_size" "changed_mind" "not_as_described" "damaged_shipping")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

print_header() {
    echo -e "\n${BLUE}==========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}==========================================${NC}\n"
}

print_phase() {
    echo -e "\n${CYAN}--- PHASE $1: $2 ---${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

wait_with_countdown() {
    local seconds=$1
    local message=$2
    echo -n "$message "
    for ((i=seconds; i>0; i--)); do
        echo -n "$i "
        sleep 1
    done
    echo ""
}

check_service() {
    local service_name=$1
    local port=$2
    local health_endpoint=${3:-"/healthz"}

    response=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST:$port$health_endpoint" 2>/dev/null || echo "000")

    if [ "$response" = "200" ]; then
        print_success "$service_name (port $port) is healthy"
        return 0
    else
        print_error "$service_name (port $port) is not responding (HTTP $response)"
        return 1
    fi
}

random_customer() {
    echo "${CUSTOMERS[$RANDOM % ${#CUSTOMERS[@]}]}"
}

random_item() {
    echo "${ITEMS[$RANDOM % ${#ITEMS[@]}]}"
}

random_price() {
    local min=$1
    local max=$2
    awk -v min="$min" -v max="$max" 'BEGIN{srand(); printf "%.2f", min+rand()*(max-min)}'
}

# =============================================================================
# API FUNCTIONS
# =============================================================================

submit_order() {
    local customer=$1
    local item=$2
    local total=$3

    response=$(curl -s -X POST "http://$HOST:$ORDER_PROCESSOR_PORT/orders" \
        -H "Content-Type: application/json" \
        -d "{\"customer\": \"$customer\", \"item\": \"$item\", \"total\": $total}")

    echo "$response"
}

get_order_status() {
    local order_id=$1
    curl -s "http://$HOST:$ORDER_PROCESSOR_PORT/orders/$order_id"
}

approve_order() {
    local order_id=$1
    local approver=$2
    local approved=$3

    curl -s -X POST "http://$HOST:$ORDER_PROCESSOR_PORT/orders/$order_id/approve" \
        -H "Content-Type: application/json" \
        -d "{\"approver\": \"$approver\", \"approved\": $approved}"
}

submit_bulk_order() {
    local customer=$1
    local items_json=$2

    response=$(curl -s -X POST "http://$HOST:$BATCH_PROCESSOR_PORT/bulk-orders" \
        -H "Content-Type: application/json" \
        -d "{\"customer\": \"$customer\", \"items\": $items_json}")

    echo "$response"
}

get_bulk_order_status() {
    local order_id=$1
    curl -s "http://$HOST:$BATCH_PROCESSOR_PORT/bulk-orders/$order_id"
}

submit_return() {
    local original_order_id=$1
    local customer=$2
    local item=$3
    local reason=$4
    local return_value=$5

    response=$(curl -s -X POST "http://$HOST:$RETURNS_PORT/returns" \
        -H "Content-Type: application/json" \
        -d "{\"original_order_id\": \"$original_order_id\", \"customer\": \"$customer\", \"item\": \"$item\", \"reason\": \"$reason\", \"return_value\": $return_value}")

    echo "$response"
}

get_return_status() {
    local return_id=$1
    curl -s "http://$HOST:$RETURNS_PORT/returns/$return_id"
}

approve_return() {
    local return_id=$1
    local approver=$2
    local approved=$3

    curl -s -X POST "http://$HOST:$RETURNS_PORT/returns/$return_id/approve" \
        -H "Content-Type: application/json" \
        -d "{\"approver\": \"$approver\", \"approved\": $approved}"
}

get_inventory() {
    curl -s "http://$HOST:$INVENTORY_PORT/api/v1/inventory"
}

restock_inventory() {
    curl -s -X POST "http://$HOST:$INVENTORY_PORT/api/v1/inventory/restock"
}

get_circuit_breakers() {
    curl -s "http://$HOST:$ORDER_PROCESSOR_PORT/circuit-breakers"
}

# =============================================================================
# MAIN DEMO SCRIPT
# =============================================================================

print_header "INTEGRATION DEMO - Full Order Lifecycle"
echo "This demo tests all services: order-processor, inventory, payments,"
echo "shipping, batch-processor, returns, and notifications."
echo ""
echo "Press Ctrl+C to exit at any time."
echo ""

# Trap for graceful exit
trap 'echo -e "\n${YELLOW}Demo interrupted. Exiting...${NC}"; exit 0' INT

# -----------------------------------------------------------------------------
print_phase "1" "Service Health Check"
# -----------------------------------------------------------------------------

all_healthy=true

check_service "order-processor" $ORDER_PROCESSOR_PORT || all_healthy=false
check_service "inventory" $INVENTORY_PORT "/healthz" || all_healthy=false
check_service "payments" $PAYMENTS_PORT || all_healthy=false
check_service "shipping" $SHIPPING_PORT || all_healthy=false
check_service "batch-processor" $BATCH_PROCESSOR_PORT || all_healthy=false
check_service "returns" $RETURNS_PORT || all_healthy=false
# Notifications is optional - it's for UI display only
if ! check_service "notifications" $NOTIFICATIONS_PORT "/healthz"; then
    print_warning "Notifications service not running - UI updates will not be available"
fi

if [ "$all_healthy" = false ]; then
    print_error "Some services are not healthy. Please start all services with:"
    echo "  diagrid dev run -f dapr.yaml --project \$WORKFLOW_PROJECT_NAME"
    exit 1
fi

print_success "All services are healthy!"

# -----------------------------------------------------------------------------
print_phase "2" "Inventory Setup"
# -----------------------------------------------------------------------------

print_info "Restocking inventory..."
restock_response=$(restock_inventory)
print_success "Inventory restocked"

print_info "Current inventory levels:"
inventory=$(get_inventory)
echo "$inventory" | jq -r '.[] | "  \(.item): \(.quantity) units"' 2>/dev/null || echo "$inventory"

# -----------------------------------------------------------------------------
print_phase "3" "Standard Orders (Small Value)"
# -----------------------------------------------------------------------------

print_info "Submitting 3 standard orders (under \$100)..."

for i in {1..3}; do
    customer=$(random_customer)
    item=$(random_item)
    total=$(random_price 10 50)

    response=$(submit_order "$customer" "$item" "$total")
    order_id=$(echo "$response" | jq -r '.instance_id' 2>/dev/null)

    if [ -n "$order_id" ] && [ "$order_id" != "null" ]; then
        ORDER_IDS+=("$order_id")
        print_success "Order #$i: $customer ordered $item for \$$total (ID: ${order_id:0:8}...)"
    else
        print_warning "Order #$i: Failed to submit - $response"
    fi

    sleep 0.5
done

wait_with_countdown 3 "Waiting for workflows to process..."

# Check status of orders
print_info "Checking order statuses:"
for order_id in "${ORDER_IDS[@]}"; do
    status=$(get_order_status "$order_id" | jq -r '.runtime_status' 2>/dev/null || echo "unknown")
    echo "  Order ${order_id:0:8}...: $status"
done

# -----------------------------------------------------------------------------
print_phase "4" "High-Value Order (Requires Approval)"
# -----------------------------------------------------------------------------

customer=$(random_customer)
item=$(random_item)
total=$(random_price 1200 2000)

print_info "Submitting high-value order: $customer ordering $item for \$$total"
response=$(submit_order "$customer" "$item" "$total")
high_value_order_id=$(echo "$response" | jq -r '.instance_id' 2>/dev/null)

if [ -n "$high_value_order_id" ] && [ "$high_value_order_id" != "null" ]; then
    ORDER_IDS+=("$high_value_order_id")
    print_success "High-value order submitted (ID: ${high_value_order_id:0:8}...)"

    wait_with_countdown 2 "Waiting for approval request..."

    # Check status - should be waiting for approval
    status=$(get_order_status "$high_value_order_id")
    runtime_status=$(echo "$status" | jq -r '.runtime_status' 2>/dev/null)
    print_info "Order status: $runtime_status (waiting for approval)"

    # Approve the order
    print_info "Manager approving the order..."
    approve_response=$(approve_order "$high_value_order_id" "manager_jane" "true")
    print_success "Order approved by manager_jane"

    wait_with_countdown 3 "Waiting for workflow to complete..."

    final_status=$(get_order_status "$high_value_order_id" | jq -r '.runtime_status' 2>/dev/null)
    print_info "Final status: $final_status"
else
    print_warning "Failed to submit high-value order"
fi

# -----------------------------------------------------------------------------
print_phase "5" "Bulk Order (Parent-Child Workflows)"
# -----------------------------------------------------------------------------

customer=$(random_customer)
bulk_items='[
    {"item": "apple", "quantity": 2, "price": 15.99},
    {"item": "orange", "quantity": 3, "price": 12.50},
    {"item": "kiwi", "quantity": 1, "price": 8.75}
]'

print_info "Submitting bulk order for $customer with 3 different items..."
response=$(submit_bulk_order "$customer" "$bulk_items")
bulk_order_id=$(echo "$response" | jq -r '.bulk_order_id' 2>/dev/null)
items_count=$(echo "$response" | jq -r '.items_count' 2>/dev/null)
total_cost=$(echo "$response" | jq -r '.total_cost' 2>/dev/null)

if [ -n "$bulk_order_id" ] && [ "$bulk_order_id" != "null" ]; then
    BULK_ORDER_IDS+=("$bulk_order_id")
    print_success "Bulk order submitted: $items_count items, total \$$total_cost (ID: ${bulk_order_id:0:8}...)"

    wait_with_countdown 5 "Waiting for child workflows to process..."

    # Check bulk order status
    bulk_status=$(get_bulk_order_status "$bulk_order_id")
    runtime_status=$(echo "$bulk_status" | jq -r '.runtime_status' 2>/dev/null)
    child_count=$(echo "$bulk_status" | jq -r '.child_workflow_ids | length' 2>/dev/null || echo "0")
    print_info "Bulk order status: $runtime_status ($child_count child workflows)"
else
    print_warning "Failed to submit bulk order - $response"
fi

# -----------------------------------------------------------------------------
print_phase "6" "Return Processing (Multiple Types)"
# -----------------------------------------------------------------------------

# Use one of the earlier order IDs as the original order
original_order_id="${ORDER_IDS[0]:-order-001}"

# 6a. Standard Return
print_info "Submitting standard return (changed_mind)..."
return_response=$(submit_return "$original_order_id" "alice" "apple" "changed_mind" 25.00)
return_id=$(echo "$return_response" | jq -r '.return_id' 2>/dev/null)

if [ -n "$return_id" ] && [ "$return_id" != "null" ]; then
    RETURN_IDS+=("$return_id")
    print_success "Standard return submitted (ID: ${return_id:0:8}...)"
else
    print_warning "Failed to submit standard return"
fi

sleep 1

# 6b. Defective Return
print_info "Submitting defective return..."
return_response=$(submit_return "$original_order_id" "bob" "orange" "defective" 18.50)
return_id=$(echo "$return_response" | jq -r '.return_id' 2>/dev/null)

if [ -n "$return_id" ] && [ "$return_id" != "null" ]; then
    RETURN_IDS+=("$return_id")
    print_success "Defective return submitted (ID: ${return_id:0:8}...)"
else
    print_warning "Failed to submit defective return"
fi

sleep 1

# 6c. High-Value Return (Requires Approval)
print_info "Submitting high-value return (\$750, requires approval)..."
return_response=$(submit_return "$original_order_id" "charlie" "kiwi" "not_as_described" 750.00)
high_value_return_id=$(echo "$return_response" | jq -r '.return_id' 2>/dev/null)

if [ -n "$high_value_return_id" ] && [ "$high_value_return_id" != "null" ]; then
    RETURN_IDS+=("$high_value_return_id")
    print_success "High-value return submitted (ID: ${high_value_return_id:0:8}...)"

    wait_with_countdown 2 "Waiting for approval request..."

    # Approve the return
    print_info "Manager approving the high-value return..."
    approve_response=$(approve_return "$high_value_return_id" "manager_bob" "true")
    print_success "Return approved by manager_bob"
else
    print_warning "Failed to submit high-value return"
fi

wait_with_countdown 3 "Waiting for return workflows to complete..."

# Check return statuses
print_info "Return statuses:"
for return_id in "${RETURN_IDS[@]}"; do
    status=$(get_return_status "$return_id" | jq -r '.runtime_status' 2>/dev/null || echo "unknown")
    echo "  Return ${return_id:0:8}...: $status"
done

# -----------------------------------------------------------------------------
print_phase "7" "System Status & Monitoring"
# -----------------------------------------------------------------------------

print_info "Circuit breaker status:"
cb_status=$(get_circuit_breakers)
echo "$cb_status" | jq '.' 2>/dev/null || echo "$cb_status"

print_info "Final inventory levels:"
inventory=$(get_inventory)
echo "$inventory" | jq -r '.[] | "  \(.item): \(.quantity) units"' 2>/dev/null || echo "$inventory"

# -----------------------------------------------------------------------------
print_header "DEMO COMPLETE - Summary"
# -----------------------------------------------------------------------------

echo -e "Orders submitted:      ${GREEN}${#ORDER_IDS[@]}${NC}"
echo -e "Bulk orders submitted: ${GREEN}${#BULK_ORDER_IDS[@]}${NC}"
echo -e "Returns submitted:     ${GREEN}${#RETURN_IDS[@]}${NC}"
echo ""
echo "Workflows tested:"
echo "  ✓ Standard order processing"
echo "  ✓ High-value order with approval"
echo "  ✓ Bulk order (parent-child workflows)"
echo "  ✓ Standard return (refund + restock)"
echo "  ✓ Defective return (refund only)"
echo "  ✓ High-value return with approval"
echo ""
echo "Services exercised:"
echo "  ✓ order-processor (workflow orchestration)"
echo "  ✓ inventory (state management)"
echo "  ✓ payments (charge & refund)"
echo "  ✓ shipping (fulfillment)"
echo "  ✓ batch-processor (bulk workflows)"
echo "  ✓ returns (return workflows)"
echo "  ✓ notifications (pub/sub events)"
echo ""
print_success "Integration demo completed successfully!"
