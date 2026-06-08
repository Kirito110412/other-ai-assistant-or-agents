from fastapi import FastAPI
from asta.interfaces.gateways.whatsapp_gateway import whatsapp_router
from asta.interfaces.gateways.telegram_gateway import telegram_router
from asta.core_engine.goals.domain_spawner import fleet_manager

app = FastAPI(title="Asta Omni-Channel Interface")

# Register Remote Gateways
app.include_router(whatsapp_router, prefix="/api/v1")
app.include_router(telegram_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Asta is online and listening on all channels."}

@app.get("/api/v1/fleet")
def get_fleet_org_chart():
    """
    Returns the live Org-Chart, tracking the CEO (Asta) and all active
    sub-agents (CTO, Marketer) alongside their strict LLM budget usage.
    This provides frontend parity with Paperclip's management UI.
    """
    return fleet_manager.get_org_chart()
