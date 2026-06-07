import logging
import json
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpecialistForge:
    """
    Dynamically loads and spawns highly specialized sub-agents.
    Instead of a general 'TaskWorker', this forge provides
    niche specialists (e.g., 'Cybersecurity Red-Teamer', 'Biotech Researcher').
    """
    def __init__(self, registry_path="PersonalAIOS/core_engine/goals/specialist_swarm/specialists_registry.json"):
        self.registry_path = registry_path
        self.specialists = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if not os.path.exists(self.registry_path):
            logger.warning(f"Specialist registry not found at {self.registry_path}. Spawning basic roster.")
            return {}
        try:
            with open(self.registry_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load specialist registry: {e}")
            return {}

    def get_specialist(self, domain: str) -> Dict[str, Any]:
        """
        Retrieves the system prompt and configuration for a specific specialist.
        """
        domain_key = domain.lower().replace(" ", "_")
        if domain_key in self.specialists:
            logger.info(f"Spawning Specialist: {self.specialists[domain_key]['name']}")
            return self.specialists[domain_key]

        logger.warning(f"No exact specialist found for {domain}. Falling back to nearest archetype.")
        # Fallback logic would go here
        return {"name": "Generalist", "system_prompt": "You are a helpful assistant.", "traits": []}

    def update_registry(self, new_data: Dict[str, Any]):
        """Saves updated specialists to disk."""
        try:
            with open(self.registry_path, "w") as f:
                json.dump(new_data, f, indent=4)
            self.specialists = new_data
        except Exception as e:
            logger.error(f"Failed to save registry updates: {e}")
