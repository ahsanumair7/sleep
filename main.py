import json
import os
from src.agent.capability import MatchingCapability
from src.main import AgentWorker
# Prompts
SLEEP_PROMPT = "Going in Sleep Mode!"

class SleepCapability(MatchingCapability):
    @classmethod
    def register_capability(cls) -> "MatchingCapability":
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        ) as file:
            data = json.load(file)
        return cls(
            unique_name=data["unique_name"],
            matching_hotwords=data["matching_hotwords"],
        )

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
