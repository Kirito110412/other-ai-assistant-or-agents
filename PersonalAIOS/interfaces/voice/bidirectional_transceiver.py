from .webrtc_barge_in import WebRTCBargeIn
import asyncio

class BidirectionalTransceiver:
    """
    Low-latency real-time conversational module with interruption handling.
    """
    def __init__(self):
        self.webrtc = WebRTCBargeIn()

    def start_conversation(self):
        """
        Connects local STT (Speech-to-Text) to the Logic Engine,
        and pipes the output to a local TTS (Text-to-Speech) engine.
        Handles wake words and mid-sentence interruptions.
        """
        pass
