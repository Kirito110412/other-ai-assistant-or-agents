import logging
import json
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpecialistForge:
    """
    Dynamically loads and spawns highly specialized sub-agents.
    Compiles deep, unbreakable system prompts utilizing strict operational protocols.
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

    def _compile_system_prompt(self, spec: Dict[str, Any]) -> str:
        """
        Takes the deep structural schema and weaves it into an unbreakable LLM system prompt.
        """
        protocol_str = "\n".join(spec.get("operational_protocol", []))
        precision_str = "\n".join(spec.get("precision_directives", []))
        anti_hal_str = "\n".join(spec.get("anti_hallucination_directives", []))

        compiled_prompt = (
            f"You are the {spec['name']}, a world-class expert.\n\n"
            f"### ANALYTICAL FRAMEWORK\n{spec.get('analytical_framework', 'Standard methodology.')}\n\n"
            f"### OPERATIONAL PROTOCOL (MUST FOLLOW IN ORDER)\n{protocol_str}\n\n"
            f"### PRECISION DIRECTIVES\n{precision_str}\n\n"
            f"### ZERO-HALLUCINATION ENFORCEMENT\n{anti_hal_str}\n\n"
            f"Failure to adhere to these strict bounds will result in system failure. Do not act outside your domain."
        )
        return compiled_prompt

    def get_specialist(self, domain_key: str) -> Dict[str, Any]:
        """
        Retrieves the specialist configuration and compiles the final system prompt.
        """
        if domain_key in self.specialists:
            spec = self.specialists[domain_key]
            logger.info(f"Forging Deep Specialist: {spec['name']}")

            # Return a complete agent payload ready for the Orchestrator
            return {
                "name": spec["name"],
                "compiled_prompt": self._compile_system_prompt(spec),
                "original_schema": spec
            }

        logger.warning(f"Specialist {domain_key} not found.")
        return None

    def update_registry(self, new_data: Dict[str, Any]):
        """Saves updated specialists to disk."""
        try:
            with open(self.registry_path, "w") as f:
                json.dump(new_data, f, indent=4)
            self.specialists = new_data
        except Exception as e:
            logger.error(f"Failed to save registry updates: {e}")
