import asyncio
import threading
import uvicorn
import logging
from PersonalAIOS.interfaces.onboarding.profile_generator import ProfileGenerator
from PersonalAIOS.interfaces.native_ui.avatar_websocket import AvatarWebSocketServer
from PersonalAIOS.interfaces.web_ui.dashboard import app as fastapi_app
from PersonalAIOS.core_engine.orchestrator.event_bus import nervous_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PersonalAIOS_Bootloader")

def run_fastapi_server():
    """Runs the Web UI and Remote Gateways in a background thread."""
    logger.info("Starting Web Dashboard and Omni-Channel Gateways on port 8000...")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="warning")

def run_background_event_loop(loop):
    """Runs the core nervous system, passive senses, and async background tasks."""
    asyncio.set_event_loop(loop)
    logger.info("Core Async Event Loop started.")

    # Initialize and start Passive Senses
    from PersonalAIOS.actuation_sensory.passive.screen_listener import ScreenListener
    from PersonalAIOS.actuation_sensory.passive.audio_listener import AudioListener

    screen_listener = ScreenListener()
    audio_listener = AudioListener()

    # Toggle them ON by default (user can configure via Dashboard later)
    screen_listener.toggle(True)
    audio_listener.toggle(True)

    # Initialize Avatar WebSocket Server
    avatar_server = AvatarWebSocketServer()

    # Schedule the infinite listening loops and WebSocket Server on the event loop
    loop.create_task(screen_listener.listen_loop())
    loop.create_task(audio_listener.listen_loop())
    loop.create_task(avatar_server.start_server())

    loop.run_forever()

def main():
    logger.info("=== PersonalAIOS Boot Sequence Initiated ===")

    # 1. Onboarding check (Synchronous)
    generator = ProfileGenerator()
    generator.start_onboarding()

    # 2. Setup Async Core (Main Thread)
    # Since we removed Tkinter, the Async Core can now safely run on the main thread,
    # which is significantly more stable for cross-platform event loops.
    core_loop = asyncio.new_event_loop()

    # 3. Setup FastAPI Server (Background Thread)
    threading.Thread(target=run_fastapi_server, daemon=True).start()

    # 4. Run Core Loop
    run_background_event_loop(core_loop)

if __name__ == "__main__":
    main()
