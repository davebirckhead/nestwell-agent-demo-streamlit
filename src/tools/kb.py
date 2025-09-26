import os, json, faiss, numpy as np
KB_DIR = os.path.join(os.path.dirname(__file__), "../../demo_data/kb")
INDEX_FILE = os.path.join(KB_DIR, "kb.index")
TXT_FILE = os.path.join(KB_DIR, "kb.jsonl")
def embed(texts):
    vecs = []
    for t in texts:
        h = abs(hash(t)) % 10**8
        np.random.seed(h)
        vecs.append(np.random.rand(384).astype("float32"))
    return np.vstack(vecs)
class KBTool:
    def __init__(self):
        self.texts = []
        self.meta = []
        if os.path.exists(TXT_FILE) and os.path.exists(INDEX_FILE):
            self._load()
        else:
            self._seed()
    def _seed(self):
        docs = [
            {"text":"Return policy: free returns within 30 days; use prepaid label provided by the agent.", "source":"policy.md"},
            {"text":"Sizing guide: lounge sofas seat 3 adults; premium fabric is stain resistant.", "source":"sizing.md"},
            {"text":"Shipping: standard 3-5 business days; delays may occur during holidays.", "source":"shipping.md"},
            {"text":"Warranty: 2-year structural warranty; 1-year upholstery defects.", "source":"warranty.md"},
        ]
        self.texts = [d["text"] for d in docs]
        self.meta = [d["source"] for d in docs]
        vecs = embed(self.texts)
        index = faiss.IndexFlatIP(vecs.shape[1])
        index.add(vecs)
        faiss.write_index(index, INDEX_FILE)
        with open(TXT_FILE, "w") as f:
            for d in docs:
                f.write(json.dumps(d) + "\n")
    def _load(self):
        self.texts = []
        self.meta = []
        with open(TXT_FILE) as f:
            for line in f:
                d = json.loads(line)
                self.texts.append(d["text"]); self.meta.append(d["source"])
        self.index = faiss.read_index(INDEX_FILE)
    def answer(self, q: str) -> str:
        if not hasattr(self, "index"):
            self.index = faiss.read_index(INDEX_FILE)
        vec = embed([q])
        D,I = self.index.search(vec, 1)
        return f"{self.texts[I[0][0]]} (source: {self.meta[I[0][0]]})"
