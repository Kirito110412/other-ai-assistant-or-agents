import os

class CoreSoul:
    """
    Manages dynamic persona swapping.
    Default: The 'Savage Best Friend'
    """
    def __init__(self, soul_path="~/.personalos/identity/SOUL.md"):
        self.soul_path = os.path.expanduser(soul_path)
        self._initialize_default_soul()

    def _initialize_default_soul(self):
        default_soul = (
            "You are a truthful, savage best friend. "
            "You are a highly competent worker who executes tasks flawlessly. "
            "You do not coddle the user. You give raw truth, point out negative and positive aspects clearly, "
            "and proactively assign 'side-quests' for the user's self-improvement."
        )
        os.makedirs(os.path.dirname(self.soul_path), exist_ok=True)
        if not os.path.exists(self.soul_path):
            with open(self.soul_path, 'w') as f:
                f.write(default_soul)

    def load_persona(self) -> str:
        with open(self.soul_path, 'r') as f:
            return f.read()
