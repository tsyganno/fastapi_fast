import uvicorn
import jwt
from re import match
from fastapi import FastAPI, Form, Cookie, Response, Header, Depends, status, HTTPException
from fastapi.responses import FileResponse
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from models.models import User, Feedback, UserCreate, Login_User, TrueUser

app = FastAPI()
security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

USER_DATA = [TrueUser(**{"username": "user1", "password": "pass1"}), TrueUser(**{"username": "user2", "password": "pass2"}), TrueUser(**{"username": "admin", "password": "adminpass"})]

USERS_DATA = [{"username": "admin", "password": "adminpass", "role": "admin"}, {"username": "user", "password": "userpass", "role": "user"}, {"username": "guest", "password": "guestpass", "role": "guest"}]
# def get_user_from_db(username: str):
#     for user in USER_DATA:
#         if user.username == username:
#             return user
#     return None
#
#
# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = get_user_from_db(credentials.username)
#     if user is None or user.password != credentials.password:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect data")
#     return user

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(seconds=30)


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    data.update({"exp": datetime.utcnow() + EXPIRATION_TIME})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM) # кодируем токен, передавая в него наш словарь с тем, что мы хотим там разместить


# Функция получения User'а по токену
def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        return payload.get("sub") # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания' и другое, что мы сами туда кладем
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired") # тут какая-то логика ошибки истечения срока действия токена
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token") #тут какая-то логика обработки ошибки декодирования токена


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None


def authenticate_user(username: str, password: str) -> bool:
    for user in USERS_DATA:
        if user["username"] == username:
            if user.get("username") == username and user.get("password") == password:
                return True
    return False


@app.get("/")
async def root():
    return FileResponse("app/index.html")


# Роут для получения JWT-токена (так работает логин)
@app.post("/token")
def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]): # тут логинимся через форму
    user_data_from_db = get_user(user_data.username)
    if user_data_from_db is None or user_data.password != user_data_from_db['password']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_jwt_token({"sub": user_data.username})} # тут мы добавляем полезную нагрузку в токен, и говорим, что "sub" содержит значение username


# Защищенный роут для админов, когда токен уже получен
@app.get("/admin")
def get_admin_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data['role'] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Welcome Admin!"}


# Защищенный роут для обычных пользователей, когда токен уже получен
@app.get("/user")
def get_user_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data['role'] != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Hello User!"}


@app.get("/guest")
def get_guest_info(current_user: str = Depends(get_user_from_token)):
    user_data = get_user(current_user)
    if user_data['role'] != "guest":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return {"message": "Hello Guest!"}



# # роут для аутентификации; так делать не нужно, это для примера - более корректный пример в следующем уроке
# @app.post("/login")
# async def login(user_in: TrueUser):
#     if authenticate_user(user_in.username, user_in.password):
#         return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
#     return {"error": "Invalid credentials"}
#
#
# # защищенный роут для получения информации о пользователе
# @app.get("/protected_resource")
# async def protected_resource(current_user: str = Depends(get_user_from_token)):
#     user = get_user(current_user)
#     if user:
#         return user
#     return {"error": "User not found"}


# @app.get("/protected_resource/")
# async def get_protected_resource(user: TrueUser = Depends(authenticate_user)):
#     return {"message": "You got my secret, welcome!", "user_info": user}
#
#
# @app.post("/login")
# async def login(user: Login_User, response: Response):
#     for person in fake_db:
#         if person.username == user.username and person.password == user.password:
#             session_token = 'abc123xyz456'
#             sessions[session_token] = user
#             response.set_cookie(key="session_token", value=session_token, httponly=True)
#             return {"message": "куки установлены"}
#     return {"message": "Invalid username or password"}
#
#
# @app.get('/login_user')
# async def login_user(session_token=Cookie()):
#     user = sessions.get(session_token)
#     if user:
#         return user.dict()
#     return {"message": "Unauthorized"}


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


# @app.post("/user")
# async def user(user: User):
#     if user.age >= 18:
#         user.is_adult = True
#     return user


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


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8000,
        reload=True
    )
