import logging
from fastapi import APIRouter, Request

logger = logging.getLogger("WhatsAppGateway")
whatsapp_router = APIRouter()

@whatsapp_router.post("/webhook/whatsapp")
async def receive_whatsapp_message(request: Request):
    """
    Receives incoming webhooks from Twilio/WhatsApp Business API.
    Routes the message to the EventBus so the AI can process it remotely.
    """
    data = await request.json()
    # In a full implementation, we parse the body, ensure the sender is the User,
    # and push the command to the Central Nervous System.
    logger.info("Received remote command via WhatsApp Gateway.")
    return {"status": "received"}
