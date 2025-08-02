from fastapi import APIRouter,Depends, HTTPException, Path
from Model.models import Todos
from RequestModel.todo_request import TodoRequest
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from Database.database import SessionLocal
from .auth import get_current_user


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

@router.get("/",status_code= status.HTTP_200_OK)
async def read_all(db: database_injection):
    return db.query(Todos).all()  

@router.get("/todo/{todo_id}",status_code= status.HTTP_200_OK)
async def read_todo(db: database_injection, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id== todo_id).first()
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
                      todo_request: TodoRequest,
                      todo_id: int= Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
async def delete_todo(db: database_injection, todo_id:int = Path(gt=0)):
            todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
            if todo_model is None:
                raise HTTPException(status_code=404,detail='Todo not found!')
            else:
                db.query(Todos).filter(Todos.id == todo_id).delete()
                db.commit()