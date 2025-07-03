#!/bin/bash

# =============================================
# ADVANCED WORKFLOW CHAOS SCENARIOS DEMO SCRIPT
# =============================================
# PURPOSE: Demonstrate advanced workflow-specific failure patterns
# SCENARIOS: External Event Starvation, Child Workflow Zombies, Activity Limbo, Transaction Failures
# FOCUS: Workflow debugging, manual intervention, recovery procedures
# AUDIENCE: Perfect for demonstrating complex distributed system failures
# DURATION: ~15-20 minutes for full advanced demonstration
# =============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
CHAOS_SERVICE="http://localhost:3010"
ORDER_SERVICE="http://localhost:3006"
BULK_SERVICE="http://localhost:3007"
RETURN_SERVICE="http://localhost:3008"

# Global variables for scenario tracking
declare -a ADVANCED_SCENARIO_IDS
declare -a ADVANCED_WORKFLOW_IDS

echo -e "${CYAN}🎭 Starting Advanced Workflow Chaos Scenarios Demo${NC}"
echo "==============================================================="
echo -e "${YELLOW}⚡ Advanced Workflow-Specific Failure Simulation & Recovery${NC}"
echo "==============================================================="

# Function to print step headers
print_step() {
    echo -e "\n${MAGENTA}📋 PHASE $1: $2${NC}"
    echo "==============================================================="
}

# Function to print sub-steps
print_substep() {
    echo -e "\n${CYAN}🔹 $1${NC}"
    echo "---------------------------------------------------------------"
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

# Function to create advanced chaos scenario
create_advanced_scenario() {
    local name=$1
    local description=$2
    local failure_type=$3
    local target_service=$4
    local failure_rate=$5
    local duration=$6

    echo -e "🎯 Creating Advanced Scenario: ${YELLOW}$name${NC}"
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
    ADVANCED_SCENARIO_IDS["$name"]=$SCENARIO_ID
    echo -e "   📝 Advanced Scenario ID: ${GREEN}$SCENARIO_ID${NC}"
}

# Function to execute advanced scenario
execute_advanced_scenario() {
    local name=$1
    local scenario_id=${ADVANCED_SCENARIO_IDS[$name]}

    echo -e "💥 Executing Advanced Scenario: ${YELLOW}$name${NC}"
    RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/scenarios/$scenario_id/execute" \
      -H "Content-Type: application/json")

    WORKFLOW_ID=$(echo "$RESPONSE" | jq -r '.instance_id')
    ADVANCED_WORKFLOW_IDS["$name"]=$WORKFLOW_ID
    echo -e "   🔄 Advanced Workflow ID: ${GREEN}$WORKFLOW_ID${NC}"
}

# Function to show advanced failure states
show_advanced_failures() {
    echo -e "\n🎭 ${CYAN}Advanced Workflow Failure States:${NC}"
    RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/advanced-failures")
    if [[ $(echo "$RESPONSE" | jq '.total_failures') -gt 0 ]]; then
        echo "$RESPONSE" | jq '.workflow_failure_states[] | "   📋 \(.workflow_id): \(.failure_type) in \(.target_service)"' -r
    else
        echo "   ✅ No advanced failures detected"
    fi
}

# Function to show zombie workflows
show_zombie_workflows() {
    echo -e "\n🧟‍♂️ ${CYAN}Zombie Workflow States:${NC}"
    RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/zombie-workflows")
    if [[ $(echo "$RESPONSE" | jq '.total_zombies') -gt 0 ]]; then
        echo "$RESPONSE" | jq '.zombie_workflows[] | "   🧟 \(.child_workflow_id): stuck in \(.stuck_activity) (\(.simulated_hang_reason))"' -r
    else
        echo "   ✅ No zombie workflows detected"
    fi
}

# Function to show missed events
show_missed_events() {
    echo -e "\n📡 ${CYAN}Missed External Events:${NC}"
    RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/missed-events")
    if [[ $(echo "$RESPONSE" | jq '.total_missed') -gt 0 ]]; then
        echo "$RESPONSE" | jq '.missed_events[] | "   📡 \(.workflow_id): waiting for \(.event_name) from \(.event_source)"' -r
    else
        echo "   ✅ No missed events detected"
    fi
}

# Function to show hanging activities
show_hanging_activities() {
    echo -e "\n⏳ ${CYAN}Hanging Activities:${NC}"
    RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/hanging-activities")
    if [[ $(echo "$RESPONSE" | jq '.total_services_affected') -gt 0 ]]; then
        echo "$RESPONSE" | jq '.hanging_activities | to_entries[] | "   ⏳ \(.key): \(.value | join(", "))"' -r
    else
        echo "   ✅ No hanging activities detected"
    fi
}

# Function to show comprehensive advanced status
show_comprehensive_advanced_status() {
    echo -e "\n📊 ${CYAN}Comprehensive Advanced Chaos Status:${NC}"
    show_advanced_failures
    show_zombie_workflows
    show_missed_events
    show_hanging_activities
}

# =============================================
# PHASE 1: BASELINE ADVANCED FAILURE ASSESSMENT
# =============================================

print_step "1" "Baseline Advanced Failure Assessment"

print_substep "Service Availability Check"
echo "🔍 Checking all service endpoints for advanced testing..."
check_service "$CHAOS_SERVICE/chaos/advanced-failures" "Advanced Failures Endpoint"
check_service "$CHAOS_SERVICE/chaos/zombie-workflows" "Zombie Workflows Endpoint"
check_service "$CHAOS_SERVICE/chaos/missed-events" "Missed Events Endpoint"
check_service "$CHAOS_SERVICE/chaos/hanging-activities" "Hanging Activities Endpoint"
check_service "$ORDER_SERVICE/health" "Order Processor Service"
check_service "$BULK_SERVICE/health" "Bulk Processing Service"
check_service "$RETURN_SERVICE/health" "Return Processing Service"

print_substep "Baseline Advanced Metrics Collection"
show_comprehensive_advanced_status

print_substep "System Preparation for Advanced Testing"
echo "🔄 Preparing system for advanced workflow failure testing..."
echo -e "${GREEN}✅ System ready for advanced chaos scenarios${NC}"

# =============================================
# PHASE 2: EXTERNAL EVENT STARVATION SCENARIO
# =============================================

print_step "2" "External Event Starvation Simulation"

print_substep "Creating External Event Starvation Scenario"
create_advanced_scenario "External Event Starvation Test" \
    "Simulate workflows waiting indefinitely for external events (approvals, webhooks, API responses)" \
    "external_event_starvation" \
    "order-processor" \
    0.9 \
    120

print_substep "Executing External Event Starvation"
execute_advanced_scenario "External Event Starvation Test"
wait_with_countdown 8 "Allowing event starvation pattern to establish..."

print_substep "Creating Test Workflows That Will Be Affected"
echo "🛒 Creating high-value order that will require approval (triggering event starvation)..."
ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "event_starvation_demo_user",
    "item": "diamond_ring",
    "total": 2500.00
  }')
ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.instance_id')
echo -e "   📦 High-Value Order (will starve waiting for approval): ${GREEN}$ORDER_ID${NC}"

