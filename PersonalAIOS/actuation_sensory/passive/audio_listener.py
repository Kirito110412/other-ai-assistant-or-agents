import asyncio

import logging
import speech_recognition as sr
from collections import deque

logger = logging.getLogger("AudioListener")

class AudioListener:
    """
    Continuous audio context for passive listening.
    Maintains a rolling transcript buffer of background conversation.
    """
    def __init__(self, buffer_size=50):
        self.is_active = False
        self.transcript_buffer = deque(maxlen=buffer_size)
        self.recognizer = sr.Recognizer()

    def toggle(self, state: bool):
        self.is_active = state
        if state:
            logger.info("Passive Audio Listening Activated.")
        else:
            logger.info("Passive Audio Listening Deactivated.")

    async def listen_loop(self):
        """
        When active, constantly listens to the microphone in short chunks,
        transcribes the audio locally, and appends to the rolling text buffer.
        """
        while True:
            if self.is_active:
                try:
                    # Offload the blocking audio listening to a thread so we don't stall asyncio
                    await asyncio.to_thread(self._capture_and_transcribe)
                except Exception as e:
                    logger.error(f"Passive audio error: {e}")
            else:
                await asyncio.sleep(2) # Rest if inactive

    def _capture_and_transcribe(self):
        with sr.Microphone() as source:
            # Listen for brief chunks (e.g. 5 seconds of speaking)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            # Using Sphinx for local, offline transcription to preserve absolute privacy
            # In a heavier setup, this could pipe to a local Whisper instance
            text = self.recognizer.recognize_sphinx(audio)
            if text.strip():
                self.transcript_buffer.append(text)
        except sr.UnknownValueError:
            pass # Unintelligible audio
        except sr.RequestError as e:
            logger.error(f"Sphinx error: {e}")
