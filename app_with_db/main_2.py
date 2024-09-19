import uvicorn

from fastapi import FastAPI, HTTPException

from app_with_db.models.models import database, TodoCreate

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


# создание роута для создания дела
@app.post("/todos")
async def create_todo(todo: TodoCreate):
    query = "INSERT INTO todo (id, title, description, completed) VALUES (nextval('todo_id_sec'), :title, :description, :completed) RETURNING id"
    values = {"title": todo.title, "description": todo.description, "completed": todo.completed}
    try:
        todo_id = await database.execute(query=query, values=values)
        return {**todo.dict(), "id": todo_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create todo")


# маршрут для получения информации о деле по ID
@app.get("/todo/{todo_id}")
async def get_todo(todo_id: int):
    query = "SELECT * FROM todo WHERE id = :todo_id"
    values = {"todo_id": todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to fetch todo from database")
    if result:
        return TodoCreate(title=result["title"], description=result["description"], completed=result["completed"])
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# роут для обновления информации о деле по ID
@app.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo: TodoCreate):
    query = "SELECT * FROM todo WHERE id = :todo_id"
    values = {"todo_id": todo_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to fetch todo from database")
    if result:
        query = "UPDATE todo SET title = :title, description = :description, completed = :completed WHERE id = :todo_id"
        values = {"todo_id": todo_id, "title": todo.title, "description": todo.description, "completed": todo.completed}
        try:
            await database.execute(query=query, values=values)
            return {**todo.dict(), "id": todo_id}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Failed to update todo in database")
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# роут для удаления информации о деле по ID
@app.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int):
    query = "DELETE FROM todo WHERE id = :todo_id RETURNING id"
    values = {"todo_id": todo_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to delete todo from database")
    if deleted_rows:
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


if __name__ == '__main__':
    uvicorn.run(
        "main_2:app",
        host='localhost',
        port=8000,
        reload=True
    )
