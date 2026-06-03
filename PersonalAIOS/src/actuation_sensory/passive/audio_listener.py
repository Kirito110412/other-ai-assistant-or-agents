import asyncio
import logging
import speech_recognition as sr
from collections import deque

logger = logging.getLogger("AudioListener")

class AudioListener:
    """
    Continuous audio context for passive listening and Wake Word detection.
    Maintains a rolling transcript buffer of background conversation.
    """
    def __init__(self, buffer_size=50, wake_word="friday"):
        self.is_active = False
        self.transcript_buffer = deque(maxlen=buffer_size)
        self.recognizer = sr.Recognizer()
        self.wake_word = wake_word.lower()

    def toggle(self, state: bool):
        self.is_active = state
        if state:
            logger.info("Passive Audio Listening Activated.")
        else:
            logger.info("Passive Audio Listening Deactivated.")

    async def listen_loop(self, on_wake_word_callback=None):
        """
        When active, constantly listens to the microphone in short chunks,
        transcribes the audio locally, and appends to the rolling text buffer.
        """
        while True:
            if self.is_active:
                try:
                    # Offload the blocking audio listening to a thread so we don't stall asyncio
                    text = await asyncio.to_thread(self._capture_and_transcribe)
                    if text:
                        self.transcript_buffer.append(text)

                        # Check for wake word
                        if self.wake_word in text.lower():
                            logger.info(f"Wake word '{self.wake_word}' detected!")
                            if on_wake_word_callback:
                                # Strip wake word and pass the rest of the command
                                command = text.lower().split(self.wake_word, 1)[1].strip()
                                await on_wake_word_callback(command)

                except Exception as e:
                    logger.error(f"Passive audio error: {e}")
            else:
                await asyncio.sleep(2) # Rest if inactive

    def _capture_and_transcribe(self) -> str:
        with sr.Microphone() as source:
            # Listen for brief chunks (e.g. 5 seconds of speaking)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                 audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                 return ""

        try:
            # Using Sphinx for local, offline transcription to preserve absolute privacy
            # In a heavier setup, this could pipe to a local Whisper instance
            text = self.recognizer.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            return "" # Unintelligible audio
        except sr.RequestError as e:
            logger.error(f"Sphinx error: {e}")
            return ""
