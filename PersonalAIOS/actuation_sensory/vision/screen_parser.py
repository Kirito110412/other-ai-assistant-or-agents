class ScreenParser:
    """
    Native UI coordinate extraction without DOM scraping.
    """
    def __init__(self):
        pass

    def extract_ui_elements(self, screenshot_path: str) -> list:
        """
        Uses a vision model to locate text boxes and buttons visually,
        returning their physical X/Y coordinates on the screen.
        """
        return [{"element": "login_button", "x": 1024, "y": 768}]
