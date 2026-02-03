from pydantic import BaseModel, Field, ConfigDict


class QuoteBase(BaseModel):
    text: str = Field(..., title="Texto de la cita", min_length=10)
    author: str = Field(..., title="Autor", min_length=3)
    category: str | None = "General"

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
