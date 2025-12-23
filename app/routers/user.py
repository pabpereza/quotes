from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import user as user_model
from ..misc.database import get_db
from ..misc.security import get_current_user
from ..controllers.user import user_controller

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=user_model.User)
def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db=db, user=user)

@router.get("/", response_model=List[user_model.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_controller.read_users(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=user_model.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.read_user(db=db, user_id=user_id)

@router.delete("/{user_id}", response_model=user_model.User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return user_controller.delete_user(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=user_model.User)
def update_user(user_id: int, user: user_model.UserUpdate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return user_controller.update_user(db=db, user_id=user_id, user=user)
