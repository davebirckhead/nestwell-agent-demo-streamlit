from typing import Any, Dict, List
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_tool_schemas() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "recommend_bundle",
                "description": "Recommend a product bundle for the user's need",
                "parameters": {
                    "type": "object",
                    "properties": {"need": {"type": "string"}},
                    "required": ["need"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "price_quote",
                "description": "Create a price quote for a requested quantity",
                "parameters": {
                    "type": "object",
                    "properties": {"request": {"type": "string"}},
                    "required": ["request"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "lookup_order",
                "description": "Lookup order status",
                "parameters": {
                    "type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "kb_answer",
                "description": "Answer a knowledge base question",
                "parameters": {
                    "type": "object",
                    "properties": {"question": {"type": "string"}},
                    "required": ["question"],
                },
            },
        },
    ]

def chat_with_tools(system_prompt: str, messages: List[Dict[str, str]]):
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role":"system","content":system_prompt}] + messages,
        tools=get_tool_schemas(),
        tool_choice="auto",
        temperature=0.3,
    )
    return resp
