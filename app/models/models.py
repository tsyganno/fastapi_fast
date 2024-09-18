from pydantic import BaseModel, EmailStr, Field


class TrueUser(BaseModel):
    username: str
    password: str
    role: str = 'guest'


class Login_User(BaseModel):
    username: str
    password: str


class User(BaseModel):
    name: str
    age: int
    is_adult: bool = False


class Feedback(BaseModel):
    name: str
    message: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = Field(default=None, ge=0, lt=90)
    is_subscribed: bool = False

