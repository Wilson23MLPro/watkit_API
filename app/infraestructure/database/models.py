from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, Text, Float, Integer, Boolean,Enum
from datetime import datetime
from typing import List
from sqlalchemy import UniqueConstraint
import enum 
from sqlalchemy import Numeric

#create a class enum to immutable constants
class OrderStatus(enum.Enum):
    ORDERING = "ordering"
    PENDING = "pending"
    PAID = "paid"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
class ClientStatus(enum.Enum):
    BEGIN = "begin"
    BROWSING = "browsing"
    ORDERING = "ordering"
    WAITING = "waiting"

#The standard way to define model classes mapped to database using ORM
#SQLalchemy
class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    wa_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50), index=True)

    email: Mapped[str | None] = mapped_column(String(80), unique=True, index=True)
    register_date: Mapped[datetime] = mapped_column(server_default=func.now())

    status: Mapped[ClientStatus] = mapped_column(
        Enum(ClientStatus), default=ClientStatus.BEGIN
    )
    
    #one to many relationship
    messages: Mapped[List["Message"]] = relationship(back_populates="client")
    orders: Mapped[list["Order"]] = relationship(back_populates="client")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    is_from_user: Mapped[bool] = mapped_column(Boolean) # True=Client, False=Bot
    message_date: Mapped[datetime] = mapped_column(server_default=func.now())
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    client: Mapped["Client"] = relationship(back_populates="messages")
    is_scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime)
    send_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=None, onupdate=func.now())

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str | None] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=1)

    __table_args__ = (
    UniqueConstraint("name", "brand", name="uq_product_name_brand"),
    )

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    order_date: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.ORDERING
    )
    client: Mapped["Client"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")
    total: Mapped[float] = mapped_column(Numeric(10, 2), default=0)

class OrderItem(Base):
    __tablename__ = "order_items"

    id:Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price_at_time: Mapped[float] = mapped_column(Float)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()
    
 