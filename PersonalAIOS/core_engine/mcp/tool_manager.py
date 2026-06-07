import logging
import json
import importlib.util
import os
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class MCPToolManager:
    """
    Model Context Protocol (MCP) Manager.
    Dynamically loads plug-and-play third-party tools exactly like awesome-llm-apps.
    This allows Asta to be infinitely extensible without hardcoding skills.
    """
    def __init__(self, tools_dir="PersonalAIOS/core_engine/mcp/tools"):
        self.tools_dir = tools_dir
        self.registered_tools: Dict[str, Dict[str, Any]] = {}
        self.tool_functions: Dict[str, Callable] = {}
        os.makedirs(self.tools_dir, exist_ok=True)

    def load_all_tools(self):
        """Scans the tools directory and dynamically loads any valid MCP python tool."""
        logger.info(f"Scanning for MCP tools in {self.tools_dir}")
        for filename in os.listdir(self.tools_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                self._load_tool(filename)

    def _load_tool(self, filename: str):
        filepath = os.path.join(self.tools_dir, filename)
        module_name = filename[:-3]

        try:
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # The module must define MCP_TOOL_SCHEMA and execute_tool
                if hasattr(module, "MCP_TOOL_SCHEMA") and hasattr(module, "execute_tool"):
                    schema = module.MCP_TOOL_SCHEMA
                    tool_name = schema.get("name")

                    if tool_name:
                        self.registered_tools[tool_name] = schema
                        self.tool_functions[tool_name] = module.execute_tool
                        logger.info(f"Successfully loaded MCP tool: {tool_name}")
                else:
                    logger.warning(f"File {filename} lacks MCP_TOOL_SCHEMA or execute_tool. Skipping.")
        except Exception as e:
            logger.error(f"Failed to load tool {filename}: {e}")

    def get_all_schemas(self) -> list:
        """Returns the JSON schemas for the LLM to understand what tools exist."""
        return list(self.registered_tools.values())

    async def execute(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Executes a loaded tool based on the LLM's request."""
        if tool_name not in self.tool_functions:
            return f"Error: Tool '{tool_name}' not found."

        logger.info(f"Executing MCP Tool: {tool_name} with args: {parameters}")
        try:
            # We assume tools might be async or sync, so we handle both safely
            func = self.tool_functions[tool_name]
            import inspect
            if inspect.iscoroutinefunction(func):
                result = await func(**parameters)
            else:
                result = func(**parameters)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"MCP Tool {tool_name} failed: {e}")
            return f"Error executing {tool_name}: {e}"
