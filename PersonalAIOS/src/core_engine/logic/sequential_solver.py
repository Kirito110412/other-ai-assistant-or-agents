import json
import logging
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field
from core_engine.routing.hybrid_switch import hybrid_router

logger = logging.getLogger("SequentialSolver")

# Pydantic Schemas for Structured JSON Output
class IntentTask(BaseModel):
    task_id: str = Field(description="A unique snake_case identifier for this sub-task")
    description: str = Field(description="A clear description of the action required")
    duration: Literal["immediate", "long_term"] = Field(description="Is this a quick action or a long running project?")
    required_modules: List[str] = Field(description="List of OS modules required (e.g., 'researcher', 'python_coder')")

class IntentResponse(BaseModel):
    tasks: List[IntentTask] = Field(description="The array of split tasks parsed from the user's input")

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
            "Ensure the output strictly conforms to the requested JSON schema."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        try:
            logger.info("Routing raw input to LLM for Intent Splitting using Structured JSON Outputs...")

            # We use the Hybrid Router's structural output capability to guarantee exact JSON matching
            json_response_str = await hybrid_router.execute_query(
                messages,
                complexity=0.1,
                response_format=IntentResponse.model_json_schema()
            )

            # Pydantic validation guarantees no fatal parsing errors
            parsed_intent = IntentResponse.model_validate_json(json_response_str)

            return {
                "status": "executing",
                "message": "Intents parsed successfully.",
                "tasks": [task.model_dump() for task in parsed_intent.tasks]
            }

        except Exception as e:
            logger.error(f"Failed to parse intents: {e}")
            return {
                "status": "failed",
                "message": "Neural pathway error during intent routing.",
                "tasks": []
            }
