import uvicorn

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel, conint, EmailStr, constr

app = FastAPI()


class User(BaseModel):
    """Модель пользователя."""
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'


async def custom_http_exception_handler(request, exc):
    """Кастомный обработчик исключения для всех HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Custom HTTP Exception", "error": str(exc)},
    )


async def custom_request_validation_exception_handler(request, exc):
    """Кастомный обработчик исключения для RequestValidationError."""
    return JSONResponse(
        status_code=422,
        content={
            "message": "Custom Request Validation Error Дядя Дима",
            "errors": exc.errors()
        },
    )


app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_request_validation_exception_handler)


@app.post("/users", response_model=User)
async def create_user(user: User):
    return user


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id > 5:
        raise HTTPException(status_code=404, detail="ID пользователя больше 5...")
    return {"user": user_id}


if __name__ == '__main__':
    uvicorn.run(
        "exception_name_lesson_2:app",
        host='localhost',
        port=8000,
        reload=True
    )
