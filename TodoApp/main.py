from fastapi import FastAPI
from .models import Base
from .database import engine, SessionLocal
# this line will import the routers from there
from .routers import auth,todos,users
app = FastAPI()
 

Base.metadata.create_all(bind=engine)
#this is the health check to check if the app work or not
@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}

#this line enables the routing so that we can access multiple files at one time
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)