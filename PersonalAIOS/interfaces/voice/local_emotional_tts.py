import logging
import re
import asyncio
import os

logger = logging.getLogger(__name__)

class LocalEmotionalTTS:
    """
    Local lightweight TTS wrapper (designed for Kokoro or Piper).
    Parses <emotion> tags to dynamically adjust voice profiles/pitch.
    """
    def __init__(self, output_dir="/tmp/asta_audio"):
        self.current_emotion = "neutral"
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _parse_emotion(self, text: str):
        # Find emotion tags like <anger>, <sadness>
        match = re.search(r'<(\w+)>', text)
        if match:
            emotion = match.group(1).lower()
            # Remove tag from text
            clean_text = re.sub(r'<\w+>', '', text)
            return emotion, clean_text.strip()
        return "neutral", text

    def _apply_emotion_settings(self, emotion: str):
        # Adjust TTS parameters based on parsed emotion
        settings = {
            "anger": {"speed": 1.2, "pitch": 1.1},
            "sadness": {"speed": 0.8, "pitch": 0.9},
            "excitement": {"speed": 1.3, "pitch": 1.2},
            "tiredness": {"speed": 0.7, "pitch": 0.8},
            "neutral": {"speed": 1.0, "pitch": 1.0}
        }
        self.current_emotion = emotion
        return settings.get(emotion, settings["neutral"])

    async def speak(self, text: str) -> str:
        """
        Takes LLM text, extracts emotion, configures local TTS,
        generates the audio file, and returns the path.
        """
        emotion, clean_text = self._parse_emotion(text)
        params = self._apply_emotion_settings(emotion)

        logger.info(f"Synthesizing '{clean_text[:30]}...' with emotion '{emotion}' (Speed: {params['speed']}, Pitch: {params['pitch']})")

        # In a real setup, we would call the Piper/Kokoro binary here:
        # e.g., subprocess.run(['piper', '--model', model_path, '--output_file', out_path], input=clean_text.encode())

        # Simulate local TTS generation
        await asyncio.sleep(0.5)

        output_path = os.path.join(self.output_dir, "latest_response.wav")
        # Touch file to simulate creation
        with open(output_path, 'w') as f:
            f.write(f"SIMULATED AUDIO DATA for: {clean_text}")

        return output_path
