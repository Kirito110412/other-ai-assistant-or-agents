import asyncio

class ScreenListener:
    """
    Continuous, toggleable background context gatherer for the screen.
    """
    def __init__(self):
        self.is_active = False

    def toggle(self, state: bool):
        self.is_active = state

    async def listen_loop(self):
        """
        When active, constantly caches screenshots to allow "zero-context" commands
        like "fix this error on my screen".
        """
        while self.is_active:
            # Capture screenshot to short-term memory buffer
            await asyncio.sleep(2)
