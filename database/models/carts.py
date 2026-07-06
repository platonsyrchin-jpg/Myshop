from sqlalchemy import BigInteger, String, DECIMAL, ForeignKey
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .users import Users
from database.base import Base


class Carts(Base):
    __tablename__ = 'carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    total_price: Mapped[int] = mapped_column(DECIMAL(10, 2), default=0)
    total_products: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    user_cart: Mapped['Users'] = relationship(back_populates='carts')
    finally_id: Mapped[int] = relationship('FinallyCarts', back_populates='user_cart')


class FinallyCarts(Base):
    __tablename__ = 'finally_carts'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product_name: Mapped[str] = mapped_column(String(35))
    final_price: Mapped[int] = mapped_column(DECIMAL(10, 2))
    quantity: Mapped[int]

    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))

    user_cart: Mapped['Carts'] = relationship(back_populates='finally_id')

    __table_args__ = (
        {'sqlite_autoincrement'}
    )
