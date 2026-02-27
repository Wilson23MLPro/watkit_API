from fastapi import FastAPI
from app.api.v1.endpoints import clients
from app.infraestructure.database.config import engine
from app.infraestructure.database.models import Base
from app.api.v1.endpoints import clients, webhook
app = FastAPI(title="WhatsApp Messaging API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(clients.router, prefix="/api/v1", tags=["Clients"])
app.include_router(webhook.router, prefix="/api/v1/webhook", tags=["Webhook Twilio"])

@app.get("/")
def read_root():
    return {"message": "API de WhatsApp Activa v1.0"}

