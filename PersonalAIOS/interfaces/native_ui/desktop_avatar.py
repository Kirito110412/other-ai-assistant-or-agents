import logging
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system

logger = logging.getLogger("DesktopAvatar")

import tkinter as tk
import threading

class HolographicAvatar:
    """
    Manages the borderless, transparent floating window overlay for the interactive character.
    Acts as the visual embodiment of the AI on the user's screen.
    """
    def __init__(self):
        self.is_visible = True
        self.current_state = "idle" # States: idle, thinking, talking, working

        # Subscribe to internal OS events to trigger physical character reactions
        nervous_system.subscribe("ai_speaking", self._handle_speaking_animation)
        nervous_system.subscribe("ai_thinking", self._handle_thinking_animation)
        nervous_system.subscribe("ui_task_progress_update", self._handle_busy_animation)

        # UI must run on the main thread, so we start it in a managed way
        self.root = None

    def start_overlay(self):
        """Initializes the transparent tkinter overlay."""
        self.root = tk.Tk()
        self.root.overrideredirect(True) # Removes window borders
        self.root.attributes('-topmost', True) # Floats above all apps

        # Make background transparent (Platform dependent)
        try:
            self.root.attributes('-transparentcolor', 'black')
        except:
            pass # Mac handles transparency differently, can use '-alpha' or 'wm_attributes'

        self.root.geometry("200x200-50+50") # Bottom right corner

        self.label = tk.Label(self.root, text="(•_•)\nIdle", fg="green", bg="black", font=("Courier", 16))
        self.label.pack(expand=True)

        # Start UI loop
        threading.Thread(target=self.root.mainloop, daemon=True).start()

    def update_avatar_state(self, face: str, text: str, color: str):
        if self.root and self.label:
            self.label.config(text=f"{face}\n{text}", fg=color)

    def toggle_visibility(self, state: bool):
        self.is_visible = state
        if self.root:
            if not state:
                self.root.withdraw()
            else:
                self.root.deiconify()

    async def _handle_speaking_animation(self, payload: dict):
        """
        Syncs the character's facial movements/lip-sync with the incoming TTS audio stream.
        """
        self.current_state = "talking"
        self.update_avatar_state("(^o^)", "Speaking...", "cyan")

    async def _handle_thinking_animation(self, payload: dict):
        self.current_state = "thinking"
        self.update_avatar_state("(o_o)", "Calculating...", "yellow")

    async def _handle_busy_animation(self, payload: dict):
        """
        If a background task is running, the character might visually appear to be working
        (e.g., typing on a holographic keyboard or floating in the corner).
        """
        self.current_state = "working"
        percent = payload.get("progress_percent", 0)
        self.update_avatar_state("(@_@)", f"Working: {percent}%", "magenta")
