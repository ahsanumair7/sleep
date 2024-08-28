import logging
from typing import Any
from src.agent.capability import MatchingCapability
from src.agent.base import BotAgent
from src.agent.io_interface import (
    SynchronousTTT,
    SharedValue,
)
from src.utils.sound_player import play_sound
from src.main import AgentWorker
import os
import json

# import asyncio

SLEEP_SOUND = "src/sounds/sleep.mp3"
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
        interrupt_str: SharedValue,
    ):
        msg = worker.final_user_input
        agent = worker.agent
        text_respond = worker.ttt_sync
        speak_respond = worker.tts_ios
        audio = "/tmp/the_file.wav"
        meta = {}
        
        if worker.bot_awake_event.is_set():
            logging.info("Going to sleep mode")
            worker.bot_is_speaking_event.clear()
            worker.bot_awake_event.clear()
            worker.user_is_speaking_event.clear()
            worker.user_is_finished_speak_event.set()
            play_sound(SLEEP_SOUND)

            return SLEEP_PROMPT
