from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

#ORM Importation
from . import models
from .database import engine,SessionLocal , get_db
from sqlalchemy.orm import Session 
from .routers import post,user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_msg():
    return {"message": "Bienvenidos a mi API REST, una aplicaicón de POST"}
