from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models.quote import Quote as QuotePydantic, QuoteCreate
from ..misc.database import get_db
from ..misc.security import get_current_user
from ..models.user import User as UserModel
from ..controllers.quote import quote_controller

router = APIRouter(
    prefix="/quotes",
    tags=["quote"],
    responses={404: {"description": "Not found"}},
)

@router.get("", response_model=List[QuotePydantic])
async def read_quotes(db: Session = Depends(get_db)):
    return quote_controller.read_quotes(db=db)

@router.post("", response_model=QuotePydantic, status_code=201)
async def create_quote(quote: QuoteCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return quote_controller.create_quote(db=db, quote=quote)
