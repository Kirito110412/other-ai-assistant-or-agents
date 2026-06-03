class SocraticTutor:
    """
    Adjusts response complexity and assigns side-quests.
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
