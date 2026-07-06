from sqlalchemy import BigInteger, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from database.base import Base

class Categories(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(25), unique=True)

    products = relationship("Products", back_populates="product_category")