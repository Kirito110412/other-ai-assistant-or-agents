class HybridSwitch:
    """
    Instantly routes tasks between local 3B models and heavy cloud LLMs.
    """
    def __init__(self):
        self.local_model_url = "http://localhost:11434/v1"
        self.cloud_models = ["gpt-4o", "claude-3-5-sonnet-20241022"]

    def route_query(self, query: str, complexity: float) -> str:
        """
        Determines the most efficient neural pathway based on complexity score.
        """
        if complexity < 0.4:
            return "local_3b_model"
        return "cloud_heavy_model"
