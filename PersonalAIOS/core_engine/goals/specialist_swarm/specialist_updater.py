import logging
import asyncio
from datetime import datetime, timezone
from .specialist_forge import SpecialistForge

logger = logging.getLogger(__name__)

class SpecialistUpdater:
    """
    Automated job to keep the 200+ Specialist Roster continuously relevant.
    It hooks into the system's Cron/AsyncTaskQueue to run periodically (e.g., weekly),
    allowing specialists to "scrape the web" and refine their own system prompts based on new industry trends.
    """
    def __init__(self, hybrid_switch):
        self.forge = SpecialistForge()
        self.hybrid_switch = hybrid_switch

    async def run_weekly_update_cycle(self):
        logger.info("Initiating Specialist Swarm Auto-Update Cycle...")

        updated_registry = self.forge.specialists.copy()

        # In a real scenario, updating 200+ agents via LLM in one go is heavy.
        # We process a batch of them per cycle.
        sorted_keys = sorted(updated_registry.keys(), key=lambda k: updated_registry[k].get('last_updated', ''))
        batch_keys = sorted_keys[:5] # Prioritize oldest updated

        for key in batch_keys:
            spec = updated_registry[key]
            logger.info(f"Updating Specialist Knowledge for: {spec['name']}")

            # Step 1: LLM determines the latest trends for this niche
            trend_prompt = f"What are the top 3 absolute latest developments in the field of {spec['name']} as of this week? Be brief."
            trends = await self.hybrid_switch.execute_query([{"role": "user", "content": trend_prompt}], complexity=0.4)

            # Step 2: Dynamically inject trends into the system prompt
            base_prompt = spec.get("base_prompt", spec["system_prompt"]) # Preserve original
            new_prompt = f"{base_prompt}\n\nCurrent Edge Knowledge to consider: {trends}"

            spec["base_prompt"] = base_prompt
            spec["system_prompt"] = new_prompt
            spec["last_updated"] = datetime.now(timezone.utc).isoformat()

            updated_registry[key] = spec
            await asyncio.sleep(0.5) # Prevent rate-limiting

        self.forge.update_registry(updated_registry)
        logger.info("Specialist Swarm Auto-Update Cycle Complete.")
