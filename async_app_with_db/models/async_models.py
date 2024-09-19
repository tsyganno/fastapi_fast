from sqlalchemy import Column, String, BigInteger, Boolean
from async_app_with_db.models.async_base import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(BigInteger, autoincrement=True, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
