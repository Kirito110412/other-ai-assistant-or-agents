import logging
from fastapi import APIRouter, Request

logger = logging.getLogger("TelegramGateway")
telegram_router = APIRouter()

@telegram_router.post("/webhook/telegram")
async def receive_telegram_message(request: Request):
    """
    Receives incoming webhooks from Telegram Bot API.
    Routes the message to the EventBus.
    """
    data = await request.json()
    logger.info("Received remote command via Telegram Gateway.")
    return {"status": "received"}
