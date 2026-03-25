from app.infraestructure.repositories.order_repository import OrderRepository
from app.infraestructure.repositories.product_repository import ProductRepository
from app.infraestructure.database.models import OrderStatus, Order
class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo : ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def start_new_order(self, client_id: int ) -> str:
            order = await self.order_repo.create_order(
                    client_id=client_id
                    )
            return f"Order #{order.id} done!, which product you want to add? (send the ID)"
    async def add_product_to_order(self, order_id: int, product_id: int, quantity: int = 1) -> str: 
            #product exist?
            product = await self.product_repo.get_product_by_id(product_id)

            if not product:
                return "invalid product ID. Please Check the menu"
            
            if product.stock < quantity:
                return f"we only have {product.stock} units of {product.name}"
            
            await self.order_repo.add_item(
                order_id=order_id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            await self.product_repo.decrease_stock_(product.id, quantity)
            return (
                 f'{quantity} x {product.name} added!\n\n '
                 'Want to add another product? Send the *ID*\n'
                 'If you are done, write *checkout* to finish your order'
            )
    async def get_active_order(self, client_id:int) -> Order | None:
         return await self.order_repo.get_order_by_status(
              client_id=client_id,
              status=OrderStatus.ORDERING
         )
#update order status
    async def checkout(self, client_id: int):
        """Transitions from ORDERING to PAID, calculates and saves total."""
        order = await self.order_repo.get_order_by_status(client_id, OrderStatus.ORDERING)
        if not order:
            return "No active cart found."
        # Calculate total: sum of quantity * price_at_time for all items
        total = sum(item.quantity * item.price_at_time for item in order.items)
        # Update order status and total atomically
        await self.order_repo.update_order_status(order.id, OrderStatus.PAID, total=total)
        return f"Order #{order.id} confirmed! Total to pay: ${total:.2f}"

    async def cancel_order(self, client_id: int) -> str:
    # Start a transaction block
        async with self.session.begin(): 
            order = await self.order_repo.get_order_by_status(client_id, OrderStatus.ORDERING)
        
        if not order:
            return "Nothing to cancel."

        # Use the ATOMIC version here
        for item in order.items:
            await self.product_repo.increase_atomic_stock(item.product_id, item.quantity)

        # Update status
        await self.order_repo.update_order_status(order.id, OrderStatus.CANCELLED)
        
    # the stock increase is ROLLED BACK automatically.
        return f"Order #{order.id} cancelled safely."
