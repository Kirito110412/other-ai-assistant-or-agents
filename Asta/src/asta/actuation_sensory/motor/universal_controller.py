import pyautogui

import logging
import platform

logger = logging.getLogger("UniversalMotor")

class UniversalMotorController:
    """
    Physical mouse/keyboard simulation for absolute OS control across macOS/Win/Linux.
    Uses PyAutoGUI as a cross-platform wrapper.
    """
    def __init__(self):
        # Safety fail-safe: Slamming mouse to corner kills the script
        pyautogui.FAILSAFE = True
        self.os_type = platform.system().lower()

    def click(self, x: int, y: int):
        """Clicks coordinates, handling scaling issues."""
        try:
            # On macOS Retina displays, Vision coordinates often need to be scaled down by 2
            if self.os_type == "darwin":
                x, y = x // 2, y // 2

            pyautogui.moveTo(x, y, duration=0.2) # Smooth, human-like move
            pyautogui.click()
            logger.debug(f"Physically clicked coordinates: ({x}, {y})")
        except pyautogui.FailSafeException:
            logger.error("MOTOR FAILSAFE TRIGGERED! User took back mouse control.")
        except Exception as e:
            logger.error(f"Motor click failed (Check OS Accessibility Permissions): {e}")

    def type_text(self, text: str, interval: float = 0.05):
        """
        Types organically to bypass bot-detection algorithms.
        """
        try:
            pyautogui.write(text, interval=interval)
            logger.debug(f"Physically typed: {text[:20]}...")
        except Exception as e:
            logger.error(f"Motor typing failed: {e}")
