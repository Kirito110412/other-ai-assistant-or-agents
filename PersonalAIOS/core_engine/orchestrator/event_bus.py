import asyncio
from typing import Callable, Dict, List

class EventBus:
    """
    The High-Speed Internal Nervous System.
    Pub/Sub message broker allowing isolated modules to communicate instantly.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    async def publish(self, topic: str, payload: dict):
        if topic in self.subscribers:
            tasks = [callback(payload) for callback in self.subscribers[topic]]
            await asyncio.gather(*tasks)

# Global singleton instance of the nervous system
nervous_system = EventBus()
