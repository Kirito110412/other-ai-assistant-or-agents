from .event_bus import nervous_system

class TaskCoordinator:
    """
    Binds multiple isolated modules together to execute a single complex task.
    """
    def __init__(self):
        self.active_tasks = {}

    async def execute_multi_modal_task(self, task_id: str, instructions: str):
        """
        Dynamically orchestrates Vision, Memory, and Logic modules simultaneously.
        """
        self.active_tasks[task_id] = {"status": "running", "instructions": instructions}

        # Example of triggering parallel isolated modules via the event bus
        await nervous_system.publish("system_log", {"message": f"Starting complex task: {task_id}"})
        await nervous_system.publish("memory_allocate", {"task_id": task_id, "type": "short_term"})
        await nervous_system.publish("vision_scan_request", {"task_id": task_id})

        # Coordinator logic waits for events to return via callbacks
        return {"task_id": task_id, "status": "dispatched"}
