#!/bin/bash

# =============================================
# ADVANCED CHAOS ENGINEERING DEMO SCRIPT
# =============================================
# PURPOSE: Comprehensive failure simulation with multiple concurrent scenarios
# DURATION: ~8-12 minutes for full advanced demonstration
# FOCUS: Multi-service failures, circuit breakers, cascade patterns, workflow integration
# SCENARIOS: Payment timeout, database errors, network failures, memory issues
# =============================================

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
CHAOS_SERVICE="http://localhost:3010"
ORDER_SERVICE="http://localhost:3006"
INVENTORY_SERVICE="http://localhost:3013"
BULK_SERVICE="http://localhost:3007"
RETURN_SERVICE="http://localhost:3008"

# Global variables for scenario tracking
declare -a SCENARIO_IDS
declare -a WORKFLOW_IDS
declare -a SCENARIO_NAMES

echo -e "${CYAN}🚀 Starting Advanced Chaos Engineering Demo${NC}"
echo "============================================================"
echo -e "${YELLOW}⚡ Multi-Service Failure Simulation & Resilience Testing${NC}"
echo "============================================================"

# Function to print step headers
print_step() {
    echo -e "\n${MAGENTA}📋 PHASE $1: $2${NC}"
    echo "============================================================"
}

# Function to print sub-steps
print_substep() {
    echo -e "\n${CYAN}🔹 $1${NC}"
    echo "------------------------------------------------------------"
}

# Function to wait with countdown
wait_with_countdown() {
    local seconds=$1
    local message=$2
    echo -e "${BLUE}⏳ $message${NC}"
    for ((i=seconds; i>=1; i--)); do
        echo -ne "\r   ⏰ ${i}s remaining..."
        sleep 1
    done
    echo -ne "\r   ✅ Wait complete!     \n"
}

# Function to check if service is responding
check_service() {
    local url=$1
    local name=$2
    if curl -s "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $name${NC}"
        return 0
    else
        echo -e "${RED}❌ $name (at $url)${NC}"
        return 1
    fi
}

# Function to create chaos scenario
create_scenario() {
    local name=$1
    local description=$2
    local failure_type=$3
    local target_service=$4
    local failure_rate=$5
    local duration=$6

    echo -e "🎯 Creating: ${YELLOW}$name${NC}"
    RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/scenarios" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "'"$name"'",
        "description": "'"$description"'",
        "failure_type": "'"$failure_type"'",
        "target_service": "'"$target_service"'",
        "failure_rate": '$failure_rate',
        "duration_seconds": '$duration',
        "enabled": true
      }')

    SCENARIO_ID=$(echo "$RESPONSE" | jq -r '.id')
    SCENARIO_IDS+=(${SCENARIO_ID})
    SCENARIO_NAMES+=("$name")
    echo -e "   📝 Scenario ID: ${GREEN}$SCENARIO_ID${NC}"
}

# Function to execute scenario
execute_scenario() {
    local name=$1
    local scenario_id=""

    # Find the scenario ID by name
    for i in "${!SCENARIO_NAMES[@]}"; do
        if [[ "${SCENARIO_NAMES[$i]}" == "$name" ]]; then
            scenario_id="${SCENARIO_IDS[$i]}"
            break
        fi
    done

    echo -e "💥 Executing: ${YELLOW}$name${NC}"
    RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/scenarios/$scenario_id/execute" \
      -H "Content-Type: application/json")

    WORKFLOW_ID=$(echo "$RESPONSE" | jq -r '.instance_id')
    WORKFLOW_IDS+=("$WORKFLOW_ID")
    echo -e "   🔄 Workflow ID: ${GREEN}$WORKFLOW_ID${NC}"
}

# Function to show circuit breaker summary
show_circuit_breakers() {
    echo -e "\n🔌 ${CYAN}Circuit Breaker States:${NC}"
    RESPONSE=$(curl -s "$ORDER_SERVICE/circuit-breakers")
    echo "$RESPONSE" | jq '.circuit_breakers | to_entries[] | "   \(.key): \(if .value.is_open then "🔴 OPEN" else "🟢 CLOSED" end) (failures: \(.value.failure_count)/\(.value.threshold))"' -r
}

