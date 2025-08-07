from fastapi import APIRouter,Depends, HTTPException, Path, Request, status
from ..models import Todos
from ..todo_request import TodoRequest
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="TodoApp/templates")


router = APIRouter(
      prefix='/todo',
    tags=['todos']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
database_injection = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response
    
    

### PAGES ###
@router.get("/todo-page")
async def render_todo_page(request: Request,db: database_injection):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        else: todos = db.query(Todos).filter(Todos.owner_id== user.get('id')).all()
        return templates.TemplateResponse("todo.html", {"request": request,"todos":todos,"user":user})
    except:
        return redirect_to_login()
@router.get("/add-todo-page")
async def render_todo_page(request: Request):
    
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request,"user":user})
    except:
        return redirect_to_login()
        
            
    

### ENDPOINTS ###
@router.get("/",status_code= status.HTTP_200_OK)
async def read_all(db: database_injection,user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    return db.query(Todos).filter(Todos.owner_id== user.get('id')).all()  

@router.get("/todo/{todo_id}",status_code= status.HTTP_200_OK)
async def read_todo(db: database_injection, user: user_dependency,todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    todo_model = db.query(Todos).filter(Todos.id== todo_id)\
        .filter(Todos.owner_id== user.get('id')).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404,detail='Todo item not found!')
    
    
@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def add_todo(db: database_injection,user: user_dependency,todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    todo_model= Todos(**todo_request.model_dump(),owner_id = user.get('id'))
    db.add(todo_model)
    db.commit()
    
@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: database_injection,
                      user: user_dependency,
                      todo_request: TodoRequest,
                      todo_id: int= Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404,detail= 'Not Authenticated')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id== user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail= 'Item not found for id {todo_id}!')
    else:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        
        db.add(todo_model)
        db.commit()
        
@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,db: database_injection, todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed!')
    else:
        todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id== user.get('id')).first()
        if todo_model is None:
            raise HTTPException(status_code=404,detail='Todo not found!')
        else:
            db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id== user.get('id')).delete()
            db.commit()