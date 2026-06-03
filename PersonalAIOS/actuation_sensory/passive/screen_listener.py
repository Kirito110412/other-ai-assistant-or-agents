import asyncio

import os
import time
import logging
from collections import deque
from PersonalAIOS.actuation_sensory.vision.screen_parser import ScreenParser

logger = logging.getLogger("ScreenListener")

class ScreenListener:
    """
    Continuous, toggleable background context gatherer for the screen.
    Maintains a rolling buffer of recent visual context.
    """
    def __init__(self, buffer_size=10, save_dir="~/.personalos/memory_graph/short_term_vision"):
        self.is_active = False
        self.buffer_size = buffer_size
        self.save_dir = os.path.expanduser(save_dir)
        self.frame_buffer = deque(maxlen=self.buffer_size)
        self.vision = ScreenParser()

        os.makedirs(self.save_dir, exist_ok=True)

    def toggle(self, state: bool):
        self.is_active = state
        if state:
            logger.info("Passive Screen Listening Activated.")
        else:
            logger.info("Passive Screen Listening Deactivated.")

    async def listen_loop(self):
        """
        When active, constantly caches screenshots (e.g. every 5 seconds).
        Old screenshots are deleted to maintain a zero-bloat footprint.
        """
        while True:
            if self.is_active:
                timestamp = int(time.time())
                filepath = os.path.join(self.save_dir, f"frame_{timestamp}.png")

                try:
                    self.vision.capture_screen(save_path=filepath)
                    self.frame_buffer.append(filepath)

                    # Cleanup old files physically from disk
                    self._cleanup_old_frames()

                except Exception as e:
                    logger.error(f"Passive screen capture failed: {e}")

            await asyncio.sleep(5) # Capture interval

    def _cleanup_old_frames(self):
        """Ensures we only keep `buffer_size` files on disk."""
        active_files = set(self.frame_buffer)
        for filename in os.listdir(self.save_dir):
            filepath = os.path.join(self.save_dir, filename)
            if filepath not in active_files:
                try:
                    os.remove(filepath)
                except OSError:
                    pass
