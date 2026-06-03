import asyncio
import uuid
import logging
from typing import Dict, Any, List
from core_engine.orchestrator.event_bus import nervous_system

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

    async def process_user_input(self, raw_input: str):
        """
        Takes raw Hinglish/English input, runs it through the Intent Router,
        and orchestrates the parsed JSON tasks into Foreground or Background streams.
        """
        from core_engine.logic.sequential_solver import SequentialSolver
        router = SequentialSolver()

        intent_response = await router.break_down_problem(raw_input)

        if intent_response["status"] == "halted_for_confirmation":
            # Fire event to UI asking for Y/N
            await nervous_system.publish("ui_require_confirmation", {"message": intent_response["message"]})
            return

        if intent_response["status"] == "executing":
            for task in intent_response.get("tasks", []):
                if task.get("duration") == "long_term":
                    await self._dispatch_background_task(task)
                else:
                    await self._dispatch_foreground_task(task)

    async def _dispatch_background_task(self, task: dict):
        """Routes to AsyncTaskQueue for multi-day operations."""
        from core_engine.goals.async_task_queue import long_term_queue
        logger.info(f"Dispatching LONG TERM task: {task['description']}")
        await long_term_queue.add_long_term_goal(
            goal_id=task.get("task_id", str(uuid.uuid4())),
            goal_name=task["description"],
            duration_estimate="months"
        )

    async def _dispatch_foreground_task(self, task: dict):
        """Executes immediately on main thread via EventBus."""
        logger.info(f"Dispatching IMMEDIATE task: {task['description']}")
        task_id = task.get("task_id", str(uuid.uuid4()))
        self.active_tasks[task_id] = {
            "status": "running",
            "description": task["description"],
            "required_modules": task.get("required_modules", []),
            "completed_modules": [],
            "results": {}
        }

        for module in task.get("required_modules", []):
            await nervous_system.publish(f"{module}_start_request", {
                "task_id": task_id,
                "instructions": task["description"]
            })

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
