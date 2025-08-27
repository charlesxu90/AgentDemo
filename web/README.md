# Agentic Demo UI

This is the web UI for a general agentic AI demo case.

Adapted from [`DeepResearcch`](https://github.com/charlesxu90/deep-research).

## Quick Start

### Prerequisites

- [`DeepResearcch`](https://github.com/charlesxu90/deep-research)
- Node.js (v22.14.0+)
- pnpm (v10.6.2+) as package manager

### Configuration

Set up your own LLM configuration by creating and modifying the .env file.

```bash
cp .env.example .env
```

## Install
```bash
cd web
# Install the dependencies
pnpm install
```

## Run in Development Mode

> [!NOTE]
> Ensure the Python API service is running before starting the web UI.

Start the web UI development server:

```bash
cd web
pnpm dev
```

By default, the web UI will be available at `http://localhost:3000`.

You can set the `NEXT_PUBLIC_API_URL` environment variable if you're using a different host or location.

```ini
# .env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Core Workflow Explanation:
1. Frontend Layer (React/TypeScript)
- Entry: User starts at landing page, navigates to chat interface
- Main Components: Chat interface with dual-pane layout (messages + research display)
- State Management: Zustand stores manage chat state, settings, and user preferences
- API Integration: Real-time streaming via Server-Sent Events to backend

2. Backend API Layer (FastAPI)
- Entry Point: app.py handles HTTP requests with OpenAPI documentation
- Request Processing: Validates requests, manages authentication, routes to workflow engine
- Streaming: Real-time response streaming back to frontend

3. Deep Research Engine (LangGraph Workflow)
- Workflow Orchestration: workflow.py manages the entire research pipeline
- Graph Execution: LangGraph state machine with nodes for planning, research, coordination, and reporting
- Agent System: Specialized AI agents (planner, researcher, coordinator, reporter) with specific LLM assignments

4. Core Research Flow:
- Planning: User query → Research plan creation → Human approval (with interrupts)
- Background Investigation: Web search and context gathering
- Research Execution: Multi-step research with tool integrations
- Coordination: Progress monitoring and plan adjustments
- Reporting: Final report generation in selected style (Academic/Popular Science)

5. Tool Ecosystem:
- Web Search: Tavily API integration for real-time information
- Content Processing: Jina API for article extraction and processing
- Code Execution: Python REPL for data analysis and computation
- RAG System: Multiple providers (VikingDB, RAGFlow) for document retrieval

6. Configuration & Extensibility:
- Modular Configuration: YAML-based settings with environment variable overrides
- MCP Integration: Model Context Protocol for external tool integration
- Checkpoint System: MongoDB/PostgreSQL for conversation memory and state persistence
- This architecture provides a robust, scalable research assistant with real-time streaming, human-in-the-loop workflows, and extensive tool integration capabilities.


## License

This project is open source and available under the [MIT License](../LICENSE).
