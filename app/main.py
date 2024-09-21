from fastapi import FastAPI

# Importing the routers and models
from .models import quote
from .routers import quote

# Database Connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = "user"
PASSWORD = "password"
HOST = "localhost"
DATABASE = "quotes"

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s".format(USER, PASSWORD, HOST)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()


# ROUTES 
app.include_router(quote.router)



