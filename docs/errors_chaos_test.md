== APP - payments ==  * Serving Flask app 'app'
== APP - payments ==  * Debug mode: off
== APP - notifications ==
== APP - notifications == > vite_react_shadcn_ts@0.0.0 dev
== APP - notifications == > concurrently "npm run dev:server" "npm run dev:client"
== APP - shipping ==  * Serving Flask app 'app'
== APP - shipping ==  * Debug mode: on
== APP - notifications ==
== APP - payments == 2026-02-06 08:23:34.634 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - payments ==  * Running on all addresses (0.0.0.0)
== APP - payments ==  * Running on http://127.0.0.1:3003
== APP - payments ==  * Running on http://192.168.0.223:3003
== APP - payments == 2026-02-06 08:23:34.634 INFO: Press CTRL+C to quit
== APP - shipping == 2026-02-06 08:23:34.674 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - shipping ==  * Running on http://127.0.0.1:3004
== APP - shipping == 2026-02-06 08:23:34.674 INFO: Press CTRL+C to quit
== APP - order-processor == 2026-02-06 08:23:34.755 INFO: Starting workflow runtime...
== APP - order-processor == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - order-processor ==   warn(
== APP - order-processor == 2026-02-06 08:23:34.756 WorkflowRuntime INFO: Registering workflow 'process_order_workflow' with runtime
== APP - order-processor == 2026-02-06 08:23:34.756 INFO: Registering workflow 'process_order_workflow' with runtime
== APP - order-processor == 2026-02-06 08:23:34.756 WorkflowRuntime INFO: Registering activity 'notify' with runtime
== APP - order-processor == 2026-02-06 08:23:34.756 INFO: Registering activity 'notify' with runtime
== APP - order-processor == 2026-02-06 08:23:34.756 WorkflowRuntime INFO: Registering activity 'reserve_inventory' with runtime
== APP - order-processor == 2026-02-06 08:23:34.756 INFO: Registering activity 'reserve_inventory' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 WorkflowRuntime INFO: Registering activity 'submit_payment' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 INFO: Registering activity 'submit_payment' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 WorkflowRuntime INFO: Registering activity 'submit_order_to_shipping' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 INFO: Registering activity 'submit_order_to_shipping' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 WorkflowRuntime INFO: Registering activity 'refund_payment' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 INFO: Registering activity 'refund_payment' with runtime
== APP - order-processor == 2026-02-06 08:23:34.757 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - order-processor == 2026-02-06 08:23:34.757 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - order-processor ==  * Serving Flask app 'app'
== APP - order-processor ==  * Debug mode: off
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Starting Agent Worker Service...
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued workflow 'supervisor_workflow' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued workflow 'specialist_workflow' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued workflow 'atomic_task_workflow' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued activity 'announce' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued activity 'execute_atomic_task' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Queued activity 'validate_atomic_result' for registration
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Creating new WorkflowRuntime...
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Starting Chaos Engineering Service...
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: ⚡ CHAOS MODE ENABLED: Failure rate 50.0%
== APP - chaos-engineer == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - agent-worker == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - agent-worker ==   warn(
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering workflow 'supervisor_workflow' with runtime
== APP - chaos-engineer ==   warn(
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering workflow 'chaos_resilience_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering workflow 'supervisor_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering workflow 'specialist_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering workflow 'specialist_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering workflow 'chaos_resilience_workflow' with runtime
== APP - chaos-engineer ==  * Serving Flask app 'app'
== APP - chaos-engineer ==  * Debug mode: off
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering workflow 'atomic_task_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering workflow 'atomic_task_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_chaos_workflow_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_chaos_workflow_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_baseline_health_check_started' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering activity 'announce' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_atomic_task' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_baseline_health_check_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_failure_injection_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_failure_injection_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_resilience_test_round_started' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_atomic_task' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'validate_atomic_result' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Registering activity 'validate_atomic_result' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_resilience_test_round_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_retry_test_delay' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_retry_test_delay' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_circuit_breaker_test_started' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.764 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:23:34.764 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:23:34.765 INFO: WorkflowRuntime started successfully
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_circuit_breaker_test_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_cascade_failure_test_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_cascade_failure_test_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_recovery_test_started' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.765 INFO: Connection monitor started
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_recovery_test_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_chaos_workflow_completed' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_chaos_workflow_completed' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_external_event_starvation_started' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Starting returns workflow runtime...
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_external_event_starvation_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_child_workflow_zombie_detected' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_child_workflow_zombie_detected' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_activity_execution_limbo_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_activity_execution_limbo_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'announce_distributed_transaction_failure_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'announce_distributed_transaction_failure_started' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'perform_baseline_system_health_check' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'perform_baseline_system_health_check' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'perform_final_system_health_check' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'perform_final_system_health_check' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 WorkflowRuntime INFO: Registering activity 'activate_chaos_failure_scenario' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.763 INFO: Registering activity 'activate_chaos_failure_scenario' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'deactivate_chaos_failure_scenario' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'deactivate_chaos_failure_scenario' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_retry_policy_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_retry_policy_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_circuit_breaker_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_circuit_breaker_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_cascade_failure_simulation' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_cascade_failure_simulation' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_system_recovery_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_system_recovery_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_external_event_starvation_test' with runtime
== APP - returns == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - returns ==   warn(
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering workflow 'process_return_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_external_event_starvation_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_child_workflow_zombie_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_child_workflow_zombie_test' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering workflow 'process_return_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering workflow 'process_defective_return_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering workflow 'process_defective_return_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_activity_execution_limbo_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_activity_execution_limbo_test' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering workflow 'process_standard_return_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering workflow 'process_standard_return_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 WorkflowRuntime INFO: Registering activity 'execute_distributed_transaction_failure_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Registering activity 'execute_distributed_transaction_failure_test' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering workflow 'process_expedited_return_workflow' with runtime
== APP - chaos-engineer == 2026-02-06 08:23:34.764 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering workflow 'process_expedited_return_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_request_received' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_request_received' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_details_logged' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_details_logged' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_validation_started' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_validation_started' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_validation_passed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_validation_passed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_validation_failed' with runtime
== APP - agent-worker == 2026-02-06 08:23:34.768 INFO: Workflow runtime started on port 3012
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_validation_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_approval_required' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_approval_required' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_approval_received' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_approval_received' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_approval_rejected' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Starting Saga Demo Service...
== APP - agent-worker ==  * Serving Flask app 'app'
== APP - agent-worker ==  * Debug mode: off
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_approval_rejected' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_approval_timeout' with runtime
== APP - inventory ==  * Serving Flask app 'app'
== APP - inventory ==  * Debug mode: off
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'saga_order_workflow' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'order_monitor_workflow' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'fulfillment_workflow' for registration
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_approval_timeout' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_type_determination' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_type_determination' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'validation_workflow' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'address_check_workflow' for registration
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_child_workflow_spawned' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_child_workflow_spawned' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_processing_completed' with runtime
== APP - returns ==  * Serving Flask app 'app'
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued workflow 'payment_check_workflow' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'notify_saga' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'saga_reserve_inventory' for registration
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_processing_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_processing_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_processing_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_refund_summary' with runtime
== APP - returns ==  * Debug mode: off
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'saga_charge_payment' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'saga_create_shipment' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'compensate_release_inventory' for registration
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_refund_summary' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_return_inventory_summary' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_return_inventory_summary' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_defective_return_started' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'compensate_refund_payment' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'compensate_cancel_shipment' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'check_order_status' for registration
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_defective_return_started' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_defective_refund_processing' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_defective_refund_processing' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_defective_refund_failed' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.770 INFO: Starting Agent Coordinator Service...
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'validate_address' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'validate_payment' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Queued activity 'execute_fulfillment' for registration
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_defective_refund_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_defective_return_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_defective_return_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.767 WorkflowRuntime INFO: Registering activity 'announce_standard_return_started' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.770 INFO: Queued workflow 'project_coordinator_workflow' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Creating new WorkflowRuntime...
== APP - saga-demo == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - saga-demo ==   warn(
== APP - returns == 2026-02-06 08:23:34.767 INFO: Registering activity 'announce_standard_return_started' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_standard_refund_processing' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_standard_refund_processing' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_standard_refund_failed' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.770 INFO: Queued activity 'announce' for registration
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'saga_order_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'saga_order_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'order_monitor_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_standard_refund_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_standard_restocking_started' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_standard_restocking_started' with runtime
== APP - saga-demo ==  * Serving Flask app 'app'
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Starting batch processor workflow runtime...
== APP - agent-coordinator == 2026-02-06 08:23:34.770 INFO: Queued activity 'decompose_project' for registration
== APP - agent-coordinator == 2026-02-06 08:23:34.770 INFO: Creating new WorkflowRuntime...
== APP - agent-coordinator == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'order_monitor_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'fulfillment_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'fulfillment_workflow' with runtime
== APP - batch-processor == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - agent-coordinator ==   warn(
== APP - order-processor == 2026-02-06 08:23:34.773 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - batch-processor ==  * Serving Flask app 'app'
== APP - agent-coordinator ==  * Serving Flask app 'app'
== APP - agent-coordinator ==  * Debug mode: off
== APP - saga-demo ==  * Debug mode: off
== APP - batch-processor ==   warn(
== APP - agent-coordinator == 2026-02-06 08:23:34.771 WorkflowRuntime INFO: Registering workflow 'project_coordinator_workflow' with runtime
== APP - order-processor ==  * Running on all addresses (0.0.0.0)
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'validation_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_standard_restocking_warning' with runtime
== APP - batch-processor ==  * Debug mode: off
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering workflow 'process_bulk_order_workflow' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering workflow 'process_bulk_order_workflow' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering workflow 'process_single_item_workflow' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering workflow 'process_single_item_workflow' with runtime
== APP - order-processor ==  * Running on http://127.0.0.1:3006
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_standard_restocking_warning' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'validation_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'address_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'address_check_workflow' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 INFO: Registering workflow 'project_coordinator_workflow' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 INFO: Registering activity 'announce' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_standard_return_completed' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering workflow 'payment_check_workflow' with runtime
== APP - order-processor ==  * Running on http://192.168.0.223:3006
== APP - order-processor == 2026-02-06 08:23:34.773 INFO: Press CTRL+C to quit
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_bulk_order_started' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_bulk_order_started' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_child_workflow_spawned' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_child_workflow_spawned' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering workflow 'payment_check_workflow' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_standard_return_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_expedited_return_started' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_expedited_return_started' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 WorkflowRuntime INFO: Registering activity 'decompose_project' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 INFO: Registering activity 'decompose_project' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_expedited_parallel_processing' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'notify_saga' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'notify_saga' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'saga_reserve_inventory' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_waiting_for_children' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_waiting_for_children' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_expedited_parallel_processing' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'saga_reserve_inventory' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_item_success' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_expedited_refund_failed' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'saga_charge_payment' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_item_success' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_item_failure' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_item_failure' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'saga_charge_payment' with runtime
== APP - agent-coordinator == 2026-02-06 08:23:34.771 INFO: WorkflowRuntime started successfully
== APP - agent-coordinator == 2026-02-06 08:23:34.773 INFO: Connection monitor started
== APP - agent-coordinator == 2026-02-06 08:23:34.773 INFO: Workflow runtime started on port 3011
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_expedited_refund_failed' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'announce_expedited_return_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'announce_expedited_return_completed' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'validate_return_eligibility' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_bulk_order_completed' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'saga_create_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'saga_create_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'compensate_release_inventory' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'validate_return_eligibility' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'process_return_refund' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_bulk_order_completed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_bulk_order_partial_success' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'compensate_release_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'compensate_refund_payment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'compensate_refund_payment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'compensate_cancel_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'compensate_cancel_shipment' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'process_return_refund' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_bulk_order_partial_success' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_bulk_order_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_bulk_order_failed' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'check_order_status' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'check_order_status' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'validate_address' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_item_processing_started' with runtime
== APP - returns == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'restock_returned_inventory' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Registering activity 'restock_returned_inventory' with runtime
== APP - returns == 2026-02-06 08:23:34.768 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'validate_address' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'validate_payment' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_item_processing_started' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_inventory_reserved' with runtime
== APP - returns == 2026-02-06 08:23:34.768 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'validate_payment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 WorkflowRuntime INFO: Registering activity 'execute_fulfillment' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Registering activity 'execute_fulfillment' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_inventory_reserved' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_inventory_reservation_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_inventory_reservation_failed' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.768 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:34.768 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - batch-processor == 2026-02-06 08:23:34.772 WorkflowRuntime INFO: Registering activity 'announce_approval_required' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.772 INFO: Registering activity 'announce_approval_required' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_approval_received' with runtime
== APP - saga-demo == 2026-02-06 08:23:34.769 INFO: WorkflowRuntime started successfully
== APP - saga-demo == 2026-02-06 08:23:34.771 INFO: Connection monitor started
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_approval_received' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_approval_rejected' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_approval_rejected' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_approval_timeout' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_approval_timeout' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_payment_processing' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_payment_processing' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_payment_completed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_payment_completed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_payment_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_payment_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_shipping_submission' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_shipping_submission' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_shipping_scheduled' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_shipping_scheduled' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_shipping_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_shipping_failed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_payment_refunded' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_payment_refunded' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'announce_item_processing_completed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'announce_item_processing_completed' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'reserve_item_inventory' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'reserve_item_inventory' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'process_item_payment' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'process_item_payment' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'submit_item_for_shipping' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'submit_item_for_shipping' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 WorkflowRuntime INFO: Registering activity 'process_item_refund' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Registering activity 'process_item_refund' with runtime
== APP - batch-processor == 2026-02-06 08:23:34.773 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - batch-processor == 2026-02-06 08:23:34.773 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - chaos-engineer == 2026-02-06 08:23:34.805 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - chaos-engineer ==  * Running on all addresses (0.0.0.0)
== APP - chaos-engineer ==  * Running on http://127.0.0.1:3010
== APP - chaos-engineer ==  * Running on http://192.168.0.223:3010
== APP - chaos-engineer == 2026-02-06 08:23:34.805 INFO: Press CTRL+C to quit
== APP - batch-processor == 2026-02-06 08:23:34.805 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - batch-processor ==  * Running on all addresses (0.0.0.0)
== APP - batch-processor ==  * Running on http://127.0.0.1:3007
== APP - batch-processor ==  * Running on http://192.168.0.223:3007
== APP - batch-processor == 2026-02-06 08:23:34.805 INFO: Press CTRL+C to quit
== APP - returns == 2026-02-06 08:23:34.805 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - returns ==  * Running on all addresses (0.0.0.0)
== APP - returns ==  * Running on http://127.0.0.1:3008
== APP - returns ==  * Running on http://192.168.0.223:3008
== APP - returns == 2026-02-06 08:23:34.805 INFO: Press CTRL+C to quit
== APP - agent-worker == 2026-02-06 08:23:34.806 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - agent-worker ==  * Running on all addresses (0.0.0.0)
== APP - agent-worker ==  * Running on http://127.0.0.1:3012
== APP - agent-worker ==  * Running on http://192.168.0.223:3012
== APP - agent-worker == 2026-02-06 08:23:34.806 INFO: Press CTRL+C to quit
== APP - agent-coordinator == 2026-02-06 08:23:34.806 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - agent-coordinator ==  * Running on all addresses (0.0.0.0)
== APP - agent-coordinator ==  * Running on http://127.0.0.1:3011
== APP - agent-coordinator ==  * Running on http://192.168.0.223:3011
== APP - inventory == 2026-02-06 08:23:34.806 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - agent-coordinator == 2026-02-06 08:23:34.806 INFO: Press CTRL+C to quit
== APP - inventory ==  * Running on all addresses (0.0.0.0)
== APP - inventory ==  * Running on http://127.0.0.1:3002
== APP - inventory ==  * Running on http://192.168.0.223:3002
== APP - inventory == 2026-02-06 08:23:34.806 INFO: Press CTRL+C to quit
== APP - saga-demo == 2026-02-06 08:23:34.806 INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
== APP - saga-demo ==  * Running on all addresses (0.0.0.0)
== APP - saga-demo ==  * Running on http://127.0.0.1:3009
== APP - saga-demo ==  * Running on http://192.168.0.223:3009
== APP - saga-demo == 2026-02-06 08:23:34.806 INFO: Press CTRL+C to quit
== APP - notifications == [0]
== APP - notifications == [0] > vite_react_shadcn_ts@0.0.0 dev:server
== APP - notifications == [0] > node server.js
== APP - notifications == [0]
== APP - notifications == [1]
== APP - notifications == [1] > vite_react_shadcn_ts@0.0.0 dev:client
== APP - notifications == [1] > vite
== APP - notifications == [1]
== APP - notifications == [0] Running in production mode, serving from dist directory
== APP - notifications == [0] [2026-02-06T16:23:35.140Z] Server running on port 8085
== APP - notifications == [0] - API endpoint: http://localhost:8085/notifications
== APP - notifications == [0] - Socket.IO: ws://localhost:8085
== APP - notifications == [0] - Web UI: http://localhost:8085
== APP - notifications == [1]
== APP - notifications == [1]   VITE v5.4.10  ready in 147 ms
== APP - notifications == [1]
== APP - notifications == [1]   ➜  Local:   http://localhost:3000/
== APP - notifications == [1]   ➜  Network: http://192.168.0.223:3000/
== APP - returns == 2026-02-06 08:23:35.535 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:35.535 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - batch-processor == 2026-02-06 08:23:35.535 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - batch-processor == 2026-02-06 08:23:35.535 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - returns == 2026-02-06 08:23:35.535 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - returns == 2026-02-06 08:23:35.535 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - batch-processor == 2026-02-06 08:23:35.535 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - batch-processor == 2026-02-06 08:23:35.535 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-coordinator == 2026-02-06 08:23:35.543 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:23:35.543 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:23:35.543 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-coordinator == 2026-02-06 08:23:35.543 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - chaos-engineer == 2026-02-06 08:23:35.543 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - chaos-engineer == 2026-02-06 08:23:35.543 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:35.543 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - order-processor == 2026-02-06 08:23:35.543 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - order-processor == 2026-02-06 08:23:35.543 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:35.543 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:23:35.544 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - saga-demo == 2026-02-06 08:23:35.544 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - chaos-engineer == 2026-02-06 08:23:35.544 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - chaos-engineer == 2026-02-06 08:23:35.544 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - order-processor == 2026-02-06 08:23:35.544 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - order-processor == 2026-02-06 08:23:35.544 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-worker == 2026-02-06 08:23:38.503 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:23:38.503 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:23:38.505 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-worker == 2026-02-06 08:23:38.505 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
✅ Connected App ID "batch-processor" to http://:3007 ⚡️
✅ Connected App ID "notifications" to http://:8080 ⚡️
✅ Connected App ID "saga-demo" to http://:3009 ⚡️
✅ Connected App ID "shipping" to http://:3004 ⚡️
✅ Connected App ID "payments" to http://:3003 ⚡️
✅ Connected App ID "returns" to http://:3008 ⚡️
✅ Connected App ID "inventory" to http://:3002 ⚡️
✅ Connected App ID "chaos-engineer" to http://:3010 ⚡️
✅ Connected App ID "agent-coordinator" to http://:3011 ⚡️
✅ Connected App ID "agent-worker" to http://:3012 ⚡️
== APP - agent-coordinator == 2026-02-06 08:23:54.322 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:23:54.693 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:23:54.747 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:23:54.931 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:54] "GET /dapr/config HTTP/1.1" 404 -
== APP - payments == 2026-02-06 08:23:54.999 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:23:55.018 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /healthz HTTP/1.1" 200 -
== APP - chaos-engineer == 2026-02-06 08:23:55.104 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - agent-worker == 2026-02-06 08:23:55.306 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - returns == 2026-02-06 08:23:55.362 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - shipping == 2026-02-06 08:23:55.387 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - payments == 2026-02-06 08:23:55.619 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - batch-processor == 2026-02-06 08:23:55.628 INFO: 127.0.0.1 - - [06/Feb/2026 08:23:55] "GET /dapr/config HTTP/1.1" 404 -
== APP - inventory == 2026-02-06 08:24:01.700 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:01.982 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:01] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:24:02.333 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:02] "GET /dapr/config HTTP/1.1" 404 -
== APP - saga-demo == 2026-02-06 08:24:02.618 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:02] "GET /dapr/config HTTP/1.1" 404 -
== APP - agent-coordinator == 2026-02-06 08:24:04.309 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:04.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:04.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:24:04.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:05.025 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:24:11.733 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:11.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:24:14.298 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:14.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:14.741 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:24:14.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:15.003 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:15] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:17.982 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - saga-demo == 	status = StatusCode.UNAVAILABLE
== APP - saga-demo == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - saga-demo == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - saga-demo == >
== APP - saga-demo == 2026-02-06 08:24:17.982 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - saga-demo == 	status = StatusCode.UNAVAILABLE
== APP - saga-demo == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - saga-demo == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - saga-demo == >
== APP - saga-demo == 2026-02-06 08:24:17.983 durabletask-worker INFO: Work item stream ended normally
== APP - saga-demo == 2026-02-06 08:24:17.983 INFO: Work item stream ended normally
== APP - saga-demo == 2026-02-06 08:24:17.983 durabletask-worker INFO: No longer listening for work items
== APP - saga-demo == 2026-02-06 08:24:17.983 INFO: No longer listening for work items
== APP - inventory == 2026-02-06 08:24:21.709 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:21.988 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:24:24.300 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:24.688 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:24.744 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:24] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:24.790 WARNING: Worker disconnected, attempting reconnection...
== APP - saga-demo == 2026-02-06 08:24:24.791 durabletask-worker INFO: Stopping gRPC worker...
== APP - saga-demo == 2026-02-06 08:24:24.791 INFO: Stopping gRPC worker...
== APP - saga-demo == 2026-02-06 08:24:24.791 durabletask-worker INFO: Worker shutdown completed
== APP - saga-demo == 2026-02-06 08:24:24.791 INFO: Worker shutdown completed
== APP - saga-demo == 2026-02-06 08:24:24.791 INFO: Reconnection attempt #1
== APP - payments == 2026-02-06 08:24:24.982 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:25.020 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:25] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Creating new WorkflowRuntime...
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'saga_order_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'saga_order_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Registering workflow 'saga_order_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'order_monitor_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'order_monitor_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Registering workflow 'order_monitor_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'fulfillment_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'fulfillment_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Registering workflow 'fulfillment_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'validation_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'validation_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Registering workflow 'validation_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'address_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 WorkflowRuntime INFO: Registering workflow 'address_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.796 INFO: Registering workflow 'address_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering workflow 'payment_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering workflow 'payment_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering workflow 'payment_check_workflow' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'notify_saga' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'notify_saga' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'notify_saga' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_reserve_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_reserve_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'saga_reserve_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_charge_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_charge_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'saga_charge_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_create_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'saga_create_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'saga_create_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_release_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_release_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'compensate_release_inventory' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_refund_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_refund_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'compensate_refund_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_cancel_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 WorkflowRuntime INFO: Registering activity 'compensate_cancel_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.797 INFO: Registering activity 'compensate_cancel_shipment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'check_order_status' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'check_order_status' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 INFO: Registering activity 'check_order_status' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'validate_address' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'validate_address' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 INFO: Registering activity 'validate_address' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'validate_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'validate_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 INFO: Registering activity 'validate_payment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'execute_fulfillment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 WorkflowRuntime INFO: Registering activity 'execute_fulfillment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 INFO: Registering activity 'execute_fulfillment' with runtime
== APP - saga-demo == 2026-02-06 08:24:26.798 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:26.798 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:26.798 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:26.800 INFO: WorkflowRuntime started successfully
== APP - saga-demo == 2026-02-06 08:24:26.800 INFO: Reconnection successful
== APP - saga-demo == 2026-02-06 08:24:27.511 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:27.511 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:27.511 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - saga-demo == 2026-02-06 08:24:27.511 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - saga-demo == 2026-02-06 08:24:27.511 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - saga-demo == 2026-02-06 08:24:27.511 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-coordinator == 2026-02-06 08:24:30.050 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - agent-coordinator == 	status = StatusCode.UNAVAILABLE
== APP - agent-coordinator == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - agent-coordinator == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - agent-coordinator == >
== APP - agent-coordinator == 2026-02-06 08:24:30.050 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - agent-coordinator == 	status = StatusCode.UNAVAILABLE
== APP - agent-coordinator == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - agent-coordinator == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - agent-coordinator == >
== APP - agent-coordinator == 2026-02-06 08:24:30.052 durabletask-worker INFO: Work item stream ended normally
== APP - agent-coordinator == 2026-02-06 08:24:30.052 INFO: Work item stream ended normally
== APP - agent-coordinator == 2026-02-06 08:24:30.052 durabletask-worker INFO: No longer listening for work items
== APP - agent-coordinator == 2026-02-06 08:24:30.052 INFO: No longer listening for work items
== APP - agent-worker == 2026-02-06 08:24:31.166 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - agent-worker == 	status = StatusCode.UNAVAILABLE
== APP - agent-worker == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - agent-worker == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - agent-worker == >
== APP - agent-worker == 2026-02-06 08:24:31.166 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - agent-worker == 	status = StatusCode.UNAVAILABLE
== APP - agent-worker == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - agent-worker == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - agent-worker == >
== APP - agent-worker == 2026-02-06 08:24:31.167 durabletask-worker INFO: Work item stream ended normally
== APP - agent-worker == 2026-02-06 08:24:31.167 INFO: Work item stream ended normally
== APP - agent-worker == 2026-02-06 08:24:31.167 durabletask-worker INFO: No longer listening for work items
== APP - agent-worker == 2026-02-06 08:24:31.167 INFO: No longer listening for work items
== APP - returns == 2026-02-06 08:24:31.174 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - returns == 	status = StatusCode.UNAVAILABLE
== APP - returns == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - returns == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - returns == >
== APP - returns == 2026-02-06 08:24:31.174 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - returns == 	status = StatusCode.UNAVAILABLE
== APP - returns == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - returns == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - returns == >
== APP - returns == 2026-02-06 08:24:31.174 durabletask-worker INFO: Work item stream ended normally
== APP - returns == 2026-02-06 08:24:31.174 INFO: Work item stream ended normally
== APP - returns == 2026-02-06 08:24:31.174 durabletask-worker INFO: No longer listening for work items
== APP - returns == 2026-02-06 08:24:31.174 INFO: No longer listening for work items
== APP - inventory == 2026-02-06 08:24:31.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:31] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:31.876 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - batch-processor == 	status = StatusCode.UNAVAILABLE
== APP - batch-processor == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - batch-processor == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - batch-processor == >
== APP - batch-processor == 2026-02-06 08:24:31.876 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - batch-processor == 	status = StatusCode.UNAVAILABLE
== APP - batch-processor == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - batch-processor == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_status:14, grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination"}"
== APP - batch-processor == >
== APP - batch-processor == 2026-02-06 08:24:31.876 durabletask-worker INFO: Work item stream ended normally
== APP - batch-processor == 2026-02-06 08:24:31.876 INFO: Work item stream ended normally
== APP - batch-processor == 2026-02-06 08:24:31.876 durabletask-worker INFO: No longer listening for work items
== APP - batch-processor == 2026-02-06 08:24:31.876 INFO: No longer listening for work items
== APP - saga-demo == 2026-02-06 08:24:31.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:31] "GET /healthz HTTP/1.1" 200 -
== APP - chaos-engineer == 2026-02-06 08:24:32.182 durabletask-worker WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - chaos-engineer == 	status = StatusCode.UNAVAILABLE
== APP - chaos-engineer == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - chaos-engineer == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - chaos-engineer == >
== APP - chaos-engineer == 2026-02-06 08:24:32.182 WARNING: Stream reader: RPC error (code=StatusCode.UNAVAILABLE): <_MultiThreadedRendezvous of RPC that terminated with:
== APP - chaos-engineer == 	status = StatusCode.UNAVAILABLE
== APP - chaos-engineer == 	details = "upstream connect error or disconnect/reset before headers. reset reason: connection termination"
== APP - chaos-engineer == 	debug_error_string = "UNKNOWN:Error received from peer  {grpc_message:"upstream connect error or disconnect/reset before headers. reset reason: connection termination", grpc_status:14}"
== APP - chaos-engineer == >
== APP - chaos-engineer == 2026-02-06 08:24:32.183 durabletask-worker INFO: Work item stream ended normally
== APP - chaos-engineer == 2026-02-06 08:24:32.183 INFO: Work item stream ended normally
== APP - chaos-engineer == 2026-02-06 08:24:32.183 durabletask-worker INFO: No longer listening for work items
== APP - chaos-engineer == 2026-02-06 08:24:32.183 INFO: No longer listening for work items
== APP - agent-coordinator == 2026-02-06 08:24:34.351 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:34.694 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:34.748 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:34.787 WARNING: Worker disconnected, attempting reconnection...
== APP - agent-worker == 2026-02-06 08:24:34.788 durabletask-worker INFO: Stopping gRPC worker...
== APP - agent-worker == 2026-02-06 08:24:34.788 INFO: Stopping gRPC worker...
== APP - agent-worker == 2026-02-06 08:24:34.788 durabletask-worker INFO: Worker shutdown completed
== APP - agent-worker == 2026-02-06 08:24:34.788 INFO: Worker shutdown completed
== APP - agent-worker == 2026-02-06 08:24:34.788 INFO: Reconnection attempt #1
== APP - agent-coordinator == 2026-02-06 08:24:34.791 WARNING: Worker disconnected, attempting reconnection...
== APP - agent-coordinator == 2026-02-06 08:24:34.791 durabletask-worker INFO: Stopping gRPC worker...
== APP - agent-coordinator == 2026-02-06 08:24:34.791 INFO: Stopping gRPC worker...
== APP - agent-coordinator == 2026-02-06 08:24:34.792 durabletask-worker INFO: Worker shutdown completed
== APP - agent-coordinator == 2026-02-06 08:24:34.792 INFO: Worker shutdown completed
== APP - agent-coordinator == 2026-02-06 08:24:34.792 INFO: Reconnection attempt #1
== APP - payments == 2026-02-06 08:24:34.976 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:35.023 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:35] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:36.791 INFO: Creating new WorkflowRuntime...
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'supervisor_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'supervisor_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering workflow 'supervisor_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'specialist_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'specialist_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering workflow 'specialist_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'atomic_task_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering workflow 'atomic_task_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering workflow 'atomic_task_workflow' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering activity 'announce' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'execute_atomic_task' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'execute_atomic_task' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering activity 'execute_atomic_task' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'validate_atomic_result' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 WorkflowRuntime INFO: Registering activity 'validate_atomic_result' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Registering activity 'validate_atomic_result' with runtime
== APP - agent-worker == 2026-02-06 08:24:36.792 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:24:36.792 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:24:36.792 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:36.794 INFO: Creating new WorkflowRuntime...
== APP - agent-worker == 2026-02-06 08:24:36.793 INFO: WorkflowRuntime started successfully
== APP - agent-worker == 2026-02-06 08:24:36.794 INFO: Reconnection successful
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering workflow 'project_coordinator_workflow' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering workflow 'project_coordinator_workflow' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 INFO: Registering workflow 'project_coordinator_workflow' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering activity 'announce' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 INFO: Registering activity 'announce' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering activity 'decompose_project' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 WorkflowRuntime INFO: Registering activity 'decompose_project' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 INFO: Registering activity 'decompose_project' with runtime
== APP - agent-coordinator == 2026-02-06 08:24:36.794 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:36.794 durabletask-worker INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:36.794 INFO: Starting gRPC worker that connects to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:36.795 INFO: WorkflowRuntime started successfully
== APP - agent-coordinator == 2026-02-06 08:24:36.795 INFO: Reconnection successful
== APP - agent-coordinator == 2026-02-06 08:24:37.492 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:37.492 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:37.492 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-coordinator == 2026-02-06 08:24:37.494 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-coordinator == 2026-02-06 08:24:37.494 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-coordinator == 2026-02-06 08:24:37.494 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-worker == 2026-02-06 08:24:37.500 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:24:37.500 durabletask-worker INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:24:37.500 INFO: Created fresh connection to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443
== APP - agent-worker == 2026-02-06 08:24:37.501 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-worker == 2026-02-06 08:24:37.501 durabletask-worker INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - agent-worker == 2026-02-06 08:24:37.501 INFO: Successfully connected to dns:grpc-prj1183404.cloud.staging.diagrid.dev:443. Waiting for work items...
== APP - inventory == 2026-02-06 08:24:41.680 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:41.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:24:44.306 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:44.698 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:44.745 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:24:45.001 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:45] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:45.006 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:24:51.706 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:24:51.982 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:51] "GET /healthz HTTP/1.1" 200 -
== APP - chaos-engineer == 2026-02-06 08:24:52.299 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:52] "GET /chaos/status HTTP/1.1" 200 -
== APP - order-processor == 2026-02-06 08:24:52.310 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:52] "GET /circuit-breakers HTTP/1.1" 200 -
== APP - inventory == /Users/helion/repos/catalyst-order-workflow/diagrid-venv/lib/python3.13/site-packages/dapr/conf/helpers.py:43: UserWarning: http and https schemes are deprecated for grpc, use myhost?tls=false or myhost?tls=true instead
== APP - inventory ==   warn(
== APP - agent-coordinator == 2026-02-06 08:24:54.305 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:24:54.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /api/v1/inventory HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:24:54.700 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /healthz HTTP/1.1" 200 -
== APP - chaos-engineer == 2026-02-06 08:24:54.717 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /chaos/status HTTP/1.1" 200 -
== APP - order-processor == 2026-02-06 08:24:54.731 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /circuit-breakers HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:24:54.740 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /healthz HTTP/1.1" 200 -
== APP - chaos-engineer == 2026-02-06 08:24:54.747 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "POST /chaos/scenarios HTTP/1.1" 201 -
== APP - chaos-engineer == 2026-02-06 08:24:54.770 durabletask-client INFO: Starting new 'chaos_resilience_workflow' instance with ID = 'chaos_quick_payment_timeout_demo_6507_1770395094'.
== APP - chaos-engineer == 2026-02-06 08:24:54.770 INFO: Starting new 'chaos_resilience_workflow' instance with ID = 'chaos_quick_payment_timeout_demo_6507_1770395094'.
== APP - payments == 2026-02-06 08:24:54.999 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:24:55.005 INFO: 127.0.0.1 - - [06/Feb/2026 08:24:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:01.681 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:01.982 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:04.371 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:04.693 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:04.741 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:04.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:05.013 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:11.703 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:11.986 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:14.306 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:14.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:14.746 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:15.004 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:15] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:15.033 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:21.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:21.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:24.300 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:24.686 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:24.753 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:24.995 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:25.011 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:31.682 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:31.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:34.306 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:34.693 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:34.761 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:34.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:35.002 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:41.703 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:42.014 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:42] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:44.313 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:44.694 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:44.750 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:44.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:45.014 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:25:51.684 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:25:51.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:25:54.296 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:25:54.697 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:25:54.753 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:25:54.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:25:55.013 INFO: 127.0.0.1 - - [06/Feb/2026 08:25:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:01.681 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:01.978 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:04.381 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:04.688 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:04.747 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:04.992 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:05.030 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:11.687 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:11.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:14.299 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:14.699 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:14.743 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:14.992 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:15.021 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:21.711 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:21.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:24.302 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:24.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:24.748 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:24.986 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:25.012 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:31.677 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:31.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:34.311 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:34.702 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:34.757 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:34.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:35.032 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:41.702 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:41.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:44.310 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:44.690 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:44.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:44.980 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:45.020 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:26:51.697 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:26:51.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:26:54.303 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:26:54.687 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:26:54.753 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:26:54.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:26:55.016 INFO: 127.0.0.1 - - [06/Feb/2026 08:26:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:01.701 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:01.988 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:04.299 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:04.690 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:04.753 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:04.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:05.020 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:11.680 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:11.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:14.299 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:14.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:14.754 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:14.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:15.006 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:21.704 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:21.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:24.302 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:24.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:24.747 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:24.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:25.031 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:31.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:31.988 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:34.307 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:34.701 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:34.741 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:34.988 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:35.011 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:41.673 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:41.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:44.304 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:44.689 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:44.749 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:44.989 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:45.013 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:27:51.717 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:27:52.003 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:52] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:27:54.296 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:27:54.694 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:27:54.754 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:27:54.989 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:27:55.013 INFO: 127.0.0.1 - - [06/Feb/2026 08:27:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:01.707 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:01.976 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:04.387 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:04.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:04.755 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:04.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:05.018 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:11.676 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:11.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:14.292 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:14.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:14.755 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:14.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:15.021 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:21.702 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:21.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:24.308 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:24.700 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:24.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:24.983 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:25.031 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:31.697 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:31.980 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:34.297 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:34.708 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:34.754 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:34.992 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:35.027 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:41.691 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:41.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:44.297 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:44.700 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:44.745 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:44.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:45.022 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:28:51.693 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:28:51.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:28:54.302 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:28:54.694 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:28:54.749 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:28:54.976 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:28:55.033 INFO: 127.0.0.1 - - [06/Feb/2026 08:28:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:01.703 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:01.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:04.311 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:04.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:04.749 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:04.979 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:05.014 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:11.677 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:11.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:14.300 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:14.691 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:14.746 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:14.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:15.037 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:21.700 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:21.980 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:24.307 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:24.699 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:24.779 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:25.002 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:25] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:25.012 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:31.697 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:31.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:34.393 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:34.694 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:34.750 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:34.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:35.008 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:41.702 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:41.982 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:44.302 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:44.697 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:44.752 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:44.994 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:45.028 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:29:51.681 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:29:51.994 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:29:54.369 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:29:54.691 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:29:54.754 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:29:54.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:29:55.015 INFO: 127.0.0.1 - - [06/Feb/2026 08:29:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:01.679 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:01.977 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:04.398 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:04.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:04.759 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:04.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:05.012 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:11.681 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:11.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:14.303 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:14.703 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:14.756 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:14.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:15.008 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:21.699 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:21.988 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:24.311 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:24.690 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:24.749 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:24.998 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:25.017 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:31.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:31.977 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:31] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:34.406 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:34.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:34.746 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:34.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:35.010 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:41.685 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:41.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:44.303 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:44.705 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:44.749 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:44.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:45.005 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:30:51.698 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:30:51.983 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:30:54.380 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:30:54.699 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:30:54.753 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:30:54.986 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:30:55.025 INFO: 127.0.0.1 - - [06/Feb/2026 08:30:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:01.711 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:01.985 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:04.348 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:04.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:04.736 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:04.995 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:05.017 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:11.687 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:11.989 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:14.295 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:14.701 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:14.756 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:14.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:15.015 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:15] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:21.679 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:21] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:21.984 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:21] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:24.308 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:24] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:24.698 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:24] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:24.755 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:24] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:24.995 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:24] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:25.010 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:25] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:31.703 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:31] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:32.002 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:32] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:34.311 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:34] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:34.695 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:34] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:34.743 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:34] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:34.993 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:34] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:35.022 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:35] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:41.685 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:41] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:41.981 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:41] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:44.309 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:44] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:44.685 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:44] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:44.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:44] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:44.983 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:44] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:45.020 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:45] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:31:51.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:51] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:31:51.987 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:51] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:31:54.315 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:54] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:31:54.692 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:54] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:31:54.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:54] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:31:54.997 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:54] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:31:55.012 INFO: 127.0.0.1 - - [06/Feb/2026 08:31:55] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:32:01.686 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:01] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:32:01.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:01] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:32:04.313 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:04] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:32:04.696 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:04] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:32:04.760 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:04] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:32:04.991 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:04] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:32:05.017 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:05] "GET /healthz HTTP/1.1" 200 -
== APP - inventory == 2026-02-06 08:32:11.677 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:11] "GET /healthz HTTP/1.1" 200 -
== APP - saga-demo == 2026-02-06 08:32:11.990 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:11] "GET /healthz HTTP/1.1" 200 -
== APP - agent-coordinator == 2026-02-06 08:32:14.317 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:14] "GET /healthz HTTP/1.1" 200 -
== APP - agent-worker == 2026-02-06 08:32:14.698 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:14] "GET /healthz HTTP/1.1" 200 -
== APP - returns == 2026-02-06 08:32:14.751 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:14] "GET /healthz HTTP/1.1" 200 -
== APP - payments == 2026-02-06 08:32:14.989 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:14] "GET /healthz HTTP/1.1" 200 -
== APP - batch-processor == 2026-02-06 08:32:15.041 INFO: 127.0.0.1 - - [06/Feb/2026 08:32:15] "GET /healthz HTTP/1.1" 200 -
^C✅ Disconnected App ID "inventory"
✅ Disconnected App ID "payments"
✅ Disconnected App ID "notifications"
✅ Disconnected App ID "shipping"
✅ Disconnected App ID "batch-processor"
✅ Disconnected App ID "returns"
✅ Disconnected App ID "chaos-engineer"
✅ Disconnected App ID "saga-demo"
✅ Disconnected App ID "agent-coordinator"
✅ Disconnected App ID "agent-worker"
✅ Exited app "inventory" successfully
✅ Exited app "order-processor" successfully
✅ Exited app "payments" successfully
✅ Exited app "notifications" successfully
✅ Exited app "shipping" successfully
✅ Exited app "batch-processor" successfully
✅ Exited app "returns" successfully
✅ Exited app "chaos-engineer" successfully
✅ Exited app "saga-demo" successfully
✅ Exited app "agent-coordinator" successfully
✅ Exited app "agent-worker" successfully
ℹ️  Shutting down...
