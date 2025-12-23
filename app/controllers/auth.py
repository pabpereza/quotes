from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..misc import security, hashing
from ..db import user as user_db
from fastapi.security import OAuth2PasswordRequestForm

class AuthController:
    def _get_user_by_username(self, db: Session, username: str):
        return db.query(user_db.User).filter(user_db.User.username == username).first()

    def login_for_access_token(self, db: Session, form_data: OAuth2PasswordRequestForm):
        user = self._get_user_by_username(db, username=form_data.username)
        if not user or not hashing.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

auth_controller = AuthController()
