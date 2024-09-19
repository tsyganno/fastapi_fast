import asyncio
import uvicorn

from fastapi import FastAPI

from async_app_with_db.models.async_base import init_models
from async_app_with_db.models.async_base import database
from contextlib import asynccontextmanager
from async_app_with_db.models.routes import todos


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(todos)


if __name__ == '__main__':
    asyncio.run(init_models())
    uvicorn.run(
        "async_main:app",
        host='localhost',
        port=8000,
        reload=True
    )
