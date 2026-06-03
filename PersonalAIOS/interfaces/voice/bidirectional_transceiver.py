import asyncio
import logging
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system
from PersonalAIOS.core_engine.routing.hybrid_switch import hybrid_router

logger = logging.getLogger("VoiceEngine")

class BidirectionalTransceiver:
    """
    Low-latency real-time conversational module.
    Pipes STT directly to the LLM and streams TTS responses back.
    """
    def __init__(self):
        self.is_listening = False

    async def process_spoken_input(self, spoken_text: str):
        """
        Takes raw Speech-to-Text string, routes it to the Logic Engine,
        and triggers the TTS playback and UI Avatar sync.
        """
        logger.info(f"User Spoke: {spoken_text}")

        # 1. Trigger Avatar to show "Thinking" state
        await nervous_system.publish("ai_thinking", {})

        # 2. Route through Hybrid LLM (In reality, goes through SequentialSolver intent router first)
        response_text = await hybrid_router.execute_query([{"role": "user", "content": spoken_text}], complexity=0.3)

        # 3. Trigger Avatar Lip-Sync & Speaking State
        await nervous_system.publish("ai_speaking", {"audio_data": response_text})

        # 4. Execute actual TTS (Text-To-Speech)
        await self._execute_tts(response_text)

    async def _execute_tts(self, text: str):
        """
        Placeholder for local pyttsx3/ElevenLabs execution.
        """
        logger.info(f"[TTS AUDIO OUTPUT]: {text}")

        # After speaking, revert Avatar to Idle
        await asyncio.sleep(2) # Simulate speaking time
        await nervous_system.publish("ui_task_progress_update", {"progress_percent": 100})
