import asyncio
import logging
from typing import Callable, Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

class EventBus:
    """
    The High-Speed Internal Nervous System.
    A robust Pub/Sub message broker allowing isolated modules to communicate instantly.
    Supports asynchronous event handling for multi-agent concurrency.
    """
    def __init__(self):
        # Maps a topic string to a list of async callbacks
        self.subscribers: Dict[str, List[Callable]] = {}
        # Stores events if we need replayability or audit logs
        self.event_history: List[Dict[str, Any]] = []

    def subscribe(self, topic: str, callback: Callable):
        """
        Registers an isolated module to listen for a specific event topic.
        """
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.debug(f"Subscribed to topic: {topic}")

    def unsubscribe(self, topic: str, callback: Callable):
        """
        Removes a subscriber, useful when sub-agents are spun down.
        """
        if topic in self.subscribers and callback in self.subscribers[topic]:
            self.subscribers[topic].remove(callback)

    async def publish(self, topic: str, payload: dict):
        """
        Fires an event to all subscribed modules simultaneously without blocking.
        """
        event = {"topic": topic, "payload": payload}
        self.event_history.append(event)

        if topic in self.subscribers:
            logger.info(f"Publishing event [{topic}] to {len(self.subscribers[topic])} subscribers.")

            # Create a list of coroutines to run concurrently
            tasks = []
            for callback in self.subscribers[topic]:
                try:
                    tasks.append(asyncio.create_task(callback(payload)))
                except Exception as e:
                    logger.error(f"Failed to dispatch to callback on topic {topic}: {e}")

            if tasks:
                # True fire-and-forget: spawn a background task to await the gather
                # so the publisher is never blocked by slow subscribers.
                asyncio.create_task(asyncio.gather(*tasks, return_exceptions=True))

# Global singleton instance of the nervous system
nervous_system = EventBus()
