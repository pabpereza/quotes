from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import token as token_model
from ..misc.database import get_db
from ..controllers.auth import auth_controller

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=token_model.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_controller.login_for_access_token(db=db, form_data=form_data)
