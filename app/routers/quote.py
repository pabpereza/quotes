from fastapi import APIRouter, HTTPException
from ..models.quote import Quote

router = APIRouter(
    prefix="/quote",
    tags=["quote"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def read_quotes():
    return [{"Hola Mundo": "- Random developer"}]


@router.post("")
async def create_quote(quote: Quote):
    return quote
