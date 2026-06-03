import json
import os

class PreferencesDB:
    """
    Stores user constraints, habits, and preferences.
    """
    def __init__(self, db_path="~/.personalos/identity/USER.json"):
        self.db_path = os.path.expanduser(db_path)
        self.preferences = self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def save_preference(self, key: str, value: str):
        self.preferences[key] = value
        with open(self.db_path, 'w') as f:
            json.dump(self.preferences, f)
