import logging
from typing import Any
from src.agent.capability import MatchingCapability
from src.agent.base import BotAgent
from src.agent.io_interface import (
    SynchronousTTT,
    SharedValue,
)
from src.system_conf import (
    SLEEP_SOUND,
    SLEEP_PROMPT,
)
from src.utils.sound_player import play_sound
from src.main import AgentWorker
import os
import json

# import asyncio


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
        msg: str,
        agent: BotAgent,
        text_respond: SynchronousTTT,
        speak_respond: None,
        audio: str,
        worker: AgentWorker,
        meta: dict[str, Any],
        interrupt_str: SharedValue,
    ):
        if worker.bot_awake_event.is_set():
            logging.info("Going to sleep mode")
            worker.bot_is_speaking_event.clear()
            worker.bot_awake_event.clear()
            worker.user_is_speaking_event.clear()
            worker.user_is_finished_speak_event.set()
            play_sound(SLEEP_SOUND)

            return SLEEP_PROMPT
