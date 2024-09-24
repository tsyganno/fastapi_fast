from sqlalchemy.ext.asyncio import AsyncSession
from alembic_app_with_db.models.models import *


def add_product(session: AsyncSession, title: str, price: int, count: int, description: str):
    new_product = Product(title=title, price=price, count=count, description=description)
    session.add(new_product)
    return new_product
