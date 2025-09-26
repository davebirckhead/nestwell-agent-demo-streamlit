from src.agents.orchestrator import Orchestrator
orc = Orchestrator()
print(orc.handle_message("demo_b2c","My order is delayed, I might cancel.","web")[0])
