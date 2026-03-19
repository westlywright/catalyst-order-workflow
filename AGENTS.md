# AGENTS.md
This file provides guidance to AI coding assistants working in this repository.

**Note:** CLAUDE.md, .clinerules, .cursorrules, .windsurfrules, .replit.md, GEMINI.md, .github/copilot-instructions.md, and .idx/airules.md are symlinks to AGENTS.md in this project.

# Catalyst Order Processing Workflow

A multi-service order processing system demonstrating Diagrid Catalyst APIs with advanced patterns including bulk processing, returns management, and chaos engineering for resilience testing.

## Project Overview

**Architecture:** Microservices with Dapr sidecar pattern
- **8 services** orchestrated via Dapr
- **7 Python Flask services** for backend processing
- **1 Node.js/React service** for real-time UI notifications
- **Dapr components** for state management, pub/sub messaging, and workflows

**Core Services:**
| Service | Port | Language | Purpose |
|---------|------|----------|---------|
| order-processor | 3006 | Python | Main workflow engine with approval handling and circuit breaker patterns |
| inventory | 3013 | Python | Inventory management using Catalyst State API |
| payments | 3014 | Python | Payment processing with failure simulation |
| shipping | 3004 | Python | Shipping coordination service |
| notifications | 8080 | Node.js/React | Real-time workflow monitoring UI |
| batch-processor | 3007 | Python | Bulk order processing with parent-child workflows |
| returns | 3008 | Python | Return processing with workflow chaining |
| chaos-engineer | 3010 | Python | Failure simulation and resilience testing |

## Build & Commands

### Setup & Installation

```bash
# Initial setup - install all dependencies and build
chmod +x build-apps.sh
./build-apps.sh
```

### Running the Application

```bash
# Set your Catalyst project name
export WORKFLOW_PROJECT_NAME="unique-project-name"

# Start all services with Dapr
diagrid dev run -f dapr.yaml --project $WORKFLOW_PROJECT_NAME
```

### Notifications Service (Node.js/React)

```bash
cd services/notifications

# Development mode (concurrent client + server)
npm run dev

# Development client only (Vite dev server on port 3000)
npm run dev:client

# Development server only (Express on port 8085)
npm run dev:server

# Production build
npm run build

# Preview production build
npm run preview

# Start production server
npm start
```

### Python Services

```bash
# Install dependencies for a specific service
cd services/<service-name>
pip3 install -r requirements.txt

# Run a service directly (usually started via dapr.yaml)
python3 app.py
```

### Script Command Consistency
**Important**: When modifying npm scripts in package.json, ensure all references are updated:
- `dapr.yaml` - Dapr app configurations
- `build-apps.sh` - Build automation script
- `README.md` - Project documentation

## Code Style

### Python Services

**Framework:** Flask with Dapr SDK

**Imports:**
- Standard library imports first
- Third-party imports (dapr, flask, grpc)
- Local imports last
- Use `from typing import ...` for type hints

**Naming Conventions:**
- Functions: `snake_case` (e.g., `reserve_inventory`, `submit_payment`)
- Classes: `PascalCase` (e.g., `Order`, `InventoryResult`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `APP_PORT`, `PUBSUB_NAME`)
- Private functions: `_leading_underscore`

**Dataclasses:** Use `@dataclass` for data structures:
```python
@dataclass
class Order:
    id: str
    customer: str
    item: str
    total: float
```

**Logging:**
```python
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)
```

**Flask Routes:**
- RESTful patterns: GET for retrieval, POST for creation
- Health checks at `/healthz` or `/health`
- JSON responses with `jsonify()`
- Error responses include `"error"` and `"message"` fields

**Error Handling:**
```python
try:
    # operation
except grpc.RpcError as err:
    logger.error(f'Error: {err.details()}')
    return make_response(
        jsonify({"error": "Internal Server Error", "message": "..."}),
        500
    )
```

### TypeScript/React (Notifications Service)

