from fastapi import Path
from pydantic import BaseModel


class Source(BaseModel):
    name: str
    year: int

    class config:
        orm_mode = True

class Type(BaseModel):
    name: str
    description: str

    class config:
        orm_mode = True
    

class Tag(BaseModel):
    name: str
    description: str

    class config:
        orm_mode = True

class Quote(BaseModel):
    text: str
    source: Source | None = None
    type: Type | None = None
    tags: list[Tag] | None = None

    class config:
        orm_mode = True
