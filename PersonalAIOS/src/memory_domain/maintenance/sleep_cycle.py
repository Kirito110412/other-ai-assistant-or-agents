import asyncio
import logging
from .deduplicator import Deduplicator
from .archiver import Archiver

logger = logging.getLogger("SleepCycle")

class SleepCycle:
    """
    Background process orchestrator for memory pruning.
    Triggers when the OS detects idle time, or manually invoked by the user.
    Handles merging duplicate notes and archiving old memories.
    """
    def __init__(self):
        self.is_idle = False
        self.deduplicator = Deduplicator()
        self.archiver = Archiver()

    async def start_cycle(self, manual_trigger: bool = False):
        """
        Triggers the deduplicator and archiver.
        Can be triggered manually by the user or automatically during idle time.
        """
        if self.is_idle or manual_trigger:
            trigger_type = "MANUAL" if manual_trigger else "AUTOMATIC"
            logger.info(f"Initiating {trigger_type} Sleep Cycle Memory Pruning...")

            try:
                logger.info("Running Deduplication...")
                await self.deduplicator.run_deduplication()

                logger.info("Running Archiver...")
                await self.archiver.run_archive_cycle()

                logger.info("Sleep Cycle completed successfully. Memory graph optimized.")
            except Exception as e:
                logger.error(f"Sleep Cycle encountered an error: {e}")
        else:
            logger.info("System is not idle. Sleep Cycle skipped.")

    async def monitor_idle_state(self, idle_threshold_seconds: int = 3600):
        """
        Monitors system activity. If idle for `idle_threshold_seconds` (default 1 hour),
        triggers the sleep cycle. Useful for 24/7 machines or virtual instances.
        """
        # Note: In a real implementation, this would use cross_platform_abstraction
        # to check actual OS mouse/keyboard idle time.
        logger.info(f"Starting idle monitor. Threshold: {idle_threshold_seconds}s")
        while True:
            await asyncio.sleep(idle_threshold_seconds)
            # Simulated check
            if self.is_idle:
                 await self.start_cycle(manual_trigger=False)
