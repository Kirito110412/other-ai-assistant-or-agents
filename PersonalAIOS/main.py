import asyncio
import threading
import uvicorn
import logging
from PersonalAIOS.interfaces.onboarding.profile_generator import ProfileGenerator
from PersonalAIOS.interfaces.native_ui.desktop_avatar import HolographicAvatar
from PersonalAIOS.interfaces.web_ui.dashboard import app as fastapi_app
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PersonalAIOS_Bootloader")

def run_fastapi_server():
    """Runs the Web UI and Remote Gateways in a background thread."""
    logger.info("Starting Web Dashboard and Omni-Channel Gateways on port 8000...")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="warning")

def run_background_event_loop(loop):
    """Runs the core nervous system and async background tasks."""
    asyncio.set_event_loop(loop)
    logger.info("Core Async Event Loop started.")
    loop.run_forever()

def main():
    logger.info("=== PersonalAIOS Boot Sequence Initiated ===")

    # 1. Onboarding check (Synchronous)
    generator = ProfileGenerator()
    generator.start_onboarding()

    # 2. Setup Async Core (Background Thread)
    # This prevents the async OS operations from blocking the macOS GUI thread
    core_loop = asyncio.new_event_loop()
    threading.Thread(target=run_background_event_loop, args=(core_loop,), daemon=True).start()

    # 3. Setup FastAPI Server (Background Thread)
    threading.Thread(target=run_fastapi_server, daemon=True).start()

    # 4. Start Native UI (Main Thread)
    # macOS strictly requires GUI toolkits (Tkinter/rumps) to run on the main thread.
    logger.info("Initializing Holographic Avatar on Main GUI Thread...")
    avatar = HolographicAvatar()
    # Replace the previous threading logic in desktop_avatar.py to run natively here
    avatar.start_overlay()

if __name__ == "__main__":
    main()
