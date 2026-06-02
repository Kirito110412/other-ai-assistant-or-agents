import pyautogui

class MacOSController:
    """
    Physical mouse/keyboard simulation for absolute OS control.
    """
    def __init__(self):
        # Safety fail-safe
        pyautogui.FAILSAFE = True

    def click(self, x: int, y: int):
        pyautogui.click(x, y)

    def type_text(self, text: str, interval: float = 0.05):
        """
        Types organically to bypass bot-detection algorithms.
        """
        pyautogui.write(text, interval=interval)
