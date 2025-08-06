from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from starlette import status
from ..models import Users
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..user_verification_request import UserVerification
from .auth import get_current_user
from ..database import SessionLocal

router = APIRouter(
    prefix='/user',
    tags=['user']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
database_injection = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
brcypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

@router.get("/get_user",status_code=status.HTTP_200_OK)
async def get_user(db: database_injection, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    return db.query(Users).filter(Users.id == user.get('id')).first()
    
@router.put("/update_passowrd",status_code=status.HTTP_204_NO_CONTENT)
async def update_password(db:database_injection,user:user_dependency,user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if not brcypt_context.verify(user_verification.password,current_user.hashed_password):
        raise HTTPException(status_code=401,detail='Password didnot matched!')
    else:
        current_user.hashed_password = brcypt_context.hash(user_verification.password)
        db.add(current_user)
        db.commit()

@router.put("/update_phone/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone(db:database_injection,user:user_dependency,phone_number: str):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    current_user.phone_number = phone_number
    db.add(current_user)
    db.commit()        
        
    
        