from fastapi import FastAPI

from .models import quote
from .routers import quote

app = FastAPI()

app.include_router(quote.router)



