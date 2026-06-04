import asyncio
import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("AsyncTaskQueue")

class AsyncTaskQueue:
    """
    Persistent tracker for long-term operations lasting hours, days, or months.
    Survives system reboots by serializing task state to disk.
    Also handles Cron Job style scheduling, ensuring tasks run repeatedly on set intervals.
    """
    def __init__(self, storage_path="~/.personalos/goals/active_tasks.json"):
        self.storage_path = os.path.expanduser(storage_path)
        self.queue: Dict[str, Dict[str, Any]] = self._load_state()
        self._background_tasks = []

    def _load_state(self) -> dict:
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_state(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.queue, f, indent=4)

    async def add_long_term_goal(self, goal_id: str, goal_name: str, duration_estimate: str, cron_interval: int = None):
        """
        Adds a massive goal (e.g., 'Code AAA game') or a recurring cron task to the background orchestrator.
        """
        self.queue[goal_id] = {
            "goal": goal_name,
            "status": "running",
            "duration_estimate": duration_estimate,
            "progress_percent": 0.0,
            "cron_interval": cron_interval,
            "sub_tasks": []
        }
        self._save_state()
        logger.info(f"Added massive long-term goal: {goal_name} [{goal_id}]")

        # Starts background loop for this specific goal
        task = asyncio.create_task(self._background_execution_loop(goal_id))
        self._background_tasks.append(task)

    async def _background_execution_loop(self, goal_id: str):
        """
        Runs persistently. Periodically checks in, spawns sub-tasks via Coordinator,
        and saves state so progress isn't lost if the machine sleeps/reboots.
        """
        from asta.core_engine.logic.sequential_solver import SequentialSolver
        solver = SequentialSolver()

        while True:
            if goal_id not in self.queue:
                break # Goal was removed

            goal_data = self.queue[goal_id]

            if goal_data["status"] == "completed" and not goal_data.get("cron_interval"):
                logger.info(f"Long-term goal [{goal_id}] is completed. Ending background loop.")
                break

            logger.debug(f"Heartbeat for long-term goal [{goal_id}]: {goal_data['progress_percent']}% complete.")

            # Use SequentialSolver to determine next sub-steps
            try:
                # If it's a cron job, re-evaluate the main goal text. If a long-term project, evaluate next sub-task.
                eval_query = f"I am currently working on '{goal_data['goal']}'. Progress is {goal_data['progress_percent']}%. What is the precise next action?"
                next_step_data = await solver.break_down_problem(eval_query)

                if next_step_data.get("status") == "executing" and next_step_data.get("tasks"):
                    from asta.core_engine.orchestrator.event_bus import nervous_system
                    # Route to central event bus for processing by correct subsystem
                    await nervous_system.publish("execute_subtask", next_step_data["tasks"][0])
            except Exception as e:
                logger.error(f"Failed to evaluate next step for {goal_id}: {e}")

            # Persist any state changes
            self._save_state()

            # Sleep mechanism. If cron, sleep cron interval. If standard massive project, sleep e.g., 1 hr (60s scaffold).
            sleep_time = goal_data.get("cron_interval") or 60
            await asyncio.sleep(sleep_time)

    async def update_progress(self, goal_id: str, percent: float, status: str = "running"):
        if goal_id in self.queue:
            self.queue[goal_id]["progress_percent"] = percent
            self.queue[goal_id]["status"] = status
            self._save_state()

            # Fire event to update the Menu Bar UI and Avatar
            from asta.core_engine.orchestrator.event_bus import nervous_system
            await nervous_system.publish("ui_task_progress_update", {
                "goal_id": goal_id,
                "goal_name": self.queue[goal_id]["goal"],
                "progress_percent": percent,
                "duration_estimate": self.queue[goal_id]["duration_estimate"]
            })

# Global singleton
long_term_queue = AsyncTaskQueue()
