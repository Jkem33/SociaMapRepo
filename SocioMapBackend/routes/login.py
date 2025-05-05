from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models
from database.db import get_db
from pydantic import BaseModel

router = APIRouter()

class LoginInput(BaseModel):
    email_or_username: str
    password: str

@router.post("/login")
def login_user(user: LoginInput, db: Session = Depends(get_db)):
    user_record = db.query(models.User).filter(
        (models.User.email == user.email_or_username) | 
        (models.User.username == user.email_or_username)
    ).first()

    if not user_record or user_record.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect credentials")

    return {"message": "Login successful"}