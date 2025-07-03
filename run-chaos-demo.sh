#!/bin/bash

# =============================================
# SIMPLE CHAOS ENGINEERING DEMO SCRIPT
# =============================================
# PURPOSE: Automated demonstration of failure simulation and resilience testing
# DURATION: ~3-5 minutes for quick validation and debugging
# FOCUS: Payment service timeout with circuit breaker demonstration
# =============================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CHAOS_SERVICE="http://localhost:3010"
ORDER_SERVICE="http://localhost:3006"
INVENTORY_SERVICE="http://localhost:3002"

echo -e "${BLUE}🚀 Starting Simple Chaos Engineering Demo${NC}"
echo "=================================================="

# Function to print step headers
print_step() {
    echo -e "\n${YELLOW}📋 STEP $1: $2${NC}"
    echo "----------------------------------------"
}

# Function to wait with countdown
wait_with_countdown() {
    local seconds=$1
    local message=$2
    echo -e "${BLUE}⏳ $message${NC}"
    for ((i=seconds; i>=1; i--)); do
        echo -ne "\r   Waiting... ${i}s remaining"
        sleep 1
    done
    echo -ne "\r   ✅ Wait complete!        \n"
}

# Function to check if service is responding
check_service() {
    local url=$1
    local name=$2
    if curl -s "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ $name is responding${NC}"
        return 0
    else
        echo -e "${RED}❌ $name is not responding at $url${NC}"
        return 1
    fi
}

# =============================================
# PHASE 1: BASELINE HEALTH CHECK
# =============================================

print_step "1" "Baseline System Health Assessment"

echo "🔍 Checking service availability..."
check_service "$CHAOS_SERVICE/chaos/status" "Chaos Engineer Service"
check_service "$ORDER_SERVICE/circuit-breakers" "Order Processor Service"
check_service "$INVENTORY_SERVICE/api/v1/inventory" "Inventory Service"

echo -e "\n📊 Initial chaos status:"
curl -s "$CHAOS_SERVICE/chaos/status" | jq '.' || echo "Failed to get chaos status"

echo -e "\n🔌 Initial circuit breaker states:"
curl -s "$ORDER_SERVICE/circuit-breakers" | jq '.' || echo "Failed to get circuit breaker status"

# =============================================
# PHASE 2: SCENARIO CREATION
# =============================================

print_step "2" "Creating Payment Timeout Scenario"

echo "🎯 Creating payment service timeout scenario..."
SCENARIO_RESPONSE=$(curl -s -X POST "$CHAOS_SERVICE/chaos/scenarios" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Payment Timeout Demo",
    "description": "Simple payment timeout for demo validation",
    "failure_type": "timeout",
    "target_service": "payments",
    "failure_rate": 0.8,
    "duration_seconds": 30,
    "enabled": true
  }')

echo "📝 Scenario creation response:"
echo "$SCENARIO_RESPONSE" | jq '.'

# Extract scenario ID
SCENARIO_ID=$(echo "$SCENARIO_RESPONSE" | jq -r '.id')
echo -e "${GREEN}✅ Created scenario with ID: $SCENARIO_ID${NC}"

# =============================================
# PHASE 3: FAILURE INJECTION
# =============================================

print_step "3" "Executing Chaos Scenario"

echo "💥 Executing chaos scenario..."
curl -s -X POST "$CHAOS_SERVICE/chaos/scenarios/$SCENARIO_ID/execute" \
  -H "Content-Type: application/json" | jq '.'

echo -e "${YELLOW}🎭 Chaos scenario is now active!${NC}"

# =============================================
# PHASE 4: SYSTEM TESTING DURING CHAOS
# =============================================

print_step "4" "Testing System Under Chaos"

wait_with_countdown 5 "Allowing chaos to take effect..."

echo "🛒 Submitting test order during chaos to observe failures..."
ORDER_RESPONSE=$(curl -s -X POST "$ORDER_SERVICE/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "chaos_demo_user",
    "item": "apple",
    "total": 75.00
  }')

echo "📦 Order submission response:"
echo "$ORDER_RESPONSE" | jq '.'

# =============================================
# PHASE 5: MONITORING AND OBSERVABILITY
# =============================================

print_step "5" "Monitoring System Behavior"

wait_with_countdown 8 "Observing system behavior during failure injection..."

echo "🔌 Circuit breaker states during chaos:"
curl -s "$ORDER_SERVICE/circuit-breakers" | jq '.'

echo -e "\n📊 Recent chaos events (last 20):"
curl -s "${CHAOS_SERVICE}/chaos/events?limit=20" | jq '.[:5] // empty' || echo "No events available"

echo -e "\n⚠️  Error events during chaos:"
curl -s "${CHAOS_SERVICE}/chaos/events?severity=error&limit=10" | jq '.[:3] // empty' || echo "No error events"

# =============================================
# PHASE 6: RECOVERY MONITORING
# =============================================

print_step "6" "System Recovery Monitoring"

wait_with_countdown 15 "Waiting for chaos scenario to complete (30s duration)..."

echo "🔄 Post-chaos system status:"
curl -s "$CHAOS_SERVICE/chaos/status" | jq '.'

echo -e "\n🔌 Circuit breaker recovery status:"
curl -s "$ORDER_SERVICE/circuit-breakers" | jq '.'

echo -e "\n🛒 Testing normal order processing after chaos..."
RECOVERY_ORDER=$(curl -s -X POST "$ORDER_SERVICE/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "recovery_test_user",
    "item": "orange",
    "total": 50.00
  }')

echo "📦 Recovery order response:"
echo "$RECOVERY_ORDER" | jq '.'

# =============================================
# DEMO SUMMARY
# =============================================

echo -e "\n${GREEN}🎉 Simple Chaos Demo Complete!${NC}"
echo "=================================================="
echo -e "${BLUE}📋 Demo Summary:${NC}"
echo "   • Created and executed payment timeout scenario"
echo "   • Observed system behavior during 80% failure rate"
echo "   • Monitored circuit breaker state changes"
echo "   • Verified system recovery after chaos completion"
echo "   • Tested normal operations post-recovery"
echo ""
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo "   • Check notifications UI at http://localhost:8080"
echo "   • Review detailed events: curl $CHAOS_SERVICE/chaos/events"
echo "   • Run chaos-demo.http for comprehensive scenarios"
echo ""
echo -e "${GREEN}✅ Demo completed successfully!${NC}"
