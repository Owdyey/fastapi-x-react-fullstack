from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine
from app import database, models, operations
from app.routers import items, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)

