class PythonCoder:
    """
    Writes Python scripts from scratch when a specific tool is lacking.
    """
    def __init__(self):
        pass

    async def generate_and_test_script(self, task_description: str) -> dict:
        """
        Generates raw Python code, injects it into the Docker sandbox,
        and validates the output.
        """
        from PersonalAIOS.core_engine.routing.hybrid_switch import hybrid_router
        from PersonalAIOS.security_isolation.sandbox.docker_orchestrator import DockerOrchestrator

        prompt = (
            "You are an expert Python engineer. Write a self-contained, standalone Python script "
            f"that accomplishes the following task: {task_description}. "
            "Output ONLY the raw python code. No markdown formatting, no explanations."
        )

        try:
            # Force cloud model for complex coding
            raw_code = await hybrid_router.execute_query([{"role": "user", "content": prompt}], complexity=0.9)

            # Clean possible markdown
            if raw_code.startswith("```python"):
                raw_code = raw_code[9:-3].strip()

            sandbox = DockerOrchestrator()
            result = sandbox.run_untrusted_code(raw_code)

            return {
                "generated_code": raw_code,
                "sandbox_result": result
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}
