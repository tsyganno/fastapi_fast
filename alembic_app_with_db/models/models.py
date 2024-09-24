from sqlalchemy import Column, String, BigInteger, Integer

from alembic_app_with_db.models.base_engine import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    title = Column(String)
    price = Column(Integer, default=100)
    count = Column(Integer, default=0)
    description = Column(String, nullable=True)
