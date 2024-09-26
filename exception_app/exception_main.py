import uvicorn

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


# пример модели ответа для успешного запроса
class ItemsResponse(BaseModel):
    item_id: int


# не изменяли
class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# не изменяли
@app.exception_handler(CustomExceptionA)
async def custom_exception_handler(request: Request, exc: CustomExceptionA):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_CustomExceptionA": exc.detail}
    )


# не изменяли
@app.exception_handler(CustomExceptionB)
async def custom_exception_handler(request: Request, exc: CustomExceptionB):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_CustomExceptionB": exc.detail}
    )


# Обработчик глобальных исключений, который "ловит" все необработанные исключения
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Деление на ноль!!!"}
    )


# добавили непредусмотренное исключение
@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id == 1:
        raise CustomExceptionA(status_code=420, detail="item_id равен 1")
    if item_id == 2:
        raise CustomExceptionB(status_code=440, detail="item_id равен 2")
    # симулируем непредусмотренное исключение
    if item_id == 3:
        result = 1 / 0
    return ItemsResponse(item_id=item_id)


if __name__ == '__main__':
    uvicorn.run(
        "exception_main:app",
        host='localhost',
        port=8000,
        reload=True
    )