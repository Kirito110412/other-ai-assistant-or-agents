import logging
from typing import Dict, Any, Tuple
from core_engine.routing.hybrid_switch import hybrid_router
from feature_architecture.research.web_scraper import WebScraper
from core_engine.routing.hybrid_switch import hybrid_router

logger = logging.getLogger("CriticEvaluator")

class CriticEvaluator:
    """
    Executive evaluator that tests code and performs auto-repair via web research if logic fails.
    Before asking the user, it verifies logic against fundamental axioms.
    If it fails, it analyzes the failure, searches forums/docs, and returns pointers for revision.
    """
    def __init__(self):
        self.scraper = WebScraper()

    async def evaluate_and_repair(self, task_description: str, python_coder_module) -> Dict[str, Any]:
        """
        Attempts to generate, test, and auto-repair a Python script.
        If it fails, it doesn't give up. It researches the error and tries again.
        Returns the final successful code and its stats, or a failure after max retries.
        """
        max_retries = 3
        current_attempt = 1
        repair_context = ""

        while current_attempt <= max_retries:
            logger.info(f"Critic Evaluator Attempt {current_attempt}/{max_retries} for task: {task_description}")

            # Pass any previous failure context to the coder
            full_prompt = task_description
            if repair_context:
                full_prompt += f"\n\nPREVIOUS FAILURE CONTEXT AND RESEARCH:\n{repair_context}\nFix the previous implementation based on this information."

            # Generate and run code in sandbox
            generation_result = await python_coder_module.generate_and_test_script(full_prompt)

            if generation_result.get("status") == "failed":
                 # Sandbox error or syntax issue
                 error_msg = generation_result.get("error", "Unknown Sandbox Error")
                 logger.warning(f"Generation failed: {error_msg}")
                 repair_pointers = await self._analyze_failure_and_research(task_description, error_msg, generation_result.get("generated_code", ""))
                 repair_context = f"Error: {error_msg}\nCritic Suggestions & Web Findings: {repair_pointers}"
                 current_attempt += 1
                 continue

            sandbox_res = generation_result.get("sandbox_result", {})
            if sandbox_res.get("status") == "success":
                # Passes sandbox execution. Now verify logic against axioms using Critic LLM
                logic_valid, critique = await self._verify_logic_axioms(
                    task_description,
                    generation_result.get("generated_code", ""),
                    sandbox_res.get("output", "")
                )

                if logic_valid:
                    logger.info("Critic Evaluator: Code passed sandbox and axiomatic logic verification.")
                    return {
                        "status": "success",
                        "final_code": generation_result["generated_code"],
                        "sandbox_output": sandbox_res.get("output", ""),
                        "attempts_used": current_attempt
                    }
                else:
                    logger.warning(f"Axiomatic logic failed. Critic says: {critique}")
                    # Research the logic failure
                    repair_pointers = await self._analyze_failure_and_research(task_description, critique, generation_result.get("generated_code", ""))
                    repair_context = f"Logic Failure: {critique}\nCritic Suggestions & Web Findings: {repair_pointers}"
                    current_attempt += 1
            else:
                 # Code ran but threw exception
                 error_msg = sandbox_res.get("error", "Unknown Execution Error")
                 logger.warning(f"Execution failed: {error_msg}")
                 repair_pointers = await self._analyze_failure_and_research(task_description, error_msg, generation_result.get("generated_code", ""))
                 repair_context = f"Execution Error: {error_msg}\nCritic Suggestions & Web Findings: {repair_pointers}"
                 current_attempt += 1

        logger.error(f"Critic Evaluator failed to repair code after {max_retries} attempts.")
        return {"status": "failed", "reason": "Max auto-repair retries exceeded", "last_context": repair_context}

    async def _verify_logic_axioms(self, task: str, code: str, output: str) -> Tuple[bool, str]:
        """
        Uses the LLM as a harsh Critic to verify if the output aligns with mathematical/physical axioms
        and actually solves the user's task.
        """
        prompt = (
            f"You are the Critic Engine. Your job is to rigorously evaluate if the following code "
            f"solves the task: '{task}'.\n\nCode:\n{code}\n\nOutput:\n{output}\n\n"
            f"Does this mathematically and logically make sense? Are there hallucinations? "
            f"Respond with 'VALID' if perfect. If flawed, explain exactly why it is wrong."
        )
        # Use cloud model for rigorous logic evaluation
        evaluation = await hybrid_router.execute_query([{"role": "user", "content": prompt}], complexity=0.9)

        if "VALID" in evaluation.upper()[:20]:
            return True, "Valid"
        return False, evaluation

    async def _analyze_failure_and_research(self, task: str, error_msg: str, bad_code: str) -> str:
        """
        Takes an error, identifies the root cause, and simulates searching Reddit/Forums
        for a solution.
        """
        logger.info("Critic analyzing failure and initiating web research...")

        # 1. Ask local/cloud model what the error means
        analysis_prompt = (
            f"Analyze this Python error or logic failure for task '{task}':\n"
            f"Error: {error_msg}\n"
            f"Code:\n{bad_code}\n\n"
            f"What should I search on StackOverflow or Reddit to fix this? Provide a search query."
        )
        search_query = await hybrid_router.execute_query([{"role": "user", "content": analysis_prompt}], complexity=0.5)

        # 2. Simulate Web Research (In a real implementation, use duckduckgo/google search APIs + WebScraper)
        # We will mock the search URL for now and extract
        search_url = f"https://duckduckgo.com/html/?q={search_query.replace(' ', '+')}+site:stackoverflow.com+OR+site:reddit.com"

        scraped_data = await self.scraper.extract_clean_text(search_url)

        # 3. Synthesize findings into repair pointers
        synth_prompt = (
            f"Based on the following scraped research data regarding the error:\n{scraped_data[:2000]}\n\n"
            f"Provide concrete pointers on how to fix the python code to resolve '{error_msg}'."
        )
        pointers = await hybrid_router.execute_query([{"role": "user", "content": synth_prompt}], complexity=0.7)

        return pointers
