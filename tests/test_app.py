import unittest

from fastapi.testclient import TestClient
from exception_app.exception_lesson_3 import app, random_digit  # включаем сюда ваш инстанс FastAPI приложения с названием "app"
from unittest.mock import patch

# создаём инстанс TestClient для тестирования FastAPI приложения
client = TestClient(app)


# def test_create_user():
#     response = client.post("/user", json={"username": "user5", "password": "pass5"})
#     assert response.status_code == 200
#     assert response.json() == {"username": "user5", "password": "pass5"}
#
#     response = client.post("/user", json={"username": "user1", "password": "pass1"})
#     assert response.status_code == 404
#     assert response.json() == "Пользователь уже существует в БД."
#
#     response = client.post("/user", json={"username": "user1", "password": 3232323})
#     assert response.status_code == 404
#     assert response.json() == "Некорректный формат вводных данных для создания пользователя."


def test_get_user():
    response = client.get("/users/user1")
    assert response.status_code == 200
    assert response.json() == {"username": "user1", "password": "pass1"}

    response = client.get("/users/user15")
    assert response.status_code == 400
    assert response.json() == 'Пользователь не найден в БД.'

    response = client.get("/users/3333315")
    assert response.status_code == 400
    assert response.json() == 'Некорректный формат входных данных пользователя.'


def test_delete_user():
    response = client.delete("/users/user1")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь успешно удален"}

    response = client.delete("/users/user15")
    assert response.status_code == 400
    assert response.json() == 'Пользователь не найден в БД.'

    response = client.delete("/users/3333315")
    assert response.status_code == 400
    assert response.json() == 'Некорректный формат входных данных пользователя.'


class TestMain(unittest.TestCase):

    @patch("exception_app.exception_lesson_3.random_digit")
    def test_get_and_process_data(self, random_digit):
        # Имитируем функцию fetch_data_from_api, чтобы вернуть пример ответа
        random_digit_response = 1
        random_digit.return_value = random_digit_response

        # отправляем запрос на конечную точку /data/
        response = client.post("/user", json={"username": "user8", "password": "pass8"})

        # наши assertions
        random_digit.assert_called_once()  # Убеждаемся, что random_digit был вызван один раз
        self.assertEqual(response.status_code, 200)  # проверяем что status code равен 200
        self.assertEqual(response.json(), {"username": "user8", "password": "pass8"})  # проверяем, что данные ответа соответствуют имитируемым обработанным данным

        random_digit_response = 0
        random_digit.return_value = random_digit_response
        response = client.post("/user", json={"username": "user9", "password": "pass9"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"username": "0", "password": "0"})

        response = client.post("/user", json={"username": "admin", "password": "adminpass"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Пользователь уже существует в БД.")
