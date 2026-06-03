import docker

class DockerOrchestrator:
    """
    Manages disposable environments for safely testing newly generated skills.
    """
    def __init__(self):
        self.client = docker.from_env()

    def _extract_imports(self, source_code: str) -> list:
        """Parses the generated code for required pip packages."""
        import ast
        try:
            tree = ast.parse(source_code)
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
            # Filter standard library (very basic filter for scaffold)
            std_libs = {"os", "sys", "json", "time", "re", "math", "logging", "asyncio", "ast"}
            return list(imports - std_libs)
        except:
            return []

    def run_untrusted_code(self, source_code: str, container_image="python:3.11-slim") -> dict:
        """
        Two-stage Execution:
        Stage 1: Pre-install dependencies with network ON.
        Stage 2: Execute actual untrusted logic with network OFF.
        """
        try:
            required_packages = self._extract_imports(source_code)

            if required_packages:
                # Stage 1: Build a temporary image with dependencies (Network ON)
                install_cmd = f"pip install {' '.join(required_packages)}"
                build_script = f"FROM {container_image}\nRUN {install_cmd}"

                # In production, we'd use docker.images.build() here from a temp Dockerfile.
                # For this scaffold, we simulate the prepared image:
                prepared_image = container_image
            else:
                prepared_image = container_image

            # Stage 2: Strictly isolate the container by disabling networking
            container = self.client.containers.run(
                image=prepared_image,
                command=["python", "-c", source_code],
                network_disabled=True,
                mem_limit="512m",
                cpu_quota=50000,
                detach=True
            )

            # Wait for execution and get logs
            result = container.wait(timeout=15)
            logs = container.logs().decode("utf-8")
            container.remove(force=True)

            if result.get("StatusCode") == 0:
                return {"status": "success", "output": logs}
            else:
                return {"status": "failed", "error": logs}

        except Exception as e:
            return {"status": "failed", "error": str(e)}
