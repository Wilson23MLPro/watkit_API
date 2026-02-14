#config.py is for asyncronus conection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./whatsapp_api.db"

engine = create_async_engine(DATABASE_URL, echo=True)#echo=True show queryes on console

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

#funcion para obtener la sesion dependency injection en fastapi
async def get_db():
    async with SessionLocal() as session:
        yield session
        