from dataclasses import dataclass
@dataclass
class A2AMessage:
    role: str
    content: str
    payload: dict | None = None

class A2ARouter:
    def route(self, msg: A2AMessage, handler):
        return handler(msg)
