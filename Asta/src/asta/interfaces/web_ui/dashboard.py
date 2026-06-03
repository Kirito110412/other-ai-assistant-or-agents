from fastapi import FastAPI
from asta.interfaces.gateways.whatsapp_gateway import whatsapp_router
from asta.interfaces.gateways.telegram_gateway import telegram_router

app = FastAPI(title="Asta Omni-Channel Interface")

# Register Remote Gateways
app.include_router(whatsapp_router, prefix="/api/v1")
app.include_router(telegram_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Asta is online and listening on all channels."}

# Placeholder for Local UI Websocket endpoints to handle real-time streaming