print_substep "Monitoring Event Starvation Effects"
show_missed_events
wait_with_countdown 10 "Observing external event starvation patterns..."

# =============================================
# PHASE 3: CHILD WORKFLOW ZOMBIE SCENARIO
# =============================================

print_step "3" "Child Workflow Zombie State Simulation"

print_substep "Creating Child Workflow Zombie Scenario"
create_advanced_scenario "Child Workflow Zombie State" \
    "Simulate child workflows that enter zombie state (running but never complete)" \
    "child_workflow_zombie" \
    "batch-processor" \
    0.8 \
    90

print_substep "Executing Child Workflow Zombie Simulation"
execute_advanced_scenario "Child Workflow Zombie State"
wait_with_countdown 6 "Allowing zombie workflow pattern to establish..."

print_substep "Creating Bulk Order to Trigger Child Workflows"
echo "📦 Creating bulk order that will spawn child workflows (some will become zombies)..."
BULK_RESPONSE=$(curl -s -X POST "$BULK_SERVICE/bulk-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "zombie_workflow_demo",
    "items": [
      {"item": "laptop", "quantity": 1, "price": 1200.0},
      {"item": "monitor", "quantity": 2, "price": 300.0},
      {"item": "keyboard", "quantity": 1, "price": 100.0},
      {"item": "mouse", "quantity": 1, "price": 50.0}
    ]
  }')
BULK_ID=$(echo "$BULK_RESPONSE" | jq -r '.instance_id')
echo -e "   🎁 Bulk Order (will have zombie children): ${GREEN}$BULK_ID${NC}"

