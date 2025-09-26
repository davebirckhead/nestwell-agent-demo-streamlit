import json, os, random
DATA = os.path.join(os.path.dirname(__file__), "../../demo_data/catalog/catalog.json")

class CatalogTool:
    def __init__(self):
        with open(DATA) as f:
            self.catalog = json.load(f)

    def recommend_bundle(self, message: str):
        items = []
        for k in ["chair","desk","sofa","pillow","lamp"]:
            candidates = [p for p in self.catalog if k in p["tags"]]
            if candidates:
                items.append(random.choice(candidates))
        return items[:3]

    def price_quote(self, message: str):
        qty = 10 if "10" in message else 5
        pick = random.choice(self.catalog)
        unit = pick["price"]
        total = unit * qty * (0.9 if qty >= 10 else 1.0)
        return {"items":[{"sku": pick["sku"], "qty": qty, "unit": unit}], "total": total, "summary": f"{qty}x {pick['name']} @ ${unit} → total ${total:,.2f}"}
