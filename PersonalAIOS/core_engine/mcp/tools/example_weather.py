"""
An example plug-and-play MCP tool to demonstrate the architecture.
"""

MCP_TOOL_SCHEMA = {
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}

async def execute_tool(location: str, unit: str = "fahrenheit"):
    # In reality, this would call an external API
    return {"location": location, "temperature": "72", "unit": unit, "forecast": "Sunny"}
