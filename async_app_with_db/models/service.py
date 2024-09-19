from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from async_app_with_db.models.async_models import *

from sqlalchemy import update, delete


async def get_todo(session: AsyncSession, id_todo):
    result = await session.execute(select(Todo).where(Todo.id == id_todo))
    return result.scalars().all()


def add_todo(session: AsyncSession, title: str, description: str, completed: bool):
    new_todo = Todo(title=title, description=description, completed=completed)
    session.add(new_todo)
    return new_todo


async def update_todo(session: AsyncSession, id_todo: int, title: str, description: str, completed: bool):
    up_todo = update(Todo).where(Todo.id == id_todo).values(title=title, description=description, completed=completed)
    await session.execute(up_todo)
    await session.commit()
    result = await session.execute(select(Todo).where(Todo.id == id_todo))
    return result.scalars().all()


async def delete_todo(session: AsyncSession, id_todo: int):
    obj = delete(Todo).where(Todo.id == id_todo)
    await session.execute(obj)
    await session.commit()
