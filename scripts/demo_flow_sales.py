from src.agents.orchestrator import Orchestrator
orc = Orchestrator()
print(orc.handle_message("demo_b2b","We need a quote for 10 units by end of quarter. What's the price?","web")[0])
