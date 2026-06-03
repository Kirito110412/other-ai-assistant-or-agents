import docker

class DockerOrchestrator:
    """
    Manages disposable environments for safely testing newly generated skills.
    """
    def __init__(self):
        self.client = docker.from_env()

    def run_untrusted_code(self, source_code: str, container_image="python:3.11-slim") -> dict:
        """
        Spawns an isolated container with absolutely no network access to test logic.
        """
        try:
            # Strictly isolates the container by disabling networking
            container = self.client.containers.run(
                image=container_image,
                command=["python", "-c", source_code],
                network_disabled=True,
                mem_limit="512m",
                cpu_quota=50000,
                detach=True
            )

            # Wait for execution and get logs
            result = container.wait(timeout=10)
            logs = container.logs().decode("utf-8")
            container.remove(force=True)

            if result.get("StatusCode") == 0:
                return {"status": "success", "output": logs}
            else:
                return {"status": "failed", "error": logs}

        except Exception as e:
            return {"status": "failed", "error": str(e)}
