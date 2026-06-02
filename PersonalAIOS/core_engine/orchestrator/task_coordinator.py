import asyncio
import uuid
import logging
from typing import Dict, Any, List
from .event_bus import nervous_system

logger = logging.getLogger("TaskCoordinator")

class TaskCoordinator:
    """
    Binds multiple isolated modules together to execute a single massive task.
    Manages the lifecycle of sub-agents and tracks global state across them.
    """
    def __init__(self):
        # Maps task_id to its state and associated sub-agents
        self.active_tasks: Dict[str, Dict[str, Any]] = {}

        # Subscribe to sub-agent completion events
        nervous_system.subscribe("sub_agent_complete", self._handle_sub_agent_completion)
        nervous_system.subscribe("sub_agent_failed", self._handle_sub_agent_failure)

    async def execute_multi_modal_task(self, instructions: str, required_modules: List[str]) -> str:
        """
        Dynamically orchestrates multiple modules (Vision, Memory, Logic, etc.) simultaneously.
        """
        task_id = str(uuid.uuid4())
        self.active_tasks[task_id] = {
            "status": "running",
            "instructions": instructions,
            "required_modules": required_modules,
            "completed_modules": [],
            "results": {}
        }

        logger.info(f"Orchestrating massive task [{task_id}] requiring modules: {required_modules}")

        # Trigger all required isolated modules in parallel via the event bus
        for module in required_modules:
            event_topic = f"{module}_start_request"
            payload = {
                "task_id": task_id,
                "instructions": instructions
            }
            await nervous_system.publish(event_topic, payload)

        return task_id

    async def _handle_sub_agent_completion(self, payload: dict):
        """
        Listens for 'sub_agent_complete' events on the bus.
        """
        task_id = payload.get("task_id")
        module_name = payload.get("module_name")
        result = payload.get("result")

        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task["completed_modules"].append(module_name)
            task["results"][module_name] = result

            logger.info(f"Sub-agent [{module_name}] completed work for task [{task_id}]")

            # Check if entire massive task is done
            if set(task["completed_modules"]) == set(task["required_modules"]):
                task["status"] = "completed"
                logger.info(f"Massive task [{task_id}] fully completed! Aggregating results.")
                await nervous_system.publish("massive_task_complete", {
                    "task_id": task_id,
                    "final_results": task["results"]
                })

    async def _handle_sub_agent_failure(self, payload: dict):
        """
        Handles graceful recovery or hard failure if a sub-agent crashes.
        """
        task_id = payload.get("task_id")
        module_name = payload.get("module_name")
        error = payload.get("error")

        if task_id in self.active_tasks:
            logger.error(f"Sub-agent [{module_name}] FAILED on task [{task_id}]: {error}")
            self.active_tasks[task_id]["status"] = "failed"
            # Could implement retry logic here based on exploitative solver
            await nervous_system.publish("massive_task_failed", {"task_id": task_id, "error": error})

# Global singleton
coordinator = TaskCoordinator()
