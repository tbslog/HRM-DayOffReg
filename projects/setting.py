from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, or_
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import FastAPI, Depends
from pathlib import Path
import os


DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_HOSTS = ["*"]
MIDDLEWARE = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

