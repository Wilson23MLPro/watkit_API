#this is to comunicate to the twilio api

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository
from app.domain.services.message_service import MessageService

router = APIRouter()

@router.post("/twilio")
async def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    ProfileName:str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    wa_id = From.replace("whatsapp:", "")

    client_repo = ClientRepository(session=db)
    message_service = MessageService(client_repo)

    bot_response = await message_service.process_messsage(
        wa_id=wa_id,
        first_name=ProfileName or "user",
        last_name="", #we leave this empty for now
        text=Body
    )

    print(f"bot response for {wa_id}: {bot_response}")
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>{bot_response}</Message>
    </Response>
    """
    
    return Response(content=xml_response, media_type="application/xml")