print_substep "Monitoring Zombie Workflow Creation"
show_zombie_workflows
wait_with_countdown 12 "Observing zombie child workflow patterns..."

# =============================================
# PHASE 4: ACTIVITY EXECUTION LIMBO SCENARIO
# =============================================

print_step "4" "Activity Execution Limbo Simulation"

print_substep "Creating Activity Execution Limbo Scenario"
create_advanced_scenario "Activity Execution Limbo" \
    "Simulate activities that hang indefinitely, consuming resources without completion" \
    "activity_execution_limbo" \
    "payments" \
    0.7 \
    75

print_substep "Executing Activity Execution Limbo Simulation"
execute_advanced_scenario "Activity Execution Limbo"
wait_with_countdown 5 "Allowing activity limbo pattern to establish..."

print_substep "Creating Orders to Trigger Payment Activities"
echo "💳 Creating orders that will trigger payment activities (which will hang)..."
for i in {1..2}; do
    ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
      -H "Content-Type: application/json" \
      -d '{
        "customer": "activity_limbo_test_'$i'",
        "item": "smartphone",
        "total": 800.00
      }')
    ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.instance_id')
    echo -e "   📱 Order $i (payment activity will hang): ${GREEN}$ORDER_ID${NC}"
done

print_substep "Monitoring Hanging Activities"
show_hanging_activities
wait_with_countdown 10 "Observing activity execution limbo patterns..."

# =============================================
# PHASE 5: DISTRIBUTED TRANSACTION FAILURE SCENARIO
# =============================================

print_step "5" "Distributed Transaction Failure Simulation"

print_substep "Creating Distributed Transaction Failure Scenario"
create_advanced_scenario "Distributed Transaction Compensation Failure" \
    "Simulate failures during distributed transaction compensation/rollback operations" \
    "distributed_transaction_failure" \
    "inventory" \
    0.6 \
    60

print_substep "Executing Distributed Transaction Failure Simulation"
execute_advanced_scenario "Distributed Transaction Compensation Failure"
wait_with_countdown 4 "Allowing transaction failure pattern to establish..."

print_substep "Creating Orders to Trigger Transaction Workflows"
echo "🏪 Creating orders that will fail during shipping (triggering compensation failures)..."
ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "transaction_failure_demo",
    "item": "fragile_item",
    "total": 450.00
  }')
ORDER_ID=$(echo "$ORDER_RESPONSE" | jq -r '.instance_id')
echo -e "   📦 Order (will fail during shipping rollback): ${GREEN}$ORDER_ID${NC}"

wait_with_countdown 8 "Observing distributed transaction failure patterns..."

# =============================================
# PHASE 6: COMPREHENSIVE MONITORING & ANALYSIS
# =============================================

print_step "6" "Comprehensive Advanced Failure Analysis"

print_substep "Advanced Failure State Overview"
show_comprehensive_advanced_status

print_substep "Critical Events Analysis"
echo -e "\n🚨 Critical and Error events from advanced scenarios:"
curl -s "${CHAOS_SERVICE}/chaos/events?severity=critical&limit=10" | jq '.[:5] | .[] | "   🔴 \(.timestamp | split("T")[1] | split(".")[0]) [\(.event_type | ascii_upcase)] \(.message)"' -r

print_substep "Advanced Diagnostic Events"
echo -e "\n📊 Recent advanced workflow events (showing top 10):"
curl -s "${CHAOS_SERVICE}/chaos/events?limit=30" | jq '.[] | select(.event_type | contains("external_event") or contains("zombie") or contains("limbo") or contains("transaction")) | .message' -r | head -10

wait_with_countdown 15 "Deep advanced failure pattern analysis period..."

# =============================================
# PHASE 7: RECOVERY SIMULATION & MANUAL INTERVENTION
# =============================================

print_step "7" "Recovery Simulation & Manual Intervention"

