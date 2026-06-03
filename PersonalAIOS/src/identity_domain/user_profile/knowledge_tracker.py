class KnowledgeTracker:
    """
    Continuously maps the user's current skill levels.
    """
    def __init__(self):
        self.skill_map = {}

    def update_skill(self, domain: str, score_delta: float):
        """
        Increases or decreases user skill score based on their questions.
        """
        if domain not in self.skill_map:
            self.skill_map[domain] = 1.0 # Base level
        self.skill_map[domain] += score_delta

    def get_skill_level(self, domain: str) -> float:
        return self.skill_map.get(domain, 1.0)