**Framework:** React 18 with TypeScript, Vite, shadcn/ui, Tailwind CSS

**File Organization:**
```
src/
├── components/       # React components
│   ├── ui/          # shadcn/ui components
│   └── *.tsx        # Custom components
├── context/         # React context providers
├── hooks/           # Custom hooks
├── pages/           # Page components
└── lib/             # Utilities
```

**Imports:**
```typescript
// React imports first
import React, { useEffect, useContext, useRef } from 'react';
// Third-party imports
import { io } from 'socket.io-client';
// Local imports with @ alias
import { MessageContext } from '@/context/MessageContext';
import { useToast } from '@/hooks/use-toast';
import { Card } from '@/components/ui/card';
```

**Component Pattern:**
```typescript
const ComponentName = () => {
  // State and hooks at top
  const [state, setState] = useState<Type>('initial');
  const { contextValue } = useContext(SomeContext);

  // Effects
  useEffect(() => {
    // effect logic
    return () => {
      // cleanup
    };
  }, [dependencies]);

  // Render
  return (
    <div className="tailwind-classes">
      {/* JSX */}
    </div>
  );
};

export default ComponentName;
```

**TypeScript:**
- Use explicit types for props and state
- Use `interface` for object shapes
- Global type extensions in component files when needed:
```typescript
declare global {
  interface Window {
    _connectionStatus: 'open' | 'closed' | 'connecting';
  }
}
```

**TypeScript Config (relaxed):**
- `noImplicitAny: false`
- `strictNullChecks: false`
- `allowJs: true`

**Styling:**
- Tailwind CSS utility classes
- `className` with template literals or `clsx`
- shadcn/ui components for consistent UI

## Testing

### Manual Testing (VS Code REST Client)
- `test-commands.http` - Basic workflow testing
- `bulk-demo.http` - Bulk order processing
- `return-demo.http` - Return workflow testing
- `chaos-demo.http` - Basic chaos engineering
- `advanced-chaos-demo.http` - Advanced workflow failures

### Automated Testing (Bash Scripts)
```bash
# Basic chaos patterns
./run-chaos-demo.sh

# Multi-service failures
./run-advanced-chaos-demo.sh

# Advanced workflow debugging
./run-advanced-workflow-chaos-demo.sh
```

### Testing Philosophy
**When tests fail, fix the code, not the test.**

Key principles:
- Tests should be meaningful - Avoid tests that always pass regardless of behavior
- Test actual functionality - Call the functions being tested
- Failing tests are valuable - They reveal bugs or missing features
- Fix the root cause - When a test fails, fix the underlying issue

## Security

### Environment Variables
- `APP_PORT` - Service port configuration
- `PUBSUB_NAME` - Dapr pub/sub component name
- `TOPIC_NAME` - Notification topic name
- `STATESTORE_NAME` - Dapr state store component name
- `WORKFLOW_PROJECT_NAME` - Diagrid Catalyst project name

### Best Practices
- No hardcoded credentials in code
- Use Dapr for service-to-service communication (mTLS by default)
- Circuit breaker patterns for resilience
- Input validation on all API endpoints

## Configuration

### Dapr Configuration (`dapr.yaml`)
Defines all service configurations including:
- App IDs and ports
- Health check endpoints (`/healthz`)
- Command to start each service
- Resource paths (`./resources`)

### Dapr Resources (`resources/`)
- `pubsub.yaml` - Redis pub/sub configuration
- `state.yaml` - State store configuration
- `subscription.yaml` - Topic subscriptions

### TypeScript Configuration
- Path alias: `@/*` maps to `./src/*`
- Vite dev server on port 3000 with proxy to Express backend
- Socket.IO WebSocket proxy configured

## Directory Structure & File Organization

### Reports Directory
ALL project reports and documentation should be saved to the `reports/` directory:

