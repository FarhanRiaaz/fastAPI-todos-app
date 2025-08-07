from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException, Request
from ..user_request import CreateUserRequest
from sqlalchemy.orm import Session
from ..models import Users
from starlette import status
from ..database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from ..token import Token
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'a905b8123ae530eb75a95473f178fb191afa58436f9ae5865fd01fd9985d5977'
ALGORITHM = 'HS256'

brcypt_context = CryptContext(schemes=['bcrypt'],deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
database_injection = Annotated[Session,Depends(get_db)]
templates = Jinja2Templates(directory='TodoApp/templates')
### PAGES ###
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html",{"request":request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html",{"request":request})

### ENDPOINTS ###
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

async def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Couldnot validate credentails')
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Couldnot validate credentails')      

@router.post("/add_user",status_code=status.HTTP_201_CREATED)
async def create_user(db: database_injection, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        phone_number= create_user_request.phone_number,
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Couldnot validate credentails')
    else:
        token = create_access_token(user_name=user.username,user_id=user.id,expires_delta=timedelta(20))    
        return {'access_token':token,'token_type':'bearer'}
