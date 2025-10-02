# NestWell Living — Agentic GTM Demo

An AI-powered customer service and sales automation demo inspired by direct-to-consumer furniture companies like Room & Board and Casper. This system demonstrates autonomous handling of customer interactions across marketing, sales, and support channels using FastAPI, LangChain/LangGraph, and a Streamlit web interface.

🌐 **[Try the Live Demo](https://github.com/davebirckhead/nestwell-agent-demo-streamlit)**

## Features

### Autonomous Customer Interaction Flows
- **Marketing**: Product bundle recommendations with automatic lead creation and budget-aware suggestions
- **Sales**: Price quotes with opportunity creation and meeting scheduling
- **Customer Service**: Order status lookup with autonomous issue resolution, goodwill credits, and risk detection
- **Knowledge Base**: Fallback support using RAG-based question answering

### Advanced Features
- **Smart Intent Classification**: Prioritizes sales quotes over product mentions for accurate routing
- **Budget-Aware Recommendations**: References user budget constraints in product suggestions
- **Focus Space Products**: Specialized catalog for quiet pods, privacy screens, and acoustic solutions
- **Memory Persistence**: Tracks user traits, preferences, and interaction history across sessions
- **Risk Detection**: Automatically flags at-risk customers based on cancellation mentions

### User Interfaces
- **Streamlit Web App**: Interactive interface with collapsible profile sections and real-time memory updates
- **FastAPI Server**: RESTful API for programmatic access
- **Demo Scripts**: Command-line demonstrations of different workflows

### Observability & Analytics
- Arize Phoenix integration for request tracing (with mock fallback)
- Interaction logging for evaluation and metrics
- Containment rate analysis (autonomous vs human handoff)
- Real-time memory state visualization

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=your_api_key_here" > .env
echo "USE_LLM_TOOLCALLING=true" >> .env
```

### Running the Applications

#### Option 1: Streamlit Web Interface (Recommended)
```bash
# Start the Streamlit app
streamlit run streamlit_app.py

# Open http://localhost:8501 in your browser
```

#### Option 2: FastAPI Server
```bash
# Start the FastAPI server
uvicorn src.server.app:app --host 0.0.0.0 --port 8000 --reload

# Health check
curl http://localhost:8000/health
```

### Testing the Streamlit Interface

Try these example messages in the web interface:

**Marketing (Product Recommendations)**
- "I'm outfitting a team lounge. Our budget is about $1,500 per room. What do you recommend?"
- "We also want quiet pods for the focus room."

**Sales (Pricing & Quotes)**
- "What's the price for 10 ergonomic chairs?"
- "We need a quote for 10 units by end of quarter."

**Customer Service**
- "My order is delayed, I might cancel."
- "I need help with my recent furniture delivery."

### Testing the API
```bash
# Marketing flow - bundle recommendation with budget
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_b2b", "message": "I need lounge furniture recommendations with a $1500 budget", "channel": "web"}'

# Sales flow - price quote
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_b2b", "message": "What is the price for 10 units?", "channel": "web"}'

# Customer service flow - order inquiry with risk
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "demo_b2b", "message": "My order is delayed and I might cancel", "channel": "web"}'
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
├── streamlit_app.py     # Main Streamlit web interface
├── src/
│   ├── server/          # FastAPI application
│   ├── agents/          # Orchestration and planning logic
│   │   ├── planner_graph.py    # LangGraph state machine with improved intent classification
│   │   └── llm_toolcaller.py   # Enhanced LLM function calling with budget awareness
│   ├── tools/           # Business logic tools (CRM, Catalog, etc.)
│   │   └── catalog.py           # Budget-aware product recommendations
│   ├── memory/          # Interaction and profile storage
│   │   ├── store.py             # Memory persistence with profile management
│   │   └── profiles.json        # User traits and interaction history
│   ├── observability/   # Tracing and monitoring
│   └── evals/           # Evaluation metrics
├── demo_data/
│   ├── catalog/         # Product catalog with focus space products
│   │   └── catalog.json         # Enhanced catalog with quiet pods and privacy solutions
│   └── kb/              # Knowledge base markdown files
└── scripts/             # Demo and seeding scripts
```

## Architecture

The system uses **smart intent-based routing** to classify incoming messages and route them to appropriate handlers:

1. **Enhanced Intent Classification**:
   - Prioritizes sales keywords (price, quote) over marketing keywords (recommend)
   - Distinguishes between "What's the price?" (sales) vs "What do you recommend?" (marketing)
   - Handles budget context appropriately

2. **Budget-Aware Tool Execution**:
   - Product recommendations consider user budget constraints from profile memory
   - LLM prompts explicitly reference budget amounts in responses
   - Focus space products filtered by price and preference tags

3. **Memory Persistence**:
   - User traits and preferences stored across sessions
   - Interaction history tracks tool usage and outcomes
   - Risk detection flags at-risk customers for churn prevention

4. **Response Generation**: Structured responses with outcome tags and memory updates

5. **Real-time UI Updates**: Streamlit interface reflects memory changes immediately

### Implementation Options
- **`planner_graph.py`**: LangGraph state machine with enhanced intent classification
- **`llm_toolcaller.py`**: Direct LLM function calling with budget-aware prompts
- **`orchestrator.py`**: Simple keyword-based routing (legacy)

## Evaluation

```bash
# Run containment analysis
python src/evals/run.py
```

This analyzes what percentage of customer interactions are resolved autonomously without requiring human handoff.

## Configuration

Key environment variables:
- `OPENAI_API_KEY`: Required for LLM operations
- `USE_LLM_TOOLCALLING`: Enable enhanced LLM function calling (recommended: `true`)
- `OPENAI_MODEL`: OpenAI model to use (default: `gpt-4o-mini`)
- `PHOENIX_COLLECTOR_ENDPOINT`: Optional tracing endpoint
- `ALLOW_GOODWILL_CREDITS`: Enable/disable autonomous credit issuance
- `GOODWILL_MAX`: Maximum credit amount

### Streamlit Configuration
- Profiles are managed through the web interface
- Memory state persists in `src/memory/profiles.json`
- User personas: B2C (Jamie) and B2B (Alex) with different traits

## Development

The system is designed for easy extension:
- Add new tools in `src/tools/`
- Extend intent classification in `planner_graph.py`
- Add new products to `demo_data/catalog/catalog.json`
- Customize UI styling in `streamlit_app.py`
- Configure tracing via Phoenix integration

### Recent Improvements
- **Intent Classification Fix**: Prioritizes pricing requests over product mentions
- **Budget Awareness**: LLM prompts explicitly reference budget constraints
- **Focus Space Catalog**: Added quiet pods, privacy screens, acoustic panels
- **Memory Management**: Collapsible profile sections with clear functionality
- **Risk Detection**: Automatic flagging of at-risk customers
- **Lead Creation Safety Net**: Ensures CRM leads are always created for marketing requests

## Troubleshooting

**Issue**: "We also want quiet pods for the focus room" not considering budget
- **Solution**: Enhanced LLM prompts now explicitly reference budget from user profile

**Issue**: Quote requests routing to marketing instead of sales
- **Solution**: Improved intent classification prioritizes sales keywords over product mentions

**Issue**: Profile memory not updating in UI
- **Solution**: Added real-time refresh and collapsible sections for better UX

---

This demo showcases how AI agents can handle complex customer service workflows with high autonomy, budget awareness, and memory persistence while maintaining appropriate escalation paths and risk detection capabilities.