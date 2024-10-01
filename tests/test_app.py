from fastapi.testclient import TestClient
from exception_app.exception_lesson_3 import app  # включаем сюда ваш инстанс FastAPI приложения с названием "app"

# создаём инстанс TestClient для тестирования FastAPI приложения
client = TestClient(app)


def test_create_user():
    response = client.post("/user", json={"username": "user5", "password": "pass5"})
    assert response.status_code == 200
    assert response.json() == {"username": "user5", "password": "pass5"}

    response = client.post("/user", json={"username": "user1", "password": "pass1"})
    assert response.status_code == 404
    assert response.json() == "Пользователь уже существует в БД."

    response = client.post("/user", json={"username": "user1", "password": 3232323})
    assert response.status_code == 404
    assert response.json() == "Некорректный формат вводных данных для создания пользователя."


def test_get_user():
    response = client.get("/users/user1")
    assert response.status_code == 200
    assert response.json() == {"username": "user1", "password": "pass1"}

    response = client.get("/users/user15")
    assert response.status_code == 404
    assert response.json() == 'Пользователь не найден в БД.'

    response = client.get("/users/3333315")
    assert response.status_code == 400
    assert response.json() == 'Некорректный формат входных данных пользователя.'


def test_delete_user():
    response = client.delete("/users/user1")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь успешно удален"}

    response = client.delete("/users/user15")
    assert response.status_code == 404
    assert response.json() == 'Пользователь не найден в БД.'

    response = client.delete("/users/3333315")
    assert response.status_code == 400
    assert response.json() == 'Некорректный формат входных данных пользователя.'
