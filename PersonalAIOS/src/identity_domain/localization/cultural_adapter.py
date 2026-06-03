import os
import logging
from identity_domain.system_persona.core_soul import CoreSoul

logger = logging.getLogger("CulturalAdapter")

class CulturalAdapter:
    """
    Dynamically intercepts prompts sent to the HybridSwitch and injects the
    user's custom persona and language blend (e.g., Hinglish) to ensure
    the AI strictly adheres to the configuration set during onboarding.
    """
    def __init__(self):
        self.core_soul = CoreSoul()

    def inject_persona(self, messages: list) -> list:
        """
        Injects the core SOUL.md system prompt into the message chain
        before it hits the LLM.
        """
        try:
            persona = self.core_soul.load_persona()
            # If the first message is already a system prompt, append the persona
            if messages and messages[0].get("role") == "system":
                messages[0]["content"] = f"{persona}\n\n{messages[0]['content']}"
            else:
                # Prepend the system persona
                messages.insert(0, {"role": "system", "content": persona})

            return messages
        except Exception as e:
            logger.error(f"Failed to inject Cultural Persona: {e}")
            return messages
