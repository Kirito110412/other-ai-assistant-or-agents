import logging
import uuid
from typing import List
from core_engine.orchestrator.event_bus import nervous_system

logger = logging.getLogger("DomainSpawner")

class DomainSpawner:
    """
    Identifies missing knowledge and dynamically spawns specific sub-agents
    to research and learn entirely new domains.
    """
    def __init__(self):
        # We would inject a reference to the User Profile / Core Memory here
        # to check what domains are already known.
        self.known_domains = ["basic_math", "python_scripting", "general_reasoning"]

    async def detect_and_spawn(self, task_requirements: List[str]):
        """
        Scans required knowledge against current User Profile / Core Memory.
        If missing (e.g., 'electrochemistry'), it fires an event to spawn
        a dedicated Research Agent to learn it.
        """
        missing_domains = [req for req in task_requirements if req not in self.known_domains]

        if not missing_domains:
            logger.info("All required domains are known. No learning required.")
            return

        logger.warning(f"Missing knowledge detected in domains: {missing_domains}. Spawning learners...")

        for domain in missing_domains:
            agent_id = f"learner_{domain}_{uuid.uuid4().hex[:8]}"
            logger.info(f"Spawning dynamic sub-agent [{agent_id}] to master [{domain}]")

            # Fire an event to the orchestrator to spin up the Research Web Scraper
            # and Paper Synthesizer to pull knowledge on this domain.
            await nervous_system.publish("spawn_dynamic_agent", {
                "agent_id": agent_id,
                "agent_type": "researcher",
                "target_domain": domain,
                "urgency": "high"
            })

            # Optimistically add to known domains (in reality, Critic Evaluator approves this later)
            self.known_domains.append(domain)

# Global singleton
domain_spawner = DomainSpawner()
