from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infraestructure.database.models import Enterprise

class EnterpriseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        async def create_enterprise(
            self, name: str, api_key: str,
              whatsapp_number: str,)-> Enterprise:
            new_enterprise = Enterprise(name=name, api_key=api_key,
                                        whatsapp_number=whatsapp_number)
            self.session.add(new_enterprise)
            await self.session.commit()
            await self.session.refresh(new_enterprise)
            return new_enterprise
        
        async def get_by_api_key(self,
                                  api_key:str) -> Enterprise | None:
            query = select(Enterprise).where(Enterprise.api_key == api_key)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
