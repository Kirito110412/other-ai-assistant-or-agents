import os
import logging
from enum import Enum
from openai import AsyncOpenAI

logger = logging.getLogger("HybridSwitch")

class LLMMode(Enum):
    CLOUD_ONLY = "cloud_only"
    LOCAL_ONLY = "local_only"
    HYBRID = "hybrid"

class HybridSwitch:
    """
    Routes tasks between local models and heavy cloud LLMs based on user configuration and task complexity.
    """
    def __init__(self, mode: LLMMode = LLMMode.HYBRID):
        self.mode = mode

        # Local client configuration (e.g., Ollama)
        self.local_client = AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama" # Required by client, ignored by Ollama
        )
        self.local_model_name = "qwen3:3b" # Default to user's preferred local model

        # Cloud client configuration
        self.cloud_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "missing_key")
        )
        self.cloud_model_name = "gpt-4o"

    def set_mode(self, new_mode: LLMMode):
        logger.info(f"LLM Routing Mode changed to: {new_mode.value}")
        self.mode = new_mode

    async def execute_query(self, messages: list, complexity: float) -> str:
        """
        Determines the most efficient neural pathway based on complexity score
        and strict user configuration.
        """
        if self.mode == LLMMode.LOCAL_ONLY:
            return await self._call_local(messages)

        elif self.mode == LLMMode.CLOUD_ONLY:
            return await self._call_cloud(messages)

        else: # HYBRID mode
            if complexity < 0.4:
                try:
                    return await self._call_local(messages)
                except Exception as e:
                    logger.warning(f"Local model failed in HYBRID mode, falling back to cloud: {e}")
                    return await self._call_cloud(messages)
            else:
                return await self._call_cloud(messages)

    async def _call_local(self, messages: list) -> str:
        logger.info(f"Executing query on local model: {self.local_model_name}")
        try:
            response = await self.local_client.chat.completions.create(
                model=self.local_model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Local model execution failed: {e}")
            raise

    async def _call_cloud(self, messages: list) -> str:
        logger.info(f"Executing query on cloud model: {self.cloud_model_name}")
        try:
            response = await self.cloud_client.chat.completions.create(
                model=self.cloud_model_name,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Cloud model execution failed: {e}")
            raise

# Global singleton
hybrid_router = HybridSwitch()