```
catalyst-order-workflow/
├── reports/              # All project reports and documentation
│   └── *.md             # Various report types
├── temp/                # Temporary files and debugging
├── services/            # Microservices
│   ├── batch-processor/
│   ├── chaos-engineer/
│   ├── inventory/
│   ├── notifications/   # React/Node.js UI
│   ├── order-processor/
│   ├── payments/
│   ├── returns/
│   └── shipping/
├── resources/           # Dapr component configurations
└── *.http              # API test files
```

### Report Generation Guidelines
**Important**: ALL reports should be saved to the `reports/` directory with descriptive names:

**Implementation Reports:**
- Phase validation: `PHASE_X_VALIDATION_REPORT.md`
- Implementation summaries: `IMPLEMENTATION_SUMMARY_[FEATURE].md`
- Feature completion: `FEATURE_[NAME]_REPORT.md`

**Testing & Analysis Reports:**
- Test results: `TEST_RESULTS_[DATE].md`
- Performance analysis: `PERFORMANCE_ANALYSIS_[SCENARIO].md`

**Report Naming Conventions:**
- Use descriptive names: `[TYPE]_[SCOPE]_[DATE].md`
- Include dates: `YYYY-MM-DD` format
- Group with prefixes: `TEST_`, `PERFORMANCE_`, `CHAOS_`
- Markdown format: All reports end in `.md`

### Temporary Files & Debugging
All temporary files, debugging scripts, and test artifacts should be organized in a `/temp` folder:

**Guidelines:**
- Never commit files from `/temp` directory
- Use `/temp` for all debugging and analysis scripts
- Clean up `/temp` directory regularly

### Claude Code Settings (.claude Directory)

#### Version Controlled Files (commit these):
- `.claude/settings.json` - Shared team settings
- `.claude/commands/*.md` - Custom slash commands

#### Ignored Files (do NOT commit):
- `.claude/settings.local.json` - Personal preferences

## API Endpoints

### Order Processor (port 3006)
- `POST /orders` - Submit new order
- `GET /orders/<order_id>` - Check order status
- `POST /orders/<order_id>/approve` - Approve high-value order
- `GET /circuit-breakers` - Circuit breaker status

### Inventory (port 3013)
- `GET /api/v1/inventory` - List inventory
- `DELETE /api/v1/inventory` - Clear inventory
- `POST /api/v1/inventory/restock` - Restock inventory
- `POST /api/v1/inventory/reserve` - Reserve inventory

### Batch Processor (port 3007)
- `POST /bulk-orders` - Submit bulk order

### Returns (port 3008)
- `POST /returns` - Submit return request

### Chaos Engineer (port 3010)
- `/chaos/events` - Diagnostic events for dashboards
- `/chaos/advanced-failures` - Advanced failure states
- `/chaos/zombie-workflows` - Zombie workflow detection

### Notifications (port 8080)
- `GET /healthz` - Health check
- `POST /notifications` - Receive notification events
- WebSocket at `ws://localhost:8080` for real-time updates

## Agent Delegation & Tool Execution

### Always Delegate to Specialists & Execute in Parallel

**When specialized agents are available, you MUST use them instead of attempting tasks yourself.**

**When performing multiple operations, send all tool calls in a single message to execute them concurrently for optimal performance.**

#### Key Principles:
- **Agent Delegation**: Always check if a specialized agent exists for your task domain
- **Complex Problems**: Delegate to domain experts
- **Multiple Agents**: Send multiple Task tool calls in a single message
- **DEFAULT TO PARALLEL**: Unless operations MUST be sequential, execute multiple tools simultaneously

#### Critical: Always Use Parallel Tool Calls

**These cases MUST use parallel tool calls:**
- Searching for different patterns (imports, usage, definitions)
- Multiple grep searches with different regex patterns
- Reading multiple files or searching different directories
- Agent delegations with multiple Task calls to different specialists

**Sequential calls ONLY when:**
You genuinely REQUIRE the output of one tool to determine the usage of the next tool.

**Performance Impact:** Parallel tool execution is 3-5x faster than sequential calls.
