
from fastapi import FastAPI, Depends, HTTPException, Path # pyright: ignore[reportMissingImports]
from typing import Annotated
from sqlalchemy.orm import Session # type: ignore
import models 
from models import ToDos
from database import engine, SessionLocal
from starlette import status # type: ignore

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #will create everything from db.py and model.py files

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/",  status_code=status.HTTP_200_OK)
async def read_All(db: db_dependency): # type: ignore
    return db.query(ToDos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int):  # type: ignore
    todo_model =  db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail = 'Todo not found')
    