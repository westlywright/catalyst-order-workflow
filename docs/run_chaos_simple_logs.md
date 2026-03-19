🚀 Starting Simple Chaos Engineering Demo
==================================================

📋 STEP 1: Baseline System Health Assessment
----------------------------------------
🔍 Checking service availability...
✅ Chaos Engineer Service is responding
✅ Order Processor Service is responding
✅ Inventory Service is responding

📊 Initial chaos status:
{
  "active_failures": 0,
  "active_scenarios": [],
  "chaos_enabled": true,
  "failure_rate": 0.5,
  "recent_events_1h": 0,
  "total_scenarios": 0
}

🔌 Initial circuit breaker states:
{
  "chaos_detection_enabled": true,
  "circuit_breakers": {
    "inventory": {
      "failure_count": 0,
      "is_open": false,
      "last_failure": null,
      "threshold": 3,
      "timeout_minutes": 1.0
    },
    "payments": {
      "failure_count": 0,
      "is_open": false,
      "last_failure": null,
      "threshold": 3,
      "timeout_minutes": 1.0
    },
    "shipping": {
      "failure_count": 0,
      "is_open": false,
      "last_failure": null,
      "threshold": 3,
      "timeout_minutes": 1.0
    }
  },
  "timestamp": "2026-02-06T08:24:54.731314"
}

📋 STEP 2: Creating Payment Timeout Scenario
----------------------------------------
🎯 Creating payment service timeout scenario...
📝 Scenario creation response:
{
  "created_at": "2026-02-06T08:24:54.747034",
  "description": "Simple payment timeout for demo validation",
  "duration_seconds": 30,
  "enabled": true,
  "failure_rate": 0.8,
  "failure_type": "timeout",
  "id": "chaos_quick_payment_timeout_demo_6507",
  "name": "Quick Payment Timeout Demo",
  "target_service": "payments"
}
✅ Created scenario with ID: chaos_quick_payment_timeout_demo_6507

📋 STEP 3: Executing Chaos Scenario
----------------------------------------
💥 Executing chaos scenario...
🎭 Chaos scenario is now active!

📋 STEP 4: Testing System Under Chaos
----------------------------------------
⏳ Allowing chaos to take effect...
   Waiting... 1s remaining^C
