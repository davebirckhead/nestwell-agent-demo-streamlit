import os
GOODWILL_MAX = float(os.getenv("GOODWILL_MAX", "50"))
class HelpdeskTool:
    def create_case(self, user_id: str, summary: str, details: dict):
        return {"id": f"C{hash(user_id+summary)%100000}", "summary": summary, "details": details}
    def issue_goodwill(self, user_id: str, amount: float):
        amt = min(amount, GOODWILL_MAX)
        return {"amount": amt, "currency": "USD"}
