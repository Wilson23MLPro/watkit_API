from app.infraestructure.repositories.order_repository import OrderRepository
from app.infraestructure.repositories.product_repository import ProductRepository

class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo : ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

        async def start_new_order(self, client_id: int ) -> str:
            order = await self.order_repo.create_order(client_id)
            return f"Order #{order.id} done!, which product you want to add?"
        async def add_product_to_order(self, order_id: int, product_id: int, quantity: int = 1) -> int: 
            #product exist?
            product = await self.product_repo.get_product(product_id)

            if not product:
                return "invalid product"
            
            if product.stock < quantity:
                return f"we only have {product.stock} units of {product.name}"
            
            await self.order_repo.add_item(
                order_id = order_id,
                product = product, 
                quantity = quantity,
                price = product.price
            )
            await self.product_repo.decrease_stock(product.id, quantity)
            return f"{quantity}: {product.name} in your order"