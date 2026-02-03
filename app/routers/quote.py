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


@router.get("", response_model=QuotePydantic)
async def get_random_quote(db: Session = Depends(get_db)):
    """Devuelve una cita célebre aleatoria."""
    return quote_controller.get_random_quote(db=db)


@router.get("/all", response_model=list[QuotePydantic])
async def read_all_quotes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Devuelve todas las citas célebres con paginación."""
    return quote_controller.read_quotes(db=db, skip=skip, limit=limit)


@router.post("", response_model=QuotePydantic, status_code=201)
async def create_quote(quote: QuoteCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    """Crea una nueva cita célebre. Requiere autenticación."""
    return quote_controller.create_quote(db=db, quote=quote)
