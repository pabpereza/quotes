from fastapi import FastAPI, Response
import os

# Importing the routers and models
from .models import quote
from .routers import quote, probes

# Database Connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get variables from environment
USER = os.getenv("POSTGRES_USER", "default_user")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_password")
HOST = os.getenv("POSTGRES_HOST", "localhost")
DATABASE = os.getenv("POSTGRES_DB", "default_db")

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s".format(USER, PASSWORD, HOST, DATABASE)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()


# PROBES
@app.get("/startup")
async def startup_check():
    ## Comprobar si el servicio de fastapi esta ejecutandose correctamente
    return Response(status_code=200, content="Service is started up successfully.") 

@app.get("/health")
async def health_check():
    ## Comprobar si el servicio de fastapi esta ejecutandose correctamente
    return Response(status_code=200, content="Service is healthy.") 

@app.get("/ready")
async def readiness_check():
    ## Comprobar si la base de datos o las dependencias externas estan disponibles

    return Response(status_code=200, content="Service is ready to accept requests.")

@app.get("/fail")
async def fail_check():
    ## Ruta para simular un fallo en el servicio
    return Response(status_code=500, content="This is a simulated failure endpoint.")

# ROUTES 
app.include_router(quote.router)