print_substep "External Event Starvation Recovery"
echo "🔧 Simulating manual event injection for starved workflows..."
for name in "${!ADVANCED_SCENARIO_IDS[@]}"; do
    if [[ "$name" == "External Event Starvation Test" ]]; then
        scenario_id=${ADVANCED_SCENARIO_IDS[$name]}
        echo -e "   🔄 Attempting recovery for scenario: ${YELLOW}$scenario_id${NC}"

        RECOVERY_RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/advanced-failures/$scenario_id/recover" \
          -H "Content-Type: application/json")

        if [[ $(echo "$RECOVERY_RESPONSE" | jq -r '.status') == "recovery_simulated" ]]; then
            echo -e "   ✅ Recovery simulated for external event starvation"
            echo "$RECOVERY_RESPONSE" | jq '.recovery_actions[] | "      🔧 \(.action): \(.event // .status)"' -r
        fi
    fi
done

print_substep "Zombie Workflow Recovery"
echo "🧟‍♂️ Simulating zombie child workflow cleanup..."
ZOMBIE_RESPONSE=$(curl -s "$CHAOS_SERVICE/chaos/zombie-workflows")
if [[ $(echo "$ZOMBIE_RESPONSE" | jq '.total_zombies') -gt 0 ]]; then
    # Get first zombie workflow's parent ID
    PARENT_ID=$(echo "$ZOMBIE_RESPONSE" | jq -r '.zombie_workflows[0].parent_workflow_id')

    RECOVERY_RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/advanced-failures/$PARENT_ID/recover" \
      -H "Content-Type: application/json")

    if [[ $(echo "$RECOVERY_RESPONSE" | jq -r '.status') == "recovery_simulated" ]]; then
        echo -e "   ✅ Zombie cleanup simulated"
        echo "$RECOVERY_RESPONSE" | jq '.recovery_actions[] | "      🧟 \(.action): \(.child_workflow_id // .status)"' -r
    fi
fi

print_substep "Activity Limbo Recovery"
echo "⏳ Simulating hanging activity termination..."
for name in "${!ADVANCED_SCENARIO_IDS[@]}"; do
    if [[ "$name" == "Activity Execution Limbo" ]]; then
        scenario_id=${ADVANCED_SCENARIO_IDS[$name]}

        RECOVERY_RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/advanced-failures/$scenario_id/recover" \
          -H "Content-Type: application/json")

        if [[ $(echo "$RECOVERY_RESPONSE" | jq -r '.status') == "recovery_simulated" ]]; then
            echo -e "   ✅ Activity termination simulated"
            echo "$RECOVERY_RESPONSE" | jq '.recovery_actions[] | "      ⏳ \(.action): \(.activity // .status)"' -r
        fi
    fi
done

print_substep "Post-Recovery Status Check"
show_comprehensive_advanced_status

wait_with_countdown 10 "Verifying recovery effectiveness..."

# =============================================
# PHASE 8: ADVANCED SCENARIO CORRELATION ANALYSIS
# =============================================

print_step "8" "Advanced Scenario Correlation & Tracing Analysis"

print_substep "End-to-End Workflow Correlation"
echo -e "\n🔗 Advanced workflow execution summary:"
for name in "${!ADVANCED_SCENARIO_IDS[@]}"; do
    scenario_id=${ADVANCED_SCENARIO_IDS[$name]}
    workflow_id=${ADVANCED_WORKFLOW_IDS[$name]}
    echo -e "   📋 $name"
    echo -e "      🎯 Scenario: ${GREEN}$scenario_id${NC}"
    echo -e "      🔄 Workflow: ${GREEN}$workflow_id${NC}"
done

