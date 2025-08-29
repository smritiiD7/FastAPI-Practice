
from fastapi import APIRouter, Depends, HTTPException, Path, Body # pyright: ignore[reportMissingImports]
from typing import Annotated
from sqlalchemy.orm import Session # type: ignore
from starlette import status # type: ignore
from database import SessionLocal
from models import ToDos, ToDoCreate

router = APIRouter()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/",  status_code=status.HTTP_200_OK)
async def read_All(db: db_dependency): # type: ignore
    return db.query(ToDos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int):  # type: ignore
    todo_model =  db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail = 'Todo not found')

@router.post("/todo/add", status_code=status.HTTP_201_CREATED)
async def add_task(db: db_dependency, todo: ToDoCreate ): # type: ignore
    to_do_model = ToDos ( #Use SQLAlchemy model here
        title = todo.title,
        description = todo.description,
        priority = todo.priority,
        complete = todo.complete
    )
    db.add(to_do_model)
    db.commit()
    db.refresh(to_do_model)

    return to_do_model
    

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo: ToDoCreate, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='To Do not found.')
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
   
    
    db.add(todo_model)
    db.commit()
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(ToDos).filter(ToDos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(ToDos).filter(ToDos.id == todo_id).delete()

    db.commit()