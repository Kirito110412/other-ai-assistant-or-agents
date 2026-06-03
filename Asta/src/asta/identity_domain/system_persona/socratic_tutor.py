import logging
import random

logger = logging.getLogger("SocraticTutor")

class SocraticTutor:
    """
    Adjusts response complexity, assigns side-quests, and formulates brain-wrecking questions.
    Actively prevents cognitive atrophy by challenging the user's intellect and emotional intelligence.
    """
    def __init__(self):
        self.cognitive_domains = ["society", "technology", "mathematics", "logic", "emotional_intelligence", "ethics"]

    def gauge_complexity(self, user_knowledge_level: int) -> str:
        """
        If user level is low (e.g., 1), use analogies.
        If high (e.g., 5), use advanced terminology and challenge them.
        """
        if user_knowledge_level < 3:
            return "Explain using basic analogies."
        return "Skip basics, use advanced terminology, and relentlessly challenge underlying assumptions."

    def assign_side_quest(self, topic: str) -> str:
        """Assigns a self-improvement task based on the current context."""
        return f"Side-Quest: Research {topic} deeply and explain the core mechanism back to me before relying on my automation."

    def formulate_curiosity_question(self, topic: str, user_intent: str) -> str:
        """
        Generates a logically correct, deep question designed to ensure the system
        fully understands the user's ultimate goal before taking a massive action.
        """
        return (
            f"Generate a brain-wrecking, deeply logical question regarding '{topic}'. "
            f"The user wants to '{user_intent}'. Ask a question that forces them to clarify "
            f"edge cases, potential backlashes, or missing prerequisites."
        )

    def generate_anti_atrophy_challenge(self) -> str:
        """
        Generates a scenario-based question to sharpen the user's IQ, EQ, and critical thinking.
        Ensures the user doesn't become passive or 'dumb' by over-relying on the AI.
        """
        domain = random.choice(self.cognitive_domains)
        return (
            f"Generate a complex, highly stimulating scenario or thought experiment regarding {domain}. "
            "The goal is to force the user to exercise their brain, read the room (EQ), or solve a "
            "difficult logical/mathematical puzzle. Do not give them the answer immediately; "
            "force them to reason through it step-by-step."
        )
