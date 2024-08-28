from fastapi import Path
from pydantic import BaseModel


class Source(BaseModel):
    name: str
    year: int

class Type(BaseModel):
    name: str
    description: str

class Tag(BaseModel):
    name: str
    description: str

class Quote(BaseModel):
    text: str
    source: Source | None = None
    type: Type | None = None
    tags: list[Tag] | None = None
