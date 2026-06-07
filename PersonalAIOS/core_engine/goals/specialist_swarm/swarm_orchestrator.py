import logging
import json
import asyncio
from typing import List, Dict, Any
from .specialist_forge import SpecialistForge

logger = logging.getLogger(__name__)

class SwarmOrchestrator:
    """
    Manages the lifecycle of specialists. It reads a complex task, identifies the
    exact required specialists, spins them up, queries them, and puts them to sleep.
    """
    def __init__(self, hybrid_switch):
        self.forge = SpecialistForge()
        self.hybrid_switch = hybrid_switch

    async def _identify_required_specialists(self, task: str) -> List[str]:
        """
        Queries the routing LLM to determine exactly which specialists are needed
        from the registry.
        """
        # We only pass the keys to the LLM to save tokens
        available_keys = list(self.forge.specialists.keys())

        prompt = (
            f"Given the following task: '{task}'\n"
            f"Select up to 3 specialist keys from the following list that are absolutely necessary to solve it. "
            f"Return ONLY a JSON list of strings representing the keys. No markdown, no explanations.\n"
            f"Available Keys: {available_keys}"
        )

        try:
            # We use local fast model for routing if possible
            response = await self.hybrid_switch.execute_query([{"role": "user", "content": prompt}], complexity=0.2)

            # Clean possible markdown block
            clean_json = response.replace("```json", "").replace("```", "").strip()
            selected_keys = json.loads(clean_json)

            if isinstance(selected_keys, list):
                # Filter valid keys
                valid_keys = [k for k in selected_keys if k in available_keys]
                return valid_keys
        except Exception as e:
            logger.error(f"Swarm Orchestrator failed to identify specialists: {e}")

        return []

    async def execute_task_with_swarm(self, task: str) -> str:
        """
        The main entrypoint. Identifies, awakens, queries, and aggregates results from specialists.
        """
        logger.info(f"Swarm Orchestrator analyzing task: {task[:50]}...")

        required_keys = await self._identify_required_specialists(task)

        if not required_keys:
            logger.warning("No specialists identified. Falling back to generalist routing.")
            return await self.hybrid_switch.execute_query([{"role": "user", "content": task}], complexity=0.8)

        logger.info(f"Awakening specialists: {required_keys}")

        # Awaken specialists and run them concurrently
        tasks = []
        for key in required_keys:
            agent = self.forge.get_specialist(key)
            if agent:
                tasks.append(self._query_specialist(agent, task))

        # Gather all specialist responses
        results = await asyncio.gather(*tasks)

        logger.info(f"Specialists returning to sleep. Aggregating {len(results)} expert analyses.")

        # Aggregate final result
        aggregation_prompt = (
            f"You are the Swarm Orchestrator. The user asked: '{task}'.\n"
            f"Here are the analyses from the awakened specialists:\n\n"
        )
        for idx, result in enumerate(results):
            aggregation_prompt += f"--- Specialist {idx+1} ---\n{result}\n\n"

        aggregation_prompt += "Synthesize these expert insights into a single, highly cohesive, absolute final answer."

        final_answer = await self.hybrid_switch.execute_query([{"role": "user", "content": aggregation_prompt}], complexity=0.9)
        return final_answer

    async def _query_specialist(self, agent: Dict[str, Any], task: str) -> str:
        """
        Constructs the strict context window for the specialist and queries the LLM.
        """
        messages = [
            {"role": "system", "content": agent["compiled_prompt"]},
            {"role": "user", "content": f"Execute your operational protocol on the following task: {task}"}
        ]

        # Specialists require high reasoning complexity
        logger.debug(f"Executing deep query for {agent['name']}")
        return await self.hybrid_switch.execute_query(messages, complexity=0.8)
