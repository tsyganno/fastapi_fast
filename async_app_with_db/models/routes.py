from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from async_app_with_db.models.async_base import get_session
from async_app_with_db.models import service


class TodoSchema(BaseModel):
    title: str
    description: str
    completed: bool = False


todos = APIRouter()


@todos.post("/async/todo")
async def add_todo(todo: TodoSchema, session: AsyncSession = Depends(get_session)):
    try:
        todo = service.add_todo(session, todo.title, todo.description, todo.completed)
        await session.commit()
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось создать задачу.")


@todos.get("/async/todo/{todo_id}")
async def get_todo(todo_id: int, session: AsyncSession = Depends(get_session)):
    try:
        todo = await service.get_todo(session, todo_id)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось получить задачу из базы данных.")


@todos.put("/async/todo/{todo_id}")
async def update_todo(todo_id: int, todo: TodoSchema, session: AsyncSession = Depends(get_session)):
    try:
        todo = await service.update_todo(session, todo_id, title=todo.title, description=todo.description, completed=todo.completed)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось обновить задачу из базы данных.")


@todos.delete("/async/todo/{todo_id}")
async def delete_todo(todo_id: int,  session: AsyncSession = Depends(get_session)):
    try:
        await service.delete_todo(session, todo_id)
        return {"message": "Запись успешно удалена."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Не удалось удалить задачу из базы данных.")
