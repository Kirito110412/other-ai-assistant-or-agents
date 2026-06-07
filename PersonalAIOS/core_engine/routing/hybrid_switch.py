import os
import logging
import json
from enum import Enum
from openai import AsyncOpenAI
from ..mcp.tool_manager import MCPToolManager

logger = logging.getLogger("HybridSwitch")

class LLMMode(Enum):
    CLOUD_ONLY = "cloud_only"
    LOCAL_ONLY = "local_only"
    HYBRID = "hybrid"

class HybridSwitch:
    """
    Routes tasks between local models and heavy cloud LLMs based on user configuration and task complexity.
    Now supports Model Context Protocol (MCP) tool execution.
    """
    def __init__(self, mode: LLMMode = LLMMode.HYBRID):
        self.mode = mode
        self.mcp_manager = MCPToolManager()
        self.mcp_manager.load_all_tools()

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
        tools = self.mcp_manager.get_all_schemas()
        # If no tools, we don't pass the parameter to avoid API errors
        tool_kwargs = {"tools": tools} if tools else {}

        if self.mode == LLMMode.LOCAL_ONLY:
            return await self._call_local(messages, tool_kwargs)

        elif self.mode == LLMMode.CLOUD_ONLY:
            return await self._call_cloud(messages, tool_kwargs)

        else: # HYBRID mode
            if complexity < 0.4:
                try:
                    return await self._call_local(messages, tool_kwargs)
                except Exception as e:
                    logger.warning(f"Local model failed in HYBRID mode, falling back to cloud: {e}")
                    return await self._call_cloud(messages, tool_kwargs)
            else:
                return await self._call_cloud(messages, tool_kwargs)

    async def _handle_tool_calls(self, response_message, client, model_name, messages, tool_kwargs):
        """Recursively handles MCP tool execution if the LLM requests it."""
        if not response_message.tool_calls:
            return response_message.content

        messages.append(response_message.model_dump())

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # Execute the dynamically loaded MCP tool
            tool_response = await self.mcp_manager.execute(function_name, function_args)

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_response,
                }
            )

        # Re-query the LLM with the tool results
        second_response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            **tool_kwargs
        )
        return second_response.choices[0].message.content

    async def _call_local(self, messages: list, tool_kwargs: dict) -> str:
        logger.info(f"Executing query on local model: {self.local_model_name}")
        try:
            response = await self.local_client.chat.completions.create(
                model=self.local_model_name,
                messages=messages,
                temperature=0.7,
                **tool_kwargs
            )
            response_message = response.choices[0].message

            if hasattr(response_message, "tool_calls") and response_message.tool_calls:
                return await self._handle_tool_calls(response_message, self.local_client, self.local_model_name, messages, tool_kwargs)

            return response_message.content
        except Exception as e:
            logger.error(f"Local model execution failed: {e}")
            raise

    async def _call_cloud(self, messages: list, tool_kwargs: dict) -> str:
        logger.info(f"Executing query on cloud model: {self.cloud_model_name}")
        try:
            response = await self.cloud_client.chat.completions.create(
                model=self.cloud_model_name,
                messages=messages,
                temperature=0.7,
                **tool_kwargs
            )
            response_message = response.choices[0].message

            if hasattr(response_message, "tool_calls") and response_message.tool_calls:
                return await self._handle_tool_calls(response_message, self.cloud_client, self.cloud_model_name, messages, tool_kwargs)

            return response_message.content
        except Exception as e:
            logger.error(f"Cloud model execution failed: {e}")
            raise

# Global singleton
hybrid_router = HybridSwitch()