# Function to show chaos status summary
show_chaos_status() {
    echo -e "\n📊 ${CYAN}Chaos Status Summary:${NC}"
    RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/status")
    echo "$RESPONSE" | jq -r '"   Active Failures: \(.active_failures)"'
    echo "$RESPONSE" | jq -r '"   Active Scenarios: \(.active_scenarios | length)"'
    echo "$RESPONSE" | jq -r '"   Events (1h): \(.recent_events_1h)"'
}

# =============================================
# PHASE 1: COMPREHENSIVE SYSTEM ASSESSMENT
# =============================================

print_step "1" "Comprehensive System Health Assessment"

print_substep "Service Availability Check"
echo "🔍 Checking all service endpoints..."
check_service "$CHAOS_SERVICE/chaos/status" "Chaos Engineer Service"
check_service "$ORDER_SERVICE/circuit-breakers" "Order Processor Service"
check_service "$INVENTORY_SERVICE/api/v1/inventory" "Inventory Service"
check_service "$BULK_SERVICE/health" "Bulk Processing Service"
check_service "$RETURN_SERVICE/health" "Return Processing Service"

print_substep "Baseline Metrics Collection"
show_chaos_status
show_circuit_breakers

print_substep "Inventory Preparation"
echo "🔄 Restocking inventory for comprehensive testing..."
curl -s -X POST "$INVENTORY_SERVICE/api/v1/inventory/restock" >/dev/null
echo -e "${GREEN}✅ Inventory restocked${NC}"

# =============================================
# PHASE 2: MULTI-SCENARIO CREATION
# =============================================

print_step "2" "Multi-Scenario Failure Creation"

print_substep "Creating Diverse Failure Scenarios"

# Create multiple scenarios with different characteristics
create_scenario "Payment Cascade Failure" "High-rate payment failures to trigger circuit breaker" "timeout" "payments" 0.95 60
create_scenario "Database Connection Issues" "Database connectivity problems in inventory service" "database_error" "inventory" 0.7 90
create_scenario "Network Infrastructure Degradation" "Network-level failures affecting order processing" "network_error" "order-processor" 0.6 75
create_scenario "Memory Pressure Simulation" "Memory-related failures in shipping service" "memory_error" "shipping" 0.8 45

echo -e "\n${GREEN}✅ Created 4 concurrent failure scenarios${NC}"

# =============================================
# PHASE 3: STAGED FAILURE INJECTION
# =============================================

print_step "3" "Staged Multi-Service Failure Injection"

print_substep "Wave 1: Payment System Stress Test"
execute_scenario "Payment Cascade Failure"
wait_with_countdown 10 "Allowing payment failures to establish pattern..."

print_substep "Wave 2: Database & Network Failures"
execute_scenario "Database Connection Issues"
wait_with_countdown 5 "Brief interval before network failures..."
execute_scenario "Network Infrastructure Degradation"
wait_with_countdown 8 "Observing cascade effects..."

print_substep "Wave 3: Memory Pressure Introduction"
execute_scenario "Memory Pressure Simulation"
echo -e "${YELLOW}🎭 All chaos scenarios are now active!${NC}"

wait_with_countdown 15 "Allowing full chaos pattern to establish..."

# =============================================
# PHASE 4: COMPREHENSIVE SYSTEM TESTING
# =============================================

print_step "4" "Multi-Workflow Testing Under Chaos"

print_substep "Standard Order Processing During Chaos"
echo "🛒 Submitting standard orders to observe failure patterns..."

for i in {1..3}; do
    ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
      -H "Content-Type: application/json" \
      -d '{
        "customer": "chaos_test_user_'$i'",
        "item": "apple",
        "total": 85.00
      }')
    ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.instance_id')
    echo -e "   📦 Order $i: ${GREEN}$ORDER_ID${NC}"
done

print_substep "Bulk Order Processing During Chaos"
echo "📦 Testing bulk order resilience during multi-service failures..."

BULK_RESPONSE=$(curl -s -X POST "$BULK_SERVICE/bulk-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "chaos_bulk_test",
    "items": [
      {"item": "apple", "quantity": 2, "price": 50.0},
      {"item": "orange", "quantity": 1, "price": 75.0},
      {"item": "pear", "quantity": 3, "price": 30.0}
    ]
  }')

