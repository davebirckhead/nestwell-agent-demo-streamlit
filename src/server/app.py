from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.orchestrator import Orchestrator
try:
    from src.observability.phoenix_tracing import traced
except ImportError:
    from src.observability.phoenix_tracing_mock import traced

app = FastAPI(title="NestWell Agentic GTM Demo")
orc = Orchestrator()

class ChatRequest(BaseModel):
    channel: str = "web"
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    trace_id: str
    outcome_tags: list[str] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    with traced("chat_session", attributes={"channel": req.channel, "user_id": req.user_id}) as span:
        reply, tags, trace_id = orc.handle_message(req.user_id, req.message, channel=req.channel)
        return ChatResponse(reply=reply, outcome_tags=tags, trace_id=trace_id)
