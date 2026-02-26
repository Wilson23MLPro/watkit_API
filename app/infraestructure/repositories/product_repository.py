from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infraestructure.database.models import Product

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

        async def get_product_by_id(self, product_id:int) -> Product | None:
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        async def get_available_products(self):
            query = select(Product).where(Product.stock > 0)
            result = await self.session.execute(query)
            return result.scalars().all()
        async def decrease_stock(self, product_id: int, quantity: int) -> bool:
            #find product
            query = select(Product).where(Product.id == product_id)
            result = await self.session.execute(query)
            product = result.scalar_one_or_none()

            if not product or product.stock < quantity:
                return False
            
            product.stock -= quantity

            self.session.add(product)
            await self.session.commit()
            return True
        


        
        
        