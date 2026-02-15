from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository
from app.domain.services.message_service import MessageService

router = APIRouter()

@router.post("/validate-client/{wat_id}")
async def validate_client(wa_id:str, name:str, db:AsyncSession= Depends(get_db)):
    #instanciamos el repositorio con la sesion de la BD
    repo = ClientRepository(db)
    #se lo pasamos al servicio(inyeccion de dependencias)
    service = MessageService(repo)

    #call business logic
    result = await service.process_message(wa_id, name, "first register")

    return {"status": "ok", "bot response": result}