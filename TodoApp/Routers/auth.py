from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from RequestModel.user_request import CreateUserRequest
from sqlalchemy.orm import Session
from Model.models import Users
from starlette import status
from Database.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from ResponseModel.token import Token

router = APIRouter()

SECRET_KEY = 'a905b8123ae530eb75a95473f178fb191afa58436f9ae5865fd01fd9985d5977'
ALGORITHM = 'HS256'

brcypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
database_injection = Annotated[Session,Depends(get_db)]

def authenticate_user(username: str, passowrd: str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not brcypt_context.verify(passowrd,user.hashed_password):
        return False
    return user

def create_access_token(user_name: str, user_id: str, expires_delta: timedelta):
    encode= {'sub':user_name,'id':user_id}
    expires= datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
        

@router.post("/add_user",status_code=status.HTTP_201_CREATED)
async def create_user(db: database_injection, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        #we have to hash the password
        #hashed_password = create_user_request.password,
        hashed_password = brcypt_context.hash(create_user_request.password),
        is_active= True
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token",status_code=status.HTTP_202_ACCEPTED,response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: database_injection):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return 'Failed Authentication!'
    else:
        token = create_access_token(user_name=user.username,user_id=user.id,expires_delta=timedelta(20))    
        return {'access_token':token,'token_type':'bearer'}
