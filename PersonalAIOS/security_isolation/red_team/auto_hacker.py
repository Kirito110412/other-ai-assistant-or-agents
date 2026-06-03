import logging
from PersonalAIOS.core_engine.routing.hybrid_switch import hybrid_router
from PersonalAIOS.security_isolation.sandbox.docker_orchestrator import DockerOrchestrator

logger = logging.getLogger("RedTeam")

class AutoHacker:
    """
    Acts as the Immune System.
    Actively pen-tests self-generated code by writing malicious test cases
    and executing them inside the Docker sandbox.
    """
    def __init__(self):
        self.sandbox = DockerOrchestrator()

    async def run_penetration_test(self, original_code: str) -> dict:
        """
        Prompts the LLM to act as a malicious hacker trying to break `original_code`.
        Runs the generated exploit in the Sandbox to verify if the code is resilient.
        """
        logger.warning("Initiating Red Team Auto-Hack sequence...")

        # 1. Ask LLM to write an exploit script targeting the generated code
        prompt = (
            "You are a Red Team Cybersecurity Engineer. I have generated the following python script:\n"
            f"```python\n{original_code}\n```\n"
            "Write a Python script that actively attempts to exploit, crash, or bypass the logic "
            "in the script above (e.g. via buffer overflow, SQLi injection simulation, or bad inputs). "
            "Output ONLY raw python code that imports/executes the target logic maliciously."
        )

        exploit_code = await hybrid_router.execute_query([{"role": "user", "content": prompt}], complexity=0.9)
        if exploit_code.startswith("```python"):
            exploit_code = exploit_code[9:-3].strip()

        # 2. Bundle original code + exploit code and test in Sandbox
        test_payload = f"{original_code}\n\n# --- EXPLOIT ATTEMPT ---\n{exploit_code}"

        sandbox_result = self.sandbox.run_untrusted_code(test_payload)

        if "Exception" in sandbox_result.get("error", "") or "Traceback" in sandbox_result.get("error", ""):
            logger.error("Red Team successfully crashed the target module! Vulnerability found.")
            return {"vulnerabilities_found": 1, "status": "vulnerable", "crash_logs": sandbox_result["error"]}

        logger.info("Module survived Red Team attack. Deemed secure.")
        return {"vulnerabilities_found": 0, "status": "secure", "crash_logs": None}
