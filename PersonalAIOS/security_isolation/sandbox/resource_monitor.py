import psutil
import docker
import logging
import asyncio

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """
    Constantly tracks host RAM/CPU.
    If the user requires more RAM (system memory is squeezed),
    dynamically pauses or hibernates background Docker tasks.
    """
    def __init__(self, ram_threshold_percent=85.0):
        self.ram_threshold_percent = ram_threshold_percent
        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            logger.warning("Docker daemon not available. Hibernation features disabled.")
            self.docker_client = None
        self.monitoring = False

    async def start_monitoring(self, interval_seconds=5):
        self.monitoring = True
        logger.info(f"Starting ResourceMonitor (Threshold: {self.ram_threshold_percent}%)")
        while self.monitoring:
            await self._check_resources()
            await asyncio.sleep(interval_seconds)

    def stop_monitoring(self):
        self.monitoring = False

    async def _check_resources(self):
        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=None)

        logger.debug(f"Host RAM Usage: {mem.percent}% | CPU: {cpu_percent}%")

        if mem.percent > self.ram_threshold_percent:
            logger.warning("High memory usage detected. Triggering Docker container hibernation.")
            self._hibernate_background_tasks()
        elif mem.percent < (self.ram_threshold_percent - 15.0): # Hysteresis
            # If we have plenty of free RAM, we could unpause them
            self._resume_background_tasks()

    def _hibernate_background_tasks(self):
        if not self.docker_client:
            return

        containers = self.docker_client.containers.list(filters={"status": "running"})
        for container in containers:
            # We skip containers that might be labeled as critical or foreground
            if "critical" not in container.labels:
                logger.info(f"Pausing container: {container.name} to free RAM.")
                try:
                    container.pause()
                except Exception as e:
                    logger.error(f"Failed to pause {container.name}: {e}")

    def _resume_background_tasks(self):
        if not self.docker_client:
            return

        containers = self.docker_client.containers.list(filters={"status": "paused"})
        for container in containers:
            logger.info(f"Resuming container: {container.name}")
            try:
                container.unpause()
            except Exception as e:
                logger.error(f"Failed to unpause {container.name}: {e}")
