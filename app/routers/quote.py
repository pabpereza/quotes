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

# AI Routes
@router.get("/ai")
async def read_ai_quotes():
    # Make request to docker model ai with a prompt
    # Return the response

    request = {
        "prompt": "Give me a random quote",
        "max_length": 50,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.2,
    }
