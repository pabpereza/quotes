from fastapi import FastAPI
from .misc.database import engine, Base
from .routers import quote, probes, user, auth

# Create tables on startup
async def create_tables_on_startup():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Event handler for startup
app.add_event_handler("startup", create_tables_on_startup)

# Include routers
app.include_router(quote.router)
app.include_router(probes.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Citas Célebres"}

