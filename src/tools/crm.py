import random, string
class CRMTool:
    def create_lead(self, user_id: str, context: dict):
        return "L" + "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
    def create_opportunity(self, user_id: str, quote: dict):
        return {"id": "O" + "".join(random.choices("0123456789", k=7)), "amount": quote["total"]}
