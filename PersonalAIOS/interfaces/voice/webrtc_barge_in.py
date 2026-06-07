import asyncio
import logging
import json

logger = logging.getLogger(__name__)

class WebRTCBargeIn:
    """
    Handles WebRTC signaling and audio stream processing for low-latency barge-in.
    Allows the user to interrupt the AI's speech dynamically.
    """
    def __init__(self, logic_engine_callback=None):
        self.pcs = set()
        self.logic_engine_callback = logic_engine_callback

    async def offer(self, sdp: str, type: str):
        try:
            from aiortc import RTCPeerConnection, RTCSessionDescription
            from aiortc.contrib.media import MediaRecorder
        except ImportError:
            logger.error("aiortc is not installed. WebRTC unavailable.")
            return json.dumps({"error": "aiortc not installed"})

        offer = RTCSessionDescription(sdp, type)
        pc = RTCPeerConnection()
        self.pcs.add(pc)

        # Setup an audio recorder for barge in VAD processing
        recorder = MediaRecorder("/tmp/webrtc_incoming.wav")

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info("Connection state is %s", pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                self.pcs.discard(pc)

        @pc.on("track")
        def on_track(track):
            logger.info("Track %s received", track.kind)
            if track.kind == "audio":
                recorder.addTrack(track)
                asyncio.create_task(recorder.start())

                # Here we simulate triggering a barge-in event.
                # In production, we'd run real-time VAD over the stream chunks.
                if self.logic_engine_callback:
                    # Async task to simulate VAD hit and stop Asta speaking
                    asyncio.create_task(self._simulate_barge_in_detection())

            @track.on("ended")
            async def on_ended():
                logger.info("Track %s ended", track.kind)
                await recorder.stop()

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })

    async def _simulate_barge_in_detection(self):
        """Simulates VAD detecting user speech mid-AI-response"""
        await asyncio.sleep(2.0)
        logger.warning("VAD BARGE-IN DETECTED! INTERRUPTING...")
        await self.logic_engine_callback({"action": "interrupt", "timestamp": asyncio.get_event_loop().time()})

    async def close_all(self):
        coros = [pc.close() for pc in self.pcs]
        await asyncio.gather(*coros)
        self.pcs.clear()
