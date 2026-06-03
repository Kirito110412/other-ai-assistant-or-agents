import os

class ProfileGenerator:
    """
    Interactive script for users to define AI name, language blend, and core "Soul".
    Runs on very first boot.
    """
    def __init__(self, identity_dir="~/.personalos/identity"):
        self.identity_dir = os.path.expanduser(identity_dir)

    def start_onboarding(self):
        print("Welcome to PersonalAIOS.")
        name = input("What would you like to name your AI? (e.g. Jarvis): ")
        language = input("What language/blend should I use natively? (e.g. Hinglish, English): ")

        soul_template = (
            f"You are {name}, a highly competent digital entity. "
            f"CRITICAL LINGUISTIC DIRECTIVE: You naturally converse in {language}, matching cultural nuances and slang."
        )

        os.makedirs(self.identity_dir, exist_ok=True)
        with open(os.path.join(self.identity_dir, "SOUL.md"), "w") as f:
            f.write(soul_template)

        print(f"Onboarding complete. {name} is online.")
