import asyncio
import json
import logging
import websockets
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system

logger = logging.getLogger("AvatarWebSocket")

class AvatarWebSocketServer:
    """
    Broadcasts real-time AI states, visemes (lip-sync), and progress updates
    to a frontend animated character (e.g., Live2D, WebGL overlay).
    """
    def __init__(self, host="127.0.0.1", port=8765):
        self.host = host
        self.port = port
        self.connected_clients = set()

        # Subscribe to internal OS events
        nervous_system.subscribe("ai_speaking", self._broadcast_speaking)
        nervous_system.subscribe("ai_thinking", self._broadcast_thinking)
        nervous_system.subscribe("ui_task_progress_update", self._broadcast_progress)

    async def _register(self, websocket):
        self.connected_clients.add(websocket)
        logger.info(f"Frontend Avatar connected. Total clients: {len(self.connected_clients)}")
        try:
            await websocket.wait_closed()
        finally:
            self.connected_clients.remove(websocket)
            logger.info("Frontend Avatar disconnected.")

    async def _broadcast(self, payload: dict):
        if not self.connected_clients:
            return

        message = json.dumps(payload)
        # Gather allows broadcasting to multiple overlay windows if needed
        await asyncio.gather(
            *[client.send(message) for client in self.connected_clients],
            return_exceptions=True
        )

    async def _broadcast_speaking(self, payload: dict):
        # Audio_data would be converted to visemes here
        await self._broadcast({
            "action": "speak",
            "state": "talking",
            "audio_chunk": payload.get("audio_data", "")
        })

    async def _broadcast_thinking(self, payload: dict):
        await self._broadcast({
            "action": "animate",
            "state": "thinking"
        })

    async def _broadcast_progress(self, payload: dict):
        await self._broadcast({
            "action": "progress",
            "state": "working",
            "percent": payload.get("progress_percent", 0),
            "text": f"Working: {payload.get('progress_percent', 0)}%"
        })

    async def start_server(self):
        """Starts the WebSocket server on the event loop."""
        logger.info(f"Starting Avatar WebSocket Server on ws://{self.host}:{self.port}")
        async with websockets.serve(self._register, self.host, self.port):
            await asyncio.Future()  # run forever
