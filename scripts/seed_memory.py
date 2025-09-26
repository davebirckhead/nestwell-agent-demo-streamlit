from src.memory.store import MemoryStore
if __name__ == "__main__":
    m = MemoryStore()
    m.add_interaction("demo_user",{"intent":"seed"})
    print("Memory seeded.")
