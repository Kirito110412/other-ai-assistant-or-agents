import json
import logging
from typing import List, Dict, Any
from PersonalAIOS.core_engine.routing.hybrid_switch import hybrid_router

logger = logging.getLogger("SequentialSolver")

class HighRiskInterceptor:
    """
    Intercepts vague or potentially destructive commands on the Host OS.
    Prevents the 'Constructive Laziness' problem (e.g., formatting a drive to clean it).
    """
    def __init__(self):
        self.dangerous_keywords = ["delete", "wipe", "format", "purchase", "buy", "transfer"]

    def assess_risk(self, command: str) -> Dict[str, Any]:
        command_lower = command.lower()
        if any(keyword in command_lower for keyword in self.dangerous_keywords):
            logger.warning(f"HIGH RISK COMMAND DETECTED: {command}")
            return {
                "is_risky": True,
                "interception_message": (
                    "Bhai, this command affects permanent host data or finances. "
                    "I have analyzed the request, but before I execute, you must confirm the specific parameters "
                    "to ensure nothing important is lost."
                )
            }
        return {"is_risky": False}

class SequentialSolver:
    """
    Acts as the Intent Router. Solves complex problems layer-by-layer
    and handles mixed multitasking commands (Hinglish/English).
    """
    def __init__(self):
        self.interceptor = HighRiskInterceptor()

    async def break_down_problem(self, user_input: str) -> Dict[str, Any]:
        """
        Deconstructs a massive problem into a strict sequence of foundational steps.
        Intercepts if the problem involves high-risk Host OS modifications.
        Splits tasks automatically.
        """
        risk_assessment = self.interceptor.assess_risk(user_input)
        if risk_assessment["is_risky"]:
            return {
                "status": "halted_for_confirmation",
                "message": risk_assessment["interception_message"],
                "tasks": []
            }

        # The Prompt forcing the LLM to act as the Intent Router
        system_prompt = (
            "You are the Intent Router for an autonomous OS. The user may speak in Hinglish or English. "
            "Analyze their request and split it into discrete, actionable tasks. "
            "For each task, classify its duration as either 'immediate' (takes seconds/minutes) "
            "or 'long_term' (takes hours/days/months like learning a topic or building a project). "
            "Output strictly as a JSON array of objects with keys: 'task_id', 'description', 'duration', 'required_modules'."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        try:
            logger.info("Routing raw input to LLM for Intent Splitting...")
            # We use local 3B model (complexity 0.1) for routing to keep it lightning fast and free
            json_response = await hybrid_router.execute_query(messages, complexity=0.1)

            # Clean markdown formatting if returned
            if json_response.startswith("```json"):
                json_response = json_response[7:-3]
            elif json_response.startswith("```"):
                json_response = json_response[3:-3]

            tasks = json.loads(json_response)

            return {
                "status": "executing",
                "message": "Intents parsed successfully.",
                "tasks": tasks
            }

        except Exception as e:
            logger.error(f"Failed to parse intents: {e}")
            return {
                "status": "failed",
                "message": "Neural pathway error during intent routing.",
                "tasks": []
            }
