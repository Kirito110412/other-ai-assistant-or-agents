import logging

logger = logging.getLogger("PythonCoder")

class PythonCoder:
    """
    Writes code from scratch. Can operate in a disposable environment for simple tasks
    or utilize a PersistentDevEnv for multi-hour stateful project development.
    """
    def __init__(self):
        self.active_devenvs = {}

    async def generate_and_test_script(self, full_prompt: str) -> dict:
        """
        Generates raw Python code, injects it into a disposable Docker sandbox,
        and validates the output (Original Fire-and-Forget Mode).
        """
        from asta.core_engine.routing.hybrid_switch import hybrid_router
        from asta.security_isolation.sandbox.docker_orchestrator import DockerOrchestrator

        system_prompt = (
            "You are an expert software engineer. Write a self-contained, standalone script "
            "that accomplishes the requested task. "
            "Output ONLY the raw code. No markdown formatting, no explanations."
        )

        try:
            # Force cloud model for complex coding
            raw_code = await hybrid_router.execute_query([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ], complexity=0.9)

            # Clean possible markdown
            if raw_code.startswith("```"):
                lines = raw_code.split("\n")
                raw_code = "\n".join(lines[1:-1]).strip()

            sandbox = DockerOrchestrator()
            result = sandbox.run_untrusted_code(raw_code)

            return {
                "status": "success",
                "generated_code": raw_code,
                "sandbox_result": result
            }

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def execute_stateful_task(self, project_name: str, commands: list[str]) -> dict:
        """
        Executes a sequence of terminal commands in a PersistentDevEnv (OpenHands Parity).
        """
        from asta.security_isolation.sandbox.persistent_devenv import PersistentDevEnv

        if project_name not in self.active_devenvs:
            env = PersistentDevEnv()
            project_id = env.create_workspace(project_name=project_name)
            if not project_id:
                 return {"status": "failed", "error": "Could not create stateful DevEnv"}
            self.active_devenvs[project_name] = {"env": env, "id": project_id}

        env_mgr = self.active_devenvs[project_name]["env"]
        p_id = self.active_devenvs[project_name]["id"]

        results = []
        for cmd in commands:
            logger.info(f"DevEnv [{project_name}]: Executing '{cmd}'")
            code, out = env_mgr.execute_command(p_id, cmd)
            results.append({"command": cmd, "exit_code": code, "output": out})
            if code != 0:
                 logger.warning(f"Command failed: {out}")
                 break

        return {"status": "success", "results": results}
