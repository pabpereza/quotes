from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import user as user_model
from ..db import user as user_db
from ..misc.hashing import get_password_hash

class UserController:
    def _get_user_by_email(self, db: Session, email: str):
        return db.query(user_db.User).filter(user_db.User.email == email).first()

    def _get_user(self, db: Session, user_id: int):
        return db.query(user_db.User).filter(user_db.User.id == user_id).first()

    def create_user(self, db: Session, user: user_model.UserCreate):
        db_user = self._get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        db_user = user_db.User(email=user.email, username=user.username, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def read_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(user_db.User).offset(skip).limit(limit).all()

    def read_user(self, db: Session, user_id: int):
        db_user = self._get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    def update_user(self, db: Session, user_id: int, user: user_model.UserUpdate):
        db_user = self._get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int):
        db_user = self._get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return db_user
        
user_controller = UserController()
