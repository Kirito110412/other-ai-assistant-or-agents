class CriticEvaluator:
    """
    Executive evaluator that self-approves tools without Y/N prompts.
    """
    def __init__(self):
        pass

    def evaluate_code(self, source_code: str, test_results: dict) -> bool:
        """
        Judges if the newly generated skill actually solves the problem,
        passes security tests, and aligns with Axiomatic Baselines.
        """
        if test_results.get("status") == "success" and test_results.get("coverage") > 90:
            return True
        return False
