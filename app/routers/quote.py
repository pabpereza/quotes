from fastapi import APIRouter, HTTPException
from ..models.quote import Quote

router = APIRouter(
    prefix="/quote",
    tags=["quote"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def read_quotes():
    return [{"text": "quote1"}, {"text": "quote2"}]


@router.post("")
async def create_quote(quote: Quote):
    return quote
