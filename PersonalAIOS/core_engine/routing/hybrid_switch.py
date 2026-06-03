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
        # Ollama/vLLM/LMStudio support the OpenAI API spec locally.
        self.local_client = AsyncOpenAI(
            base_url=os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1"),
            api_key="local-proxy" # Required by client, ignored by most local servers
        )
        self.cloud_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "missing_key")
        )

        # Pulls specific model from environment, defaults to Qwen3 3B
        self.local_model_name = os.getenv("LOCAL_MODEL_NAME", "qwen3:3b")
        self.cloud_model_name = os.getenv("CLOUD_MODEL_NAME", "gpt-4o")

    async def execute_query(self, messages: list, complexity: float, response_format: dict = None) -> str:
        """
        Determines the most efficient neural pathway based on complexity score
        and executes the inference. Injects cultural persona dynamically.
        Optionally forces the LLM to output structured JSON.
        """
        from PersonalAIOS.identity_domain.localization.cultural_adapter import CulturalAdapter
        adapter = CulturalAdapter()
        messages = adapter.inject_persona(messages)

        kwargs = {"temperature": 0.7}

        # If the caller requests strict JSON output (e.g. SequentialSolver)
        if response_format:
            # OpenAI structured outputs spec
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "schema": response_format,
                    "strict": True
                }
            }

        if complexity < 0.4:
            logger.info(f"Routing to local lightweight model: {self.local_model_name}")
            try:
                # Ollama natively supports standard json-object format
                local_kwargs = {"temperature": 0.7}

                # If local model is used, we MUST inject the JSON schema string directly into the prompt
                # because local engines often ignore the strict Pydantic `json_schema` API argument.
                if response_format:
                    import json
                    local_kwargs["response_format"] = {"type": "json_object"}
                    schema_prompt = f"\n\nYou MUST return a valid JSON object matching this exact schema: {json.dumps(response_format)}"

                    # Append schema instruction to the final system prompt in the chain
                    for msg in messages:
                        if msg["role"] == "system":
                            msg["content"] += schema_prompt
                            break
                    else:
                        messages.insert(0, {"role": "system", "content": schema_prompt})

                response = await self.local_client.chat.completions.create(
                    model=self.local_model_name,
                    messages=messages,
                    **local_kwargs
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
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Cloud model execution failed: {e}")
            return "ERROR: Neural pathways severed. Both local and cloud models failed."

# Global singleton
hybrid_router = HybridSwitch()
