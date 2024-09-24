import asyncio
import uvicorn

from fastapi import FastAPI

from alembic_app_with_db.models.base_engine import init_models
from alembic_app_with_db.models.base_engine import database
from contextlib import asynccontextmanager
from alembic_app_with_db.routes import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(products)


if __name__ == '__main__':
    asyncio.run(init_models())
    uvicorn.run(
        "alembic_main:app",
        host='localhost',
        port=8000,
        reload=True
    )
