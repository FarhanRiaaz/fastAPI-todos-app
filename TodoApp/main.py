from fastapi import FastAPI, Request
from .models import Base
from .database import engine, SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# this line will import the routers from there
from .routers import auth,todos,users
app = FastAPI()
 

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='TodoApp/templates')

app.mount("/static",StaticFiles(directory="TodoApp/static"),name="static")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

#this is the health check to check if the app work or not
@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}

#this line enables the routing so that we can access multiple files at one time
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)