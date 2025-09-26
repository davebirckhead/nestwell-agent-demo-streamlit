# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
- Install dependencies: `pip install -r requirements.txt`
- Run the FastAPI server: `uvicorn src.server.app:app --host 0.0.0.0 --port 8000 --reload`
- Health check endpoint available at `http://localhost:8000/health`

### Demo Scripts
- Marketing demo: `python scripts/demo_flow_marketing.py`
- Sales demo: `python scripts/demo_flow_sales.py`
- Customer service demo: `python scripts/demo_flow_cs.py`
- Seed knowledge base: `python scripts/seed_kb.py`
- Seed memory store: `python scripts/seed_memory.py`

### Evaluation
- Run containment metrics: `python src/evals/run.py`
- Evaluates what percentage of interactions are handled autonomously vs requiring human handoff

## Architecture Overview

### Core Components
- **FastAPI Server** (`src/server/app.py`): Single `/chat` endpoint that processes user messages
- **Orchestrator** (`src/agents/orchestrator.py`): Main business logic router that classifies intents and executes appropriate flows
- **LangGraph Planner** (`src/agents/planner_graph.py`): Alternative implementation using LangGraph state machines for workflow orchestration

### Agent Framework
The system uses an intent-based routing approach with four main pathways:
1. **Marketing**: Bundle recommendations → Lead creation (`lounge`, `recommend`, `bundle` keywords)
2. **Sales**: Price quotes → Opportunity creation + meeting booking (`price`, `quote`, `units` keywords)
3. **Customer Service**: Order lookup → Goodwill credits + case creation (`order`, `delayed`, `cancel` keywords)
4. **Knowledge Base**: Fallback for general questions using RAG

### Tools Layer (`src/tools/`)
- **CatalogTool**: Product recommendations and pricing quotes from `demo_data/catalog/catalog.json`
- **CRMTool**: Lead and opportunity creation with mock IDs
- **OrderTool**: Order status lookup and tracking
- **HelpdeskTool**: Case creation and goodwill credit issuance
- **CalendarTool**: Meeting scheduling with mock calendar slots
- **KBTool**: Knowledge base search using FAISS vector store

### Data Layer
- **MemoryStore** (`src/memory/store.py`): Logs interactions to `interactions.jsonl` for evaluation
- **Demo Data** (`demo_data/`): Static JSON catalog and markdown knowledge base files
- **Observability** (`src/observability/phoenix_tracing.py`): Arize Phoenix integration for tracing

### Configuration
- Environment variables in `.env.example`: OpenAI API key, Phoenix tracing, server settings
- Goodwill credit limits configurable via `ALLOW_GOODWILL_CREDITS` and `GOODWILL_MAX`

### Alternative Implementations
- `src/agents/llm_toolcaller.py`: Direct LLM tool calling approach
- `src/agents/a2a.py`: Agent-to-agent communication patterns
- `src/agents/openai_tools.py`: OpenAI function calling utilities

The system is designed as a demo of agentic GTM (Go-To-Market) automation, simulating a furniture company's customer interaction flows with autonomous resolution capabilities.