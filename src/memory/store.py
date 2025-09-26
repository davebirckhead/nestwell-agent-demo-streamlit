import json
from pathlib import Path
MEM_PATH = Path(__file__).parent / "interactions.jsonl"
class MemoryStore:
    def add_interaction(self, user_id: str, event: dict):
        rec = {"user_id": user_id, **event}
        with open(MEM_PATH, "a") as f:
            f.write(json.dumps(rec) + "\n")
