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
        Stage 1: Pre-install dependencies dynamically with network ON.
        Stage 2: Execute actual untrusted logic with network strictly OFF.
        """
        import uuid
        import io
        import logging

        logger = logging.getLogger("DockerOrchestrator")

        try:
            required_packages = self._extract_imports(source_code)
            prepared_image = container_image
            custom_tag = None

            if required_packages:
                logger.info(f"Stage 1: Building temporary image with dependencies: {required_packages}")
                custom_tag = f"paios_sandbox_{uuid.uuid4().hex[:8]}"
                install_cmd = f"pip install --no-cache-dir {' '.join(required_packages)}"

                dockerfile_str = f"FROM {container_image}\nRUN {install_cmd}"
                f = io.BytesIO(dockerfile_str.encode('utf-8'))

                try:
                    # Build image with network access to fetch PyPI packages
                    image, build_logs = self.client.images.build(
                        fileobj=f,
                        rm=True,
                        tag=custom_tag,
                        network_mode="bridge"
                    )
                    prepared_image = custom_tag
                except docker.errors.BuildError as be:
                    logger.error(f"Sandbox Stage 1 Build Failed: {be}")
                    return {"status": "failed", "error": f"Dependency installation failed: {be}"}

            logger.info("Stage 2: Executing untrusted code with network explicitly DISABLED.")
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

            # Cleanup temporary image if one was created
            if custom_tag:
                try:
                    self.client.images.remove(image=custom_tag, force=True)
                except Exception as cleanup_err:
                    logger.warning(f"Failed to cleanup temp sandbox image {custom_tag}: {cleanup_err}")

            if result.get("StatusCode") == 0:
                return {"status": "success", "output": logs}
            else:
                return {"status": "failed", "error": logs}

        except Exception as e:
            return {"status": "failed", "error": str(e)}
