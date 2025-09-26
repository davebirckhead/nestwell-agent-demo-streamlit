import os, json
from typing import Callable, Dict, List, Tuple, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _schemas_for_domain(domain: str) -> List[Dict[str, Any]]:
    """Tool schemas exposed to the LLM for a given domain."""
    common = [
        { "type": "function", "function": {
            "name":"kb_answer", "description":"Answer a knowledge-base question.",
            "parameters":{"type":"object","properties":{"question":{"type":"string"}}, "required":["question"]}
        }},
    ]
    marketing = [
        { "type": "function", "function": {
            "name":"recommend_bundle", "description":"Recommend a product bundle for the user's need.",
            "parameters":{"type":"object","properties":{"need":{"type":"string"}}, "required":["need"]}
        }},
        { "type": "function", "function": {
            "name":"create_lead", "description":"Create a CRM lead with context.",
            "parameters":{"type":"object","properties":{"note":{"type":"string"}}, "required":["note"]}
        }},
    ]
    sales = [
        { "type": "function", "function": {
            "name":"price_quote", "description":"Create a price quote from a free-form request.",
            "parameters":{"type":"object","properties":{"request":{"type":"string"}}, "required":["request"]}
        }},
        { "type": "function", "function": {
            "name":"create_opportunity", "description":"Create a CRM opportunity for this user/message.",
            "parameters":{"type":"object","properties":{"note":{"type":"string"}}, "required":["note"]}
        }},
        { "type": "function", "function": {
            "name":"book_meeting", "description":"Book a 30-minute meeting.",
            "parameters":{"type":"object","properties":{}}
        }},
    ]
    support = [
        { "type": "function", "function": {
            "name":"lookup_order", "description":"Lookup an order status from a user query.",
            "parameters":{"type":"object","properties":{"query":{"type":"string"}}, "required":["query"]}
        }},
        { "type": "function", "function": {
            "name":"issue_goodwill", "description":"Issue a goodwill credit (respecting policy caps).",
            "parameters":{"type":"object","properties":{"amount":{"type":"number"}}, "required":["amount"]}
        }},
        { "type": "function", "function": {
            "name":"create_case", "description":"Create a helpdesk case with a brief summary.",
            "parameters":{"type":"object","properties":{"summary":{"type":"string"}}, "required":["summary"]}
        }},
    ]
    if domain == "marketing": return marketing + common
    if domain == "sales":     return sales + common
    if domain == "support":   return support + common
    return common

def build_registry(*, user_id: str, traits: dict, tools: dict) -> Dict[str, Callable[..., Any]]:
    """Map function names to concrete tool calls, injecting user_id/traits as needed."""
    return {
        # Marketing
        "recommend_bundle": lambda need: tools["catalog"].recommend_bundle(need, traits=traits),
        "create_lead":      lambda note: tools["crm"].create_lead(user_id, {"note": note}, traits=traits),

        # Sales
        "price_quote":        lambda request: tools["catalog"].price_quote(request, traits=traits),
        "create_opportunity": lambda note: tools["crm"].create_opportunity(user_id, {"note": note}, traits=traits),
        "book_meeting":       lambda: tools["calendar"].book_meeting(user_id),

        # Support
        "lookup_order":   lambda query: tools["orders"].lookup(query),
        "issue_goodwill": lambda amount: tools["helpdesk"].issue_goodwill(user_id, float(amount), traits=traits),
        "create_case":    lambda summary: tools["helpdesk"].create_case(user_id, summary, {}),

        # KB
        "kb_answer": lambda question: tools["kb"].answer(question),
    }

SYSTEM_BASE = """You are a helpful assistant operating inside a specific business domain.
You can choose and call functions to achieve the user's goal. Prefer taking real actions over generic text.
Respond concisely. After calling tools, synthesize a human-friendly final answer."""

def llm_toolstep(
    *, domain: str, user_message: str, traits: dict, registry: Dict[str, Callable[..., Any]],
    extra_system: str = ""
) -> Tuple[str, List[Tuple[str, Any]]]:
    """
    Calls OpenAI with domain-scoped tools; executes tool calls; returns (final_text, call_log).
    call_log is [(tool_name, result), ...] for the node to derive tags / memory updates.
    """
    tools = _schemas_for_domain(domain)
    messages = [
        {"role":"system","content": SYSTEM_BASE + ("\n" + extra_system if extra_system else "")},
        {"role":"user","content": user_message}
    ]
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
    )
    msg = resp.choices[0].message
    call_log: List[Tuple[str, Any]] = []

    # Execute tool calls (single step or chain)
    if getattr(msg, "tool_calls", None):
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            if name not in registry:
                call_log.append((name, {"error":"unknown_tool"}))
                continue
            # Call tool
            result = registry[name](**{k: v for k, v in args.items()})
            call_log.append((name, result))
            # Feed tool result back to model
            messages.append({"role":"assistant", "tool_calls":[{"id": tc.id, "function":{"name":name, "arguments": tc.function.arguments}}]})
            messages.append({"role":"tool", "tool_call_id": tc.id, "content": json.dumps(result)})

        # Ask model for final user-facing answer
        final = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
            messages=messages,
            temperature=0.2,
        )
        return final.choices[0].message.content, call_log

    # No tool call; just return text
    return (msg.content or ""), call_log