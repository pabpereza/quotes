from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from ..models import quote as quote_model
from ..db import quote as quote_db
from fastapi import HTTPException

class QuoteController:
    def _get_quote(self, db: Session, quote_id: int):
        return db.query(quote_db.Quote).filter(quote_db.Quote.id == quote_id).first()

    def read_quotes(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(quote_db.Quote).offset(skip).limit(limit).all()

    def get_random_quote(self, db: Session):
        """Obtiene una cita aleatoria de la base de datos."""
        quote = db.query(quote_db.Quote).order_by(func.random()).first()
        if quote is None:
            raise HTTPException(status_code=404, detail="No quotes available")
        return quote

    def create_quote(self, db: Session, quote: quote_model.QuoteCreate):
        db_quote = quote_db.Quote(**quote.model_dump())
        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        return db_quote

    def read_quote(self, db: Session, quote_id: int):
        db_quote = self._get_quote(db, quote_id)
        if db_quote is None:
            raise HTTPException(status_code=404, detail="Quote not found")
        return db_quote

    def update_quote(self, db: Session, quote_id: int, quote: quote_model.QuoteCreate):
        db_quote = self._get_quote(db, quote_id)
        if db_quote is None:
            raise HTTPException(status_code=404, detail="Quote not found")
        
        update_data = quote.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_quote, key, value)

        db.add(db_quote)
        db.commit()
        db.refresh(db_quote)
        return db_quote

    def delete_quote(self, db: Session, quote_id: int):
        db_quote = self._get_quote(db, quote_id)
        if db_quote is None:
            raise HTTPException(status_code=404, detail="Quote not found")
        db.delete(db_quote)
        db.commit()
        return db_quote

quote_controller = QuoteController()
