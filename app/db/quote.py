from sqlalchemy import Column, Integer, String
from ..misc.database import Base

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    author = Column(String)
    category = Column(String, default="General")