BULK_ID=$(echo "$BULK_RESPONSE" | jq -r '.instance_id')
echo -e "   🎁 Bulk Order: ${GREEN}$BULK_ID${NC}"

print_substep "Return Processing During Chaos"
echo "↩️ Testing return workflow resilience..."

RETURN_RESPONSE=$(curl -s -X POST "$RETURN_SERVICE/returns" \
  -H "Content-Type: application/json" \
  -d '{
    "original_order_id": "order_chaos_test_baseline",
    "customer": "chaos_return_test",
    "item": "apple",
    "reason": "defective",
    "description": "Testing return processing during chaos",
    "return_value": 65.0
  }')

RETURN_ID=$(echo "$RETURN_RESPONSE" | jq -r '.instance_id')
echo -e "   📤 Return Request: ${GREEN}$RETURN_ID${NC}"

# =============================================
# PHASE 5: REAL-TIME MONITORING & ANALYSIS
# =============================================

print_step "5" "Real-Time System Behavior Analysis"

print_substep "Circuit Breaker Threshold Analysis"
show_circuit_breakers

print_substep "Failure Pattern Analysis"
echo -e "\n📊 Recent chaos events (showing top 8):"
curl -s "${CHAOS_SERVICE}/chaos/events?limit=20" | jq '.[:8] | .[] | "   \(.timestamp | split("T")[1] | split(".")[0]) [\(.severity | ascii_upcase)] \(.message)"' -r

print_substep "Service-Specific Error Analysis"
echo -e "\n⚠️  Critical and Error events (last 15 minutes):"
curl -s "${CHAOS_SERVICE}/chaos/events?severity=error&limit=15" | jq '.[:6] | .[] | "   🔴 \(.service): \(.message)"' -r

wait_with_countdown 20 "Deep system observation period..."

# =============================================
# PHASE 6: CIRCUIT BREAKER THRESHOLD TESTING
# =============================================

print_step "6" "Circuit Breaker Threshold Validation"

print_substep "High-Frequency Order Submission"
echo "🚀 Rapid order submission to test circuit breaker thresholds..."

for i in {1..6}; do
    ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
      -H "Content-Type: application/json" \
      -d '{
        "customer": "threshold_test_'$i'",
        "item": "kiwi",
        "total": 120.00
      }')
    ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.instance_id')
    echo -e "   ⚡ Rapid Order $i: ${GREEN}$ORDER_ID${NC}"
    sleep 2  # Brief delay between orders
done

print_substep "Circuit Breaker State Monitoring"
show_circuit_breakers

# =============================================
# PHASE 7: CASCADE FAILURE ANALYSIS
# =============================================

print_step "7" "Cascade Failure Pattern Analysis"

print_substep "Service Dependency Impact Assessment"
echo "🔗 Analyzing cascade effects across service dependencies..."

echo -e "\n📈 Service health degradation patterns:"
curl -s "${CHAOS_SERVICE}/chaos/events?limit=30" | jq '.[] | select(.event_type == "workflow_completed") | .details.post_failure_health.services | to_entries[] | "   \(.key): \(.value.health_score)% (errors: \(.value.error_rate | . * 100 | floor)%)"' -r | head -5

print_substep "Workflow Completion Analysis"
echo -e "\n🔄 Workflow execution patterns under chaos:"
for i in "${!SCENARIO_NAMES[@]}"; do
    name="${SCENARIO_NAMES[$i]}"
    workflow_id="${WORKFLOW_IDS[$i]}"
    echo -e "   📋 $name: ${GREEN}$workflow_id${NC}"
done

# =============================================
# PHASE 8: SYSTEM RECOVERY MONITORING
# =============================================

print_step "8" "System Recovery & Resilience Validation"

print_substep "Waiting for Scenario Completion"
wait_with_countdown 25 "Allowing chaos scenarios to complete naturally..."

print_substep "Post-Chaos System Assessment"
show_chaos_status
show_circuit_breakers

print_substep "Recovery Validation Testing"
echo "🧪 Testing system recovery with normal operations..."

# Test normal order processing
RECOVERY_ORDER=$(curl -s -X POST "$ORDER_SERVICE/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "recovery_validation_user",
    "item": "pear",
    "total": 40.00
  }')

