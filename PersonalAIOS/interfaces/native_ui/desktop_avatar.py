import logging
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system

logger = logging.getLogger("DesktopAvatar")

class HolographicAvatar:
    """
    Manages the borderless, transparent floating window overlay for the interactive character.
    Acts as the visual embodiment of the AI on the user's screen.
    """
    def __init__(self):
        self.is_visible = True
        self.current_state = "idle" # States: idle, thinking, talking, walking, hacking

        # Subscribe to internal OS events to trigger physical character reactions
        nervous_system.subscribe("ai_speaking", self._handle_speaking_animation)
        nervous_system.subscribe("ai_thinking", self._handle_thinking_animation)
        nervous_system.subscribe("massive_task_started", self._handle_busy_animation)

    def toggle_visibility(self, state: bool):
        self.is_visible = state
        if not state:
            logger.info("Avatar overlay hidden.")
        else:
            logger.info("Avatar overlay restored to screen.")

    async def _handle_speaking_animation(self, payload: dict):
        """
        Syncs the character's facial movements/lip-sync with the incoming TTS audio stream.
        """
        audio_stream = payload.get("audio_data")
        self.current_state = "talking"
        # Trigger UI thread to render speaking animation

    async def _handle_thinking_animation(self, payload: dict):
        self.current_state = "thinking"
        # Trigger UI thread to render thinking/calculating animation

    async def _handle_busy_animation(self, payload: dict):
        """
        If a background task is running, the character might visually appear to be working
        (e.g., typing on a holographic keyboard or floating in the corner).
        """
        self.current_state = "working"
