from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.enterprise_repository import EnterpriseRepository
from pydantic import BaseModel

router = APIRouter()

#scheme to get data DTO
class EnterpriseCreateDTO(BaseModel):
    name: str
    whatsapp_number: str
    api_key: str #in production this would happen automatically but for now you choose it

@router.post('/register-enterprise')
async def register_enterprise(data: EnterpriseCreateDTO,
                              db: AsyncSession = Depends(get_db)):
    repo = EnterpriseRepository(db)
    #verify if exists
    exist = await repo.get_by_api_key(data.api_key)

    if exist:
        raise HTTPException(status_code=400, detail="That API key exist")
    new = await repo.create_enterprise(data.name, data.api_key, 
                                       data.whatsapp_number)
    return {"message": "enterprise created succesfully!", "id": new.id,
            "name": new.name}

