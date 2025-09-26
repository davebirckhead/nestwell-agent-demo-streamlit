import json
from typing import Tuple, List
from src.tools.catalog import CatalogTool
from src.tools.orders import OrderTool
from src.tools.crm import CRMTool
from src.tools.helpdesk import HelpdeskTool
from src.tools.kb import KBTool
from src.tools.calendar import CalendarTool
from src.memory.store import MemoryStore
try:
    from src.observability.phoenix_tracing import traced
except ImportError:
    from src.observability.phoenix_tracing_mock import traced

class Orchestrator:
    def __init__(self):
        self.catalog = CatalogTool()
        self.order = OrderTool()
        self.crm = CRMTool()
        self.helpdesk = HelpdeskTool()
        self.kb = KBTool()
        self.calendar = CalendarTool()
        self.memory = MemoryStore()

    def handle_message(self, user_id: str, message: str, channel: str = "web") -> Tuple[str, List[str], str]:
        tags: List[str] = []
        with traced("orchestrator", {"user_id": user_id, "message": message}) as span:
            m = message.lower()
            if "lounge" in m or "recommend" in m or "bundle" in m:
                items = self.catalog.recommend_bundle(m)
                lead_id = self.crm.create_lead(user_id, context={"message": message, "bundle": items})
                self.memory.add_interaction(user_id, {"intent": "marketing_consult", "bundle": items, "lead_id": lead_id})
                tags += ["high_intent_engagement", "lead_created"]
                reply = f"Bundle rec: {', '.join([i['name'] for i in items])}. Created Lead {lead_id}. Schedule a call?"
                return reply, tags, span.trace_id
            if "price" in m or "quote" in m or "units" in m:
                quote = self.catalog.price_quote(message)
                evt = self.crm.create_opportunity(user_id, quote)
                meeting = self.calendar.book_meeting(user_id, duration_min=30)
                self.memory.add_interaction(user_id, {"intent": "sales_assist", "quote": quote, "meeting": meeting})
                tags += ["opportunity_created", "meeting_booked"]
                reply = f"Quote ready: {quote['summary']}. Booked 30 min: {meeting['when']} ({meeting['link']})."
                return reply, tags, span.trace_id
            if "order" in m or "delayed" in m or "cancel" in m or "return" in m:
                status = self.order.lookup(message)
                if status.get("delayed"):
                    credit = self.helpdesk.issue_goodwill(user_id, amount=20)
                    case = self.helpdesk.create_case(user_id, summary=f"Delay on {status['order_id']}", details=status)
                    self.memory.add_interaction(user_id, {"intent": "cs_resolution", "order": status, "credit": credit, "case": case})
                    tags += ["resolved_autonomously", "goodwill_credit", "case_with_context"]
                    reply = f"Order {status['order_id']} delayed; expedited + ${credit['amount']} credit. Case {case['id']} opened."
                    return reply, tags, span.trace_id
                else:
                    reply = f"Order {status.get('order_id','N/A')} on track. Anything else?"
                    return reply, tags, span.trace_id
            answer = self.kb.answer(message)
            self.memory.add_interaction(user_id, {"intent": "kb_answer", "q": message, "a": answer})
            tags += ["kb_response"]
            return answer, tags, span.trace_id
