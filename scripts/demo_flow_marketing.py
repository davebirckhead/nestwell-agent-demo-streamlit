from src.agents.orchestrator import Orchestrator
orc = Orchestrator()
print(orc.handle_message("demo_b2b","I'm outfitting a team lounge. What bundle do you recommend?","web")[0])
