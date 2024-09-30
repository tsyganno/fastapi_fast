import uvicorn
import time

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class TrueUser(BaseModel):
    """Модель пользователя."""
    username: str
    password: str


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = 'Пользователь не найден в БД.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class InvalidUserDataException(HTTPException):
    def __init__(self, detail: str = 'Некорректный формат входных данных пользователя.', status_code: int = 404):
        super().__init__(detail=detail, status_code=status_code)


USER_DATA = [
    TrueUser(**{"username": "user1", "password": "pass1"}),
    TrueUser(**{"username": "user2", "password": "pass2"}),
    TrueUser(**{"username": "admin", "password": "adminpass"})
]


app = FastAPI()


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_exception(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=404,
        content=f'Некорректный формат вводных данных для создания пользователя. Информация: {exc}',
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.post("/user", response_model=TrueUser)
async def create_user(user: TrueUser):
    USER_DATA.append(user)
    return user


@app.get("/users/{username}")
async def get_user(username: str):
    if not username.isalpha():
        raise InvalidUserDataException()
    for user in USER_DATA:
        if user.username == username:
            return user
    raise UserNotFoundException()


if __name__ == '__main__':
    uvicorn.run(
        "exception_lesson_3:app",
        host='localhost',
        port=8000,
        reload=True
    )
