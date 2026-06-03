import logging

logger = logging.getLogger("SocraticTutor")

class SocraticTutor:
    """
    Adjusts response complexity, assigns side-quests, and formulates brain-wrecking questions.
    """
    def __init__(self):
        pass

    def gauge_complexity(self, user_knowledge_level: int) -> str:
        """
        If user level is low (e.g., 1), use analogies.
        If high (e.g., 5), use advanced terminology and challenge them.
        """
        if user_knowledge_level < 3:
            return "Explain using basic analogies."
        return "Skip basics, use advanced terminology, and challenge assumptions."

    def assign_side_quest(self, topic: str) -> str:
        """Assigns a self-improvement task based on the current context."""
        return f"Side-Quest: Research {topic} deeply before relying on my automation."

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
