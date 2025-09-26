from pathlib import Path
import json
def run():
    mem = Path(__file__).parent.parent / "memory" / "interactions.jsonl"
    total = 0; contained = 0
    if mem.exists():
        for line in open(mem):
            total += 1
            ev = json.loads(line)
            if ev.get("intent") in ("marketing_consult","sales_assist","cs_resolution"):
                contained += 1
    rate = (contained / total) if total else 0.0
    print({"sessions": total, "contained": contained, "containment_rate": round(rate,3)})
if __name__ == "__main__":
    run()
