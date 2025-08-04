from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from starlette import status
from Model.models import Users
from sqlalchemy.orm import Session
from .auth import get_current_user,authenticate_user,brcypt_context

from Database.database import SessionLocal

router = APIRouter(
    prefix='/users',
    tags=['users']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
database_injection = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/get_user",status_code=status.HTTP_200_OK)
async def get_user(db: database_injection, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    user_profile = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_profile is None:
        raise HTTPException(status_code=404,detail='User profile not found!')
    else:
        return user_profile

    
@router.put("/update_passowrd",status_code=status.HTTP_204_NO_CONTENT)
async def update_password(db:database_injection,user:user_dependency,old_password:str, new_password: str):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if current_user is None:
        raise HTTPException(status_code=404,detail='User not found!')
    else:
        user = authenticate_user(current_user.username,old_password,db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Password didnnot matched!')
        else:
            user.hashed_password = brcypt_context.hash(new_password)
            db.add(user)
            db.commit()
        
    
        