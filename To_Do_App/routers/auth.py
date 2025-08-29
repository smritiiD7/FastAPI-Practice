from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session # type: ignore
from starlette import status
#from todos import db_dependency

router = APIRouter()

bcrypt_context=CryptContext(schemes=[ 'bcrypt' ], deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/auth",status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
       # hashed_password=create_user_request.password, #not hashing, saving as plain text
        hashed_password= bcrypt_context.hash(create_user_request.password),
        is_Active=True
    )
    db.add(create_user_model)
    db.commit()


