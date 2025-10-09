import json
from src.agent.capability import MatchingCapability
from src.main import AgentWorker
# Prompts
SLEEP_PROMPT = "Going in Sleep Mode!"

class SleepCapability(MatchingCapability):
    #{{register capability}}

    def call(
        self,
        worker: AgentWorker,
    ):        
        if worker.bot_awake_event.is_set():
            worker.bot_is_speaking_event.clear()
            worker.bot_awake_event.clear()
            worker.user_is_speaking_event.clear()
            worker.user_is_finished_speak_event.set()
            return SLEEP_PROMPT
