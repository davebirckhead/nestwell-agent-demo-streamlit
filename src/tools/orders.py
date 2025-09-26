import random
class OrderTool:
    def lookup(self, message: str):
        delayed = "delayed" in message.lower() or random.random() < 0.5
        return {"order_id": f"NW{random.randint(10000,99999)}", "delayed": delayed, "eta_days": 2 if not delayed else 5}
