from database import Base
from sqlalchemy import Column, Integer, String, Boolean # type: ignore
from pydantic import BaseModel, Field # type: ignore


class ToDos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)



class ToDoCreate(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 
