from databases import Database
from pydantic import BaseModel


# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql+asyncpg://ur:todo_password@localhost/todo"
# DATABASE_URL = "postgresql://ur:todo_password@localhost/todo"

database = Database(DATABASE_URL)


# Модель ToDo для валидации входных данных
class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False
