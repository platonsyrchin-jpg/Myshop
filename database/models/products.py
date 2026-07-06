from sqlalchemy import BigInteger, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.models.categories import Categories
from database.base import Base

class Products(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(DECIMAL(10,2))

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    product_category: Mapped[Categories] = relationship(back_populates='products')

