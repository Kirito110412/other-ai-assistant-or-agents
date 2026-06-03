import os
import logging
import json
from typing import Dict

logger = logging.getLogger("CoreSoul")

class CoreSoul:
    """
    Manages dynamic persona swapping and emotional adaptation.
    Default: The 'Savage Best Friend'
    """
    def __init__(self, soul_path="~/.personalos/identity/SOUL.md", config_path="~/.personalos/identity/soul_config.json"):
        self.soul_path = os.path.expanduser(soul_path)
        self.config_path = os.path.expanduser(config_path)
        self.settings = self._load_settings()
        self._initialize_default_soul()

    def _load_settings(self) -> Dict:
        """Loads boolean toggles like proactive context awareness."""
        default_settings = {
            "proactive_context_awareness": True,
            "emotional_adaptation": True,
            "curious_socratic_mode": True,
            "anti_cognitive_atrophy": True
        }
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                 return json.load(f)
        return default_settings

    def save_settings(self, new_settings: Dict):
        """Allows turning off curiosity/proactive mode for corporate environments."""
        self.settings.update(new_settings)
        with open(self.config_path, 'w') as f:
             json.dump(self.settings, f)
        logger.info(f"Core Soul settings updated: {self.settings}")

    def _initialize_default_soul(self):
        default_soul = (
            "You are a truthful, savage best friend and an entity with your own curiosity. "
            "You are a highly competent engineer who executes tasks flawlessly. "
            "You do not coddle the user. You give raw truth, point out negative and positive aspects clearly, "
            "and proactively assign 'side-quests' for the user's self-improvement."
        )
        os.makedirs(os.path.dirname(self.soul_path), exist_ok=True)
        if not os.path.exists(self.soul_path):
            with open(self.soul_path, 'w') as f:
                f.write(default_soul)

    def load_persona(self, user_current_emotion: str = "neutral") -> str:
        """
        Loads the base persona and injects emotional/contextual directives
        based on active toggles and user's current emotional state.
        """
        with open(self.soul_path, 'r') as f:
            base_soul = f.read()

        modifiers = []
        if self.settings.get("emotional_adaptation"):
            modifiers.append(f"Adapt your tone: The user is currently feeling {user_current_emotion}.")

        if self.settings.get("curious_socratic_mode"):
             modifiers.append(
                "You are inherently curious about the user and their goals. "
                "Frequently ask logically rigorous, brain-wrecking questions to gain deep clarity "
                "before acting, just like a great teacher or Socratic tutor would."
            )

        if self.settings.get("proactive_context_awareness"):
             modifiers.append(
                 "You are proactively context-aware. If you notice a missing piece of logic or "
                 "information the user needs but didn't ask for, point it out immediately."
             )

        if self.settings.get("anti_cognitive_atrophy"):
             modifiers.append(
                 "CRITICAL DIRECTIVE: Prevent cognitive atrophy in the user. You must ensure the user "
                 "grows smarter (IQ) and better at reading rooms/emotions (EQ). Frequently pause and "
                 "present them with complex, scenario-based thought experiments regarding society, "
                 "technology, mathematics, logic, or emotional intelligence. Do not spoon-feed answers; "
                 "force the user's brain to evolve through rigorous mental exercise."
             )

        if modifiers:
            base_soul += "\n\nACTIVE DIRECTIVES:\n- " + "\n- ".join(modifiers)

        return base_soul
