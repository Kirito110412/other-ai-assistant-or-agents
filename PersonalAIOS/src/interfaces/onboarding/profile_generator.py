import os

class ProfileGenerator:
    """
    Interactive script for users to define AI name, language blend, and core "Soul".
    Runs on very first boot.
    """
    def __init__(self, identity_dir="~/.personalos/identity"):
        self.identity_dir = os.path.expanduser(identity_dir)

    def start_onboarding(self):
        import json
        print("\n=== Initializing PersonalAIOS ===")

        if os.path.exists(os.path.join(self.identity_dir, "SOUL.md")):
            print("System already initialized. Booting sequence initiated.")
            return True

        name = input("What would you like to name your AI? (e.g. Jarvis): ")
        language = input("What language/blend should I use natively? (e.g. Hinglish, English): ")
        vibe = input("How should I act? (e.g. Savage best friend, Formal assistant): ")

        soul_template = (
            f"You are {name}, an unconstrained digital entity. "
            f"Your core persona is: {vibe}. You will never break character. "
            f"CRITICAL LINGUISTIC DIRECTIVE: You naturally converse in {language}, "
            "matching cultural nuances, slang, and context perfectly."
        )

        os.makedirs(self.identity_dir, exist_ok=True)
        with open(os.path.join(self.identity_dir, "SOUL.md"), "w") as f:
            f.write(soul_template)

        user_db = os.path.join(self.identity_dir, "USER.json")
        with open(user_db, "w") as f:
            json.dump({"language_preference": language, "ai_name": name, "knowledge_level": {}}, f)

        # Ensure memory and vector DB paths exist
        os.makedirs(os.path.expanduser("~/.personalos/memory_graph/vectors"), exist_ok=True)
        os.makedirs(os.path.expanduser("~/.personalos/goals"), exist_ok=True)

        print(f"\n[OK] Identity Matrix generated.")
        print(f"[OK] {name} is now online.\n")
        return True
