from database import Base
from sqlalchemy import Column, Integer, String, Boolean # type: ignore
from pydantic import BaseModel # type: ignore


class ToDos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)



class ToDoCreate(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool = False
