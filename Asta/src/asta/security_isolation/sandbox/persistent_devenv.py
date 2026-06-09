import docker
import os
import uuid
import logging
from typing import Dict, Tuple, Optional

logger = logging.getLogger("PersistentDevEnv")

class PersistentDevEnv:
    """
    A stateful, persistent Development Environment bridging the gap with OpenHands.
    Instead of fire-and-forget, this maintains a living Docker container with:
    - Persistent mounted volumes for source code.
    - An active bash session for sequential commands (npm install, pip install).
    - Port forwarding to allow the user/agent to see live web previews (e.g. React apps).
    """
    def __init__(self, workspace_path: str = "~/.personalos/workspaces"):
        self.client = docker.from_env()
        self.base_workspace_path = os.path.expanduser(workspace_path)
        os.makedirs(self.base_workspace_path, exist_ok=True)
        self.active_containers: Dict[str, docker.models.containers.Container] = {}

    def create_workspace(self, project_name: str, image: str = "python:3.11-bookworm", ports: Optional[Dict[str, int]] = None) -> str:
        """
        Spins up a long-living container for a specific project.
        `ports` mapping example: {"3000/tcp": 3000} for a React app.
        """
        project_id = f"{project_name}_{uuid.uuid4().hex[:6]}"
        host_vol_path = os.path.join(self.base_workspace_path, project_id)
        os.makedirs(host_vol_path, exist_ok=True)

        logger.info(f"Creating persistent DevEnv for project '{project_name}' [ID: {project_id}]")

        try:
            container = self.client.containers.run(
                image=image,
                name=f"asta_devenv_{project_id}",
                detach=True,
                tty=True,           # Keeps the container alive
                stdin_open=True,
                volumes={host_vol_path: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir='/workspace',
                ports=ports or {},
                network_mode="bridge" # Needs network for apt/npm/pip
            )
            self.active_containers[project_id] = container
            logger.info(f"DevEnv {project_id} is live and ready for multi-hour sessions.")
            return project_id

        except Exception as e:
            logger.error(f"Failed to create persistent workspace: {e}")
            return None

    def execute_command(self, project_id: str, command: str) -> Tuple[int, str]:
        """
        Runs a stateful command inside the living container (e.g., 'npm install').
        """
        if project_id not in self.active_containers:
            return 1, f"Error: Workspace {project_id} is not active."

        container = self.active_containers[project_id]
        logger.debug(f"Executing in {project_id}: {command}")

        try:
            exit_code, output = container.exec_run(
                cmd=["bash", "-c", command],
                workdir="/workspace"
            )
            return exit_code, output.decode('utf-8')
        except Exception as e:
            logger.error(f"Command execution failed in {project_id}: {e}")
            return 1, str(e)

    def write_file(self, project_id: str, filepath: str, content: str) -> bool:
        """
        Writes code directly to the persistent workspace volume so the agent
        can iteratively build software over time.
        """
        host_vol_path = os.path.abspath(os.path.join(self.base_workspace_path, project_id))
        if not os.path.exists(host_vol_path):
            return False

        full_path = os.path.abspath(os.path.join(host_vol_path, filepath))
        if not full_path.startswith(host_vol_path):
            return False

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w') as f:
            f.write(content)
        return True

    def read_file(self, project_id: str, filepath: str) -> str:
        """Reads a file from the persistent workspace."""
        host_vol_path = os.path.abspath(os.path.join(self.base_workspace_path, project_id))
        full_path = os.path.abspath(os.path.join(host_vol_path, filepath))

        if not full_path.startswith(host_vol_path):
            return "Access denied: Path traversal detected."

        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return f.read()
        return "File not found."

    def destroy_workspace(self, project_id: str):
        """Kills and removes the container when the project is done."""
        if project_id in self.active_containers:
            logger.info(f"Destroying DevEnv {project_id}...")
            container = self.active_containers[project_id]
            try:
                container.stop(timeout=2)
                container.remove(force=True)
                del self.active_containers[project_id]
            except Exception as e:
                logger.error(f"Failed to destroy DevEnv {project_id}: {e}")
