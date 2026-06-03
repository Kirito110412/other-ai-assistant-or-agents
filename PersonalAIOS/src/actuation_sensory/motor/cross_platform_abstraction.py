import platform
import os

class CrossPlatformAbstraction:
    """
    Ensures OS control (macOS/Win/Linux) supports any local/cloud machine.
    """
    def __init__(self):
        self.os_type = platform.system().lower()

    def get_host_environment_details(self) -> dict:
        return {
            "os": self.os_type,
            "architecture": platform.machine(),
            "has_gui": self._check_gui_availability()
        }

    def _check_gui_availability(self) -> bool:
        if self.os_type == "linux":
            return os.environ.get("DISPLAY") is not None
        return True # Mac/Win usually have GUI unless run headless
