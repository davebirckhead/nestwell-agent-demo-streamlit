# NestWell Living — Agentic GTM Demo

An AI-powered customer service and sales automation demo inspired by direct-to-consumer furniture companies like Casper. This system demonstrates autonomous handling of customer interactions across marketing, sales, and support channels using FastAPI and LangChain/LangGraph.

## Features

### Autonomous Customer Interaction Flows
- **Marketing**: Product bundle recommendations with automatic lead creation
- **Sales**: Price quotes with opportunity creation and meeting scheduling
- **Customer Service**: Order status lookup with autonomous issue resolution and goodwill credits
- **Knowledge Base**: Fallback support using RAG-based question answering

### Observability & Analytics
- Arize Phoenix integration for request tracing
- Interaction logging for evaluation and metrics
- Containment rate analysis (autonomous vs human handoff)

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your OpenAI API key
# OPENAI_API_KEY=sk-...
```

### Running the Server
```bash
# Start the FastAPI server
uvicorn src.server.app:app --host 0.0.0.0 --port 8000 --reload

# Health check
curl http://localhost:8000/health
```

### Testing the API
```bash
# Marketing flow - bundle recommendation
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user", "message": "I need lounge furniture recommendations", "channel": "web"}'

# Sales flow - price quote
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user", "message": "What is the price for 10 units?", "channel": "web"}'

# Customer service flow - order inquiry
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_user", "message": "My order is delayed", "channel": "web"}'
```

## Demo Scripts

Run these scripts to see the different interaction flows:

```bash
# Marketing demonstration
python scripts/demo_flow_marketing.py

# Sales demonstration
python scripts/demo_flow_sales.py

# Customer service demonstration
python scripts/demo_flow_cs.py
```

## Project Structure

```
├── src/
│   ├── server/          # FastAPI application
│   ├── agents/          # Orchestration and planning logic
│   ├── tools/           # Business logic tools (CRM, Catalog, etc.)
│   ├── memory/          # Interaction storage
│   ├── observability/   # Tracing and monitoring
│   └── evals/           # Evaluation metrics
├── demo_data/
│   ├── catalog/         # Product catalog JSON
│   └── kb/              # Knowledge base markdown files
└── scripts/             # Demo and seeding scripts
```

## Architecture

The system uses **intent-based routing** to classify incoming messages and route them to appropriate handlers:

1. **Intent Classification**: Keywords trigger specific workflows
2. **Tool Execution**: Specialized tools handle business logic
3. **Response Generation**: Structured responses with outcome tags
4. **Interaction Logging**: All interactions stored for analysis

### Alternative Implementations
- `orchestrator.py`: Simple keyword-based routing
- `planner_graph.py`: LangGraph state machine approach
- `llm_toolcaller.py`: Direct LLM function calling

## Evaluation

```bash
# Run containment analysis
python src/evals/run.py
```

This analyzes what percentage of customer interactions are resolved autonomously without requiring human handoff.

## Configuration

Key environment variables:
- `OPENAI_API_KEY`: Required for LLM operations
- `PHOENIX_COLLECTOR_ENDPOINT`: Optional tracing endpoint
- `ALLOW_GOODWILL_CREDITS`: Enable/disable autonomous credit issuance
- `GOODWILL_MAX`: Maximum credit amount

## Development

The system is designed for easy extension:
- Add new tools in `src/tools/`
- Extend intent classification in orchestrator
- Add new demo data in `demo_data/`
- Configure tracing via Phoenix integration

This demo showcases how AI agents can handle complex customer service workflows with high autonomy while maintaining appropriate escalation paths.