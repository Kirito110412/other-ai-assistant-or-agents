class ShortTermMemory:
    """
    Active context and conversational window management.
    """
    def __init__(self, max_tokens=4096):
        self.context_window = []
        self.max_tokens = max_tokens

    def add_interaction(self, role: str, content: str):
        """Adds a message and prunes old context if token limit is exceeded."""
        self.context_window.append({"role": role, "content": content})
        self._enforce_limit()

    def _enforce_limit(self):
        # Logic to slide the window and push stale context to Obsidian Graph
        pass
