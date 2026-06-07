import logging
import json
from mcrcon import MCRcon

logger = logging.getLogger(__name__)

MCP_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "minecraft_execute_commands",
        "description": "Executes a batch of Minecraft server commands via RCON. Useful for building structures, redstone logic, and visual computer science representations.",
        "parameters": {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "A list of Minecraft commands to execute (e.g., ['/setblock ~ ~1 ~ stone', '/fill 0 64 0 10 64 10 redstone_block'])"
                },
                "host": {
                    "type": "string",
                    "description": "The RCON host IP (default: 127.0.0.1)"
                },
                "port": {
                    "type": "integer",
                    "description": "The RCON port (default: 25575)"
                },
                "password": {
                    "type": "string",
                    "description": "The RCON password"
                }
            },
            "required": ["commands", "password"],
        }
    }
}

async def execute_tool(commands: list, password: str, host: str = "127.0.0.1", port: int = 25575):
    """
    Connects to the local Minecraft Server via RCON and executes building commands.
    Works on both Premium and Cracked (offline-mode=true) servers as long as RCON is enabled in server.properties.
    """
    logger.info(f"Connecting to Minecraft Server at {host}:{port}")
    results = []

    try:
        # We use standard synchronous MCRcon, so we don't await the connection itself
        with MCRcon(host, password, port=port) as mcr:
            for cmd in commands:
                # Ensure commands don't have leading slashes for RCON
                clean_cmd = cmd.lstrip('/')
                resp = mcr.command(clean_cmd)
                results.append({"command": clean_cmd, "response": resp})

        return {"status": "success", "executed_commands": len(commands), "results": results}
    except ConnectionRefusedError:
        return {"status": "error", "message": f"Connection refused. Ensure the Minecraft server is running and RCON is enabled on port {port}."}
    except Exception as e:
        logger.error(f"Minecraft RCON Error: {e}")
        return {"status": "error", "message": str(e)}
