from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class QuoteBase(BaseModel):
    text: str = Field(..., title="Texto de la cita", min_length=10)
    author: str = Field(..., title="Autor", min_length=3)
    category: Optional[str] = "General"

class QuoteCreate(QuoteBase):
    pass

class Quote(QuoteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