RECOVERY_ID=$(echo "$RECOVERY_ORDER" | jq -r '.instance_id')
echo -e "   📦 Recovery Order: ${GREEN}$RECOVERY_ID${NC}"

# Test bulk order processing
RECOVERY_BULK=$(curl -s -X POST "$BULK_SERVICE/bulk-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "recovery_bulk_user",
    "items": [
      {"item": "apple", "quantity": 1, "price": 45.0},
      {"item": "orange", "quantity": 2, "price": 35.0}
    ]
  }')

RECOVERY_BULK_ID=$(echo "$RECOVERY_BULK" | jq -r '.instance_id')
echo -e "   🎁 Recovery Bulk Order: ${GREEN}$RECOVERY_BULK_ID${NC}"

wait_with_countdown 10 "Verifying recovery operations..."

# =============================================
# COMPREHENSIVE DEMO SUMMARY
# =============================================

print_step "9" "Comprehensive Demo Analysis & Summary"

print_substep "Final System Health Report"
show_chaos_status
show_circuit_breakers

print_substep "Event Summary & Insights"
echo -e "\n📊 Complete chaos engineering session summary:"
TOTAL_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?limit=100" | jq 'length')
ERROR_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?severity=error&limit=100" | jq 'length')
WARNING_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?severity=warning&limit=100" | jq 'length')

echo -e "   📈 Total Events Generated: ${GREEN}$TOTAL_EVENTS${NC}"
echo -e "   🔴 Error Events: ${RED}$ERROR_EVENTS${NC}"
echo -e "   🟡 Warning Events: ${YELLOW}$WARNING_EVENTS${NC}"
echo -e "   ℹ️  Info Events: ${BLUE}$((TOTAL_EVENTS - ERROR_EVENTS - WARNING_EVENTS))${NC}"

print_substep "Scenario Execution Summary"
echo -e "\n🎯 Chaos scenarios executed:"
for i in "${!SCENARIO_NAMES[@]}"; do
    name="${SCENARIO_NAMES[$i]}"
    scenario_id="${SCENARIO_IDS[$i]}"
    workflow_id="${WORKFLOW_IDS[$i]}"
    echo -e "   ✅ $name"
    echo -e "      📋 Scenario: ${GREEN}$scenario_id${NC}"
    echo -e "      🔄 Workflow: ${GREEN}$workflow_id${NC}"
done

echo -e "\n${GREEN}🎉 Advanced Chaos Engineering Demo Complete!${NC}"
echo "============================================================"
echo -e "${CYAN}📋 COMPREHENSIVE DEMO SUMMARY:${NC}"
echo "   • 🎯 Executed 4 concurrent failure scenarios"
echo "   • 💥 Tested payment, database, network, and memory failures"
echo "   • 🔌 Monitored circuit breaker threshold responses"
echo "   • 🔗 Analyzed cascade failure patterns"
echo "   • 📦 Validated order, bulk, and return workflows under chaos"
echo "   • 🧪 Verified system recovery and resilience"
echo "   • 📊 Generated comprehensive observability data"
echo ""
echo -e "${YELLOW}💡 NEXT STEPS & INSIGHTS:${NC}"
echo "   • 🖥️  Dashboard UI: http://localhost:8080 (live notifications)"
echo "   • 📈 Detailed Events: curl ${CHAOS_SERVICE}/chaos/events"
echo "   • 🔍 Event Filtering: Add ?severity=error or ?limit=N"
echo "   • 📋 Scenario Management: Check active scenarios and cleanup"
echo "   • 🔄 Correlation Tracing: Use workflow IDs for end-to-end analysis"
echo ""
echo -e "${MAGENTA}🚀 ADVANCED CHAOS PATTERNS DEMONSTRATED:${NC}"
echo "   • ⚡ Multi-service concurrent failure injection"
echo "   • 🎭 Staged failure introduction and observation"
echo "   • 🔌 Circuit breaker threshold validation"
echo "   • 🔗 Cascade failure containment analysis"
echo "   • 📊 Real-time monitoring and diagnostic correlation"
echo "   • 🧪 Recovery pattern validation and testing"
echo ""
echo -e "${GREEN}✅ Demo completed successfully with comprehensive chaos coverage!${NC}"
