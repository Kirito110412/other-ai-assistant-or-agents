import pyautogui
import os
import base64
import tempfile

class ScreenParser:
    """
    Native UI coordinate extraction without DOM scraping.
    """
    def __init__(self):
        self.default_temp_dir = tempfile.gettempdir()

    def capture_screen(self, save_path: str = None):
        """
        Uses PyAutoGUI (cross platform) to grab the current screen state.
        Uses OS-agnostic temp directory if no save path is provided.
        """
        if save_path is None:
            save_path = os.path.join(self.default_temp_dir, "current_screen.png")

        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return save_path

    async def extract_ui_elements(self, screenshot_path: str, target_element: str) -> dict:
        """
        Sends the screenshot to a vision model (GPT-4o) to locate a specific element visually,
        returning its physical X/Y coordinates on the screen.
        """
        from core_engine.routing.hybrid_switch import hybrid_router
        import json

        if not os.path.exists(screenshot_path):
            return {"error": "Screenshot not found"}

        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        prompt = (
            f"Analyze this screenshot. I need to click on the '{target_element}'. "
            "Return ONLY a JSON object with the estimated X and Y coordinates of the center "
            "of this element based on standard 1920x1080 scaling. Example: {\"x\": 500, \"y\": 300}"
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_string}"
                        }
                    }
                ]
            }
        ]

        try:
            # Complexity 1.0 forces it to the massive cloud model (GPT-4o Vision)
            response = await hybrid_router.execute_query(messages, complexity=1.0)

            # Clean markdown formatting if present
            if response.startswith("```json"):
                response = response[7:-3]
            elif response.startswith("```"):
                response = response[3:-3]

            return json.loads(response)

        except Exception as e:
            return {"error": str(e)}
