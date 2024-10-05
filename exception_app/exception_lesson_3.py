import uvicorn
import time
import random

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
    def __init__(self, detail: str = 'Некорректный формат входных данных пользователя.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class UserExists(HTTPException):
    def __init__(self, detail: str = 'Пользователь уже существует в БД.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


USER_DATA = [
    TrueUser(**{"username": "user1", "password": "pass1"}),
    TrueUser(**{"username": "user2", "password": "pass2"}),
    TrueUser(**{"username": "admin", "password": "adminpass"})
]


app = FastAPI()


def random_digit():
    return random.random()


@app.exception_handler(UserExists)
async def user_exists(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


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
        status_code=406,
        content=f"Некорректный формат вводных данных для создания пользователя.",
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.post("/user", response_model=TrueUser)
async def create_user(user: TrueUser):
    num = random_digit()
    if user in USER_DATA:
        raise UserExists()
    if num == 1:
        USER_DATA.append(user)
        return user
    else:
        return {"username": str(num), "password": str(num)}


@app.get("/users/{username}")
async def get_user(username: str):
    if username.isalpha() or username.isdigit():
        raise InvalidUserDataException()
    for user in USER_DATA:
        if user.username == username:
            return user
    raise UserNotFoundException()


@app.delete("/users/{username}")
async def delete_user(username: str):
    if username.isalpha() or username.isdigit():
        raise InvalidUserDataException()
    for user in USER_DATA:
        if user.username == username:
            USER_DATA.remove(user)
            return {"message": "Пользователь успешно удален"}
    raise UserNotFoundException()


if __name__ == '__main__':
    uvicorn.run(
        "exception_lesson_3:app",
        host='localhost',
        port=8000,
        reload=True
    )
