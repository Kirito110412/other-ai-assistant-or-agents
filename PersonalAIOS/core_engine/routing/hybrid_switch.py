import os
import logging
from openai import AsyncOpenAI

logger = logging.getLogger("HybridSwitch")

class HybridSwitch:
    """
    Instantly routes tasks between local models (Ollama/vLLM) and heavy cloud LLMs.
    """
    def __init__(self):
        # We use the OpenAI client library as a universal interface.
        # Ollama supports the OpenAI API spec locally on port 11434.
        self.local_client = AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama" # Required by client, ignored by Ollama
        )
        self.cloud_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "missing_key")
        )

        self.local_model_name = "llama3" # Replace with actual 3B model like phi3
        self.cloud_model_name = "gpt-4o"

    async def execute_query(self, messages: list, complexity: float) -> str:
        """
        Determines the most efficient neural pathway based on complexity score
        and executes the inference.
        """
        if complexity < 0.4:
            logger.info(f"Routing to local lightweight model: {self.local_model_name}")
            try:
                response = await self.local_client.chat.completions.create(
                    model=self.local_model_name,
                    messages=messages,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Local model failed or offline, falling back to cloud: {e}")
                # Fallthrough to cloud logic

        logger.info(f"Routing to massive cloud model: {self.cloud_model_name}")
        try:
            response = await self.cloud_client.chat.completions.create(
                model=self.cloud_model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Cloud model execution failed: {e}")
            return "ERROR: Neural pathways severed. Both local and cloud models failed."

# Global singleton
hybrid_router = HybridSwitch()
