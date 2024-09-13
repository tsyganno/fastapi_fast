from re import match
from fastapi import FastAPI, Form, Cookie, Response, Header
from fastapi.responses import FileResponse
from typing import Annotated

from models.models import User, Feedback, UserCreate, Login_User

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

sample_user: dict = {"username": "user123", "password": "password123"}
fake_db: list[Login_User] = [Login_User(**sample_user)]
sessions: dict = {}

feedback_users = {}
list_create_user = []


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/login")
async def login(user: Login_User, response: Response):
    for person in fake_db:
        if person.username == user.username and person.password == user.password:
            session_token = 'abc123xyz456'
            sessions[session_token] = user
            response.set_cookie(key="session_token", value=session_token, httponly=True)
            return {"message": "куки установлены"}
    return {"message": "Invalid username or password"}


@app.get('/login_user')
async def user_info(session_token=Cookie()):
    user = sessions.get(session_token)
    if user:
        return user.dict()
    return {"message": "Unauthorized"}


@app.get("/product/search")
async def product_id(keyword: str, category: str = None, limit: int = 10):
    result = list(filter(lambda item: keyword.lower() in item['name'].lower(), sample_products))
    if category:
        result = list(filter(lambda item: item["category"] == category, result))
    return result[:limit]


@app.get("/product/{product_id}")
async def product_id(product_id: int):
    for el in sample_products:
        if el['product_id'] == product_id:
            return el
    return {"error": "User not found"}


@app.get("/users")
async def users(limit: int = 3):
    return dict(list(fake_users.items())[:limit])


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.post("/user")
async def user(user: User):
    if user.age >= 18:
        user.is_adult = True
    return user


@app.post("/feedback")
async def user(feedback: Feedback):
    feedback_users.setdefault(len(feedback_users) + 1, feedback)
    return {"message": f"Фитбэк принят, спасибо, {feedback.name}!"}


@app.get("/custom")
async def read_custom_message():
    return {"message": "This is a custom message!"}


@app.post("/calculate")
async def calculate(num1: int = Form(ge=0, lt=111), num2: int = Form(ge=0, lt=111)):
    print("num1 =", num1, "   num2 =", num2)
    return {"result": num1 + num2}


@app.get("/calculate")
async def root():
    return FileResponse("calculate.html")


@app.post("/create_user")
async def create_user(create_user: UserCreate):
    if create_user not in list_create_user:
        list_create_user.append(create_user)
    return create_user


@app.get("/showuser")
async def show_users():
    return {"users": users}


@app.get("/headers")
async def headers(user_agent: Annotated[str | None, Header()] = None, accept_language: Annotated[str | None, Header()] = None):
    pattern = r"[a-z][a-z]-[A-Z][A-Z],[a-z][a-z];[a-z]=[0-9]\.[0-9],[a-z][a-z];[a-z]=[0-9]\.[0-9]"
    if user_agent is None or accept_language is None or match(pattern, accept_language) is None:
        return {'error': 'необходимые заголовки отсутствуют'}
    return {"user_agent": user_agent, 'accept_language': accept_language}


#uvicorn main:app --reload