import asyncio

class AudioListener:
    """
    Continuous audio context for passive listening.
    """
    def __init__(self):
        self.is_active = False

    def toggle(self, state: bool):
        self.is_active = state

    async def listen_loop(self):
        """
        When active, constantly caches audio transcriptions.
        """
        while self.is_active:
            # Transcribe audio to short-term memory buffer
            await asyncio.sleep(1)