print_substep "Correlation ID Event Tracing"
echo -e "\n📊 Event correlation analysis (showing sample from first advanced scenario):"
if [[ ${#ADVANCED_SCENARIO_IDS[@]} -gt 0 ]]; then
    FIRST_SCENARIO_ID=$(echo "${ADVANCED_SCENARIO_IDS[@]}" | tr ' ' '\n' | head -1)
    curl -s "${CHAOS_SERVICE}/chaos/events?correlation_id=$FIRST_SCENARIO_ID&limit=15" | jq '.[:5] | .[] | "   📎 \(.timestamp | split("T")[1] | split(".")[0]) [\(.severity | ascii_upcase)] \(.message)"' -r
fi

print_substep "Advanced Failure Pattern Summary"
echo -e "\n🎭 Advanced failure patterns demonstrated:"
echo -e "   📡 External Event Starvation: Workflows waiting for events that never arrive"
echo -e "   🧟‍♂️ Child Workflow Zombies: Parent workflows stuck waiting for zombie children"
echo -e "   ⏳ Activity Execution Limbo: Activities hanging indefinitely consuming resources"
echo -e "   💥 Distributed Transaction Failure: Compensation failures leaving inconsistent state"

# =============================================
# COMPREHENSIVE ADVANCED DEMO SUMMARY
# =============================================

print_step "9" "Comprehensive Advanced Demo Analysis & Summary"

print_substep "Final Advanced System Health Report"
show_comprehensive_advanced_status

print_substep "Advanced Event Summary & Insights"
echo -e "\n📊 Advanced chaos engineering session summary:"
TOTAL_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?limit=200" | jq 'length')
CRITICAL_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?severity=critical&limit=100" | jq 'length')
ERROR_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?severity=error&limit=100" | jq 'length')
WARNING_EVENTS=$(curl -s "${CHAOS_SERVICE}/chaos/events?severity=warning&limit=100" | jq 'length')

echo -e "   📈 Total Advanced Events Generated: ${GREEN}$TOTAL_EVENTS${NC}"
echo -e "   🔴 Critical Events: ${RED}$CRITICAL_EVENTS${NC}"
echo -e "   🟠 Error Events: ${YELLOW}$ERROR_EVENTS${NC}"
echo -e "   🟡 Warning Events: ${YELLOW}$WARNING_EVENTS${NC}"
echo -e "   ℹ️  Info Events: ${BLUE}$((TOTAL_EVENTS - CRITICAL_EVENTS - ERROR_EVENTS - WARNING_EVENTS))${NC}"

print_substep "Advanced Scenario Execution Summary"
echo -e "\n🎭 Advanced chaos scenarios executed:"
for name in "${!ADVANCED_SCENARIO_IDS[@]}"; do
    scenario_id=${ADVANCED_SCENARIO_IDS[$name]}
    workflow_id=${ADVANCED_WORKFLOW_IDS[$name]}
    echo -e "   ✅ $name"
    echo -e "      📋 Scenario: ${GREEN}$scenario_id${NC}"
    echo -e "      🔄 Workflow: ${GREEN}$workflow_id${NC}"
done

echo -e "\n${GREEN}🎉 Advanced Workflow Chaos Scenarios Demo Complete!${NC}"
echo "=================================================================="
echo -e "${CYAN}📋 ADVANCED COMPREHENSIVE DEMO SUMMARY:${NC}"
echo "   • 🎭 Executed 4 advanced workflow-specific failure scenarios"
echo "   • 📡 Tested external event starvation (approval workflows)"
echo "   • 🧟‍♂️ Simulated child workflow zombie states (batch processing)"
echo "   • ⏳ Created activity execution limbo (hanging payment activities)"
echo "   • 💥 Triggered distributed transaction compensation failures"
echo "   • 🔧 Demonstrated manual intervention and recovery procedures"
echo "   • 📊 Generated comprehensive advanced diagnostic data"
echo ""
echo -e "${YELLOW}💡 ADVANCED INSIGHTS & NEXT STEPS:${NC}"
echo "   • 🖥️  Dashboard UI: http://localhost:8080 (live advanced notifications)"
echo "   • 📈 Advanced Events: curl ${CHAOS_SERVICE}/chaos/events"
echo "   • 🎭 Advanced Failures: curl ${CHAOS_SERVICE}/chaos/advanced-failures"
echo "   • 🧟‍♂️ Zombie Workflows: curl ${CHAOS_SERVICE}/chaos/zombie-workflows"
echo "   • 📡 Missed Events: curl ${CHAOS_SERVICE}/chaos/missed-events"
echo "   • ⏳ Hanging Activities: curl ${CHAOS_SERVICE}/chaos/hanging-activities"
echo "   • 🔧 Recovery Simulation: POST to /chaos/advanced-failures/{id}/recover"
echo ""
echo -e "${MAGENTA}🚀 ADVANCED WORKFLOW PATTERNS DEMONSTRATED:${NC}"
echo "   • 📡 External event dependency management and timeout handling"
echo "   • 🧟‍♂️ Parent-child workflow lifecycle and zombie detection"
echo "   • ⏳ Activity execution monitoring and resource management"
echo "   • 💥 Distributed transaction compensation and rollback handling"
echo "   • 🔧 Manual intervention procedures for complex failure states"
echo "   • 📊 Advanced workflow debugging and correlation tracing"
echo ""
echo -e "${GREEN}✅ Advanced demo completed with comprehensive workflow failure coverage!${NC}"
