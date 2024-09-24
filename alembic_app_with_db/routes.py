from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from alembic_app_with_db.models.base_engine import get_session
from alembic_app_with_db.models import db_manager


class ProductSchema(BaseModel):
    title: str
    price: int = 100
    count: int = 0
    description: str


products = APIRouter()


@products.post("/alembic/product")
async def add_product(product: ProductSchema, session: AsyncSession = Depends(get_session)):
    print(product)
    try:
        product = db_manager.add_product(session, product.title, product.price, product.count, product.description)
        await session.commit()
        return product
    except Exception as e:
        print('lol')
        print(e)
        raise HTTPException(status_code=500, detail="Не удалось создать продукт.")