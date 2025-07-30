from fastapi import FastAPI
from Model import models
from Database.database import engine
 
app = FastAPI()
 
models.Base.metadata.create_all(bind=engine)
 