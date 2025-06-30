# Catalyst Order Processing Workflow

This solution demonstrates the capabilities provided by all five Catalyst APIs through a python-based order processing workflow. The end-to-end solution is comprised of five services:

- **order-processor**: Contains the order process workflow definition and all associated activity methods which will be executed as part of the workflow sequence using the Catalyst Workflow API.
- **batch-processor**: Handles bulk orders by implementing parent workflows that spawn child workflows for each item, demonstrating advanced workflow patterns and parallel processing.
- **inventory**: Receives direct invocation requests sent by the order-processor using the Invocation API to manage inventory state in the Diagrid KV Store through the Catalyst State API.
- **notifications**: Subscribes to messages published by the order-processor using the Pub/Sub API and subsequently displays those messages through a simple JavaScript user interface.
- **shipping**: Receives direct invocation requests sent by the order-processor using the Invocation API to simulate the scheduling of order shipments.
- **payments**: Receives direct invocation requests sent by the order-processor using the Invocation API to mock the processing of order payments.

## Prerequisites
- [Sign up](https://catalyst.diagrid.io) for Diagrid Catalyst
- Install latest [Diagrid CLI](https://docs.diagrid.io/catalyst/references/cli-reference/intro#installing-the-cli)
- Install [Python3](https://www.python.org/downloads/)
- Install [Node.js](https://nodejs.org/) (version 20 or higher) and npm

### Prepare applications

The build apps file will go through each application directory and run any app commands necessary to prepare the applications to run. Make sure it is executable using the below command:

```bash
chmod +X build-apps.sh
```

Run the script:

```bash
./build-apps.sh
```

## Deploy Catalyst resources

Replace `unique-project-name` with a name for your workflow project

```bash
export WORKFLOW_PROJECT_NAME="unique-project-name"
```

Execute the following command to run your applications locally and create the dependent Catalyst resources:

```bash
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

## Use the APIs

A `test.rest` file is available at the root of this repository and can be used with the VS Code `Rest Client` extension.
    ![Rest Client](/images/rest-client.png)

## Bulk Order Processing (Child Workflows)

The application now includes advanced workflow patterns with **parent-child workflows** via the `batch-processor` service:

### Features:
- **Parent Workflow**: Processes bulk orders containing multiple items
- **Child Workflows**: Each item spawns its own workflow for parallel processing
- **Real-time Notifications**: Track progress of both parent and child workflows
- **Failure Handling**: Graceful handling of partial failures in bulk orders

### Example Bulk Order Request:
```json
POST http://localhost:3007/bulk-orders
Content-Type: application/json

{
  "customer": "alice",
  "items": [
    {"item": "apple", "quantity": 2, "price": 50.0},
    {"item": "orange", "quantity": 1, "price": 75.0},
    {"item": "pear", "quantity": 3, "price": 30.0}
  ]
}
```

### Check Bulk Order Status:
```http
GET http://localhost:3007/bulk-orders/{instance_id}
```

This demonstrates how Dapr workflows can orchestrate complex business processes using parent-child relationships, making it perfect for scenarios like:
- Multi-item order processing
- Batch operations
- Parallel task execution
- Coordinated microservice interactions
