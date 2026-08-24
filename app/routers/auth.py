from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.schema import UserCreate,UserLogin,UserResponse
from services.users import register_user,login_user

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post("/register",response_model=UserResponse,status_code=201)
def register(user: UserCreate,db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):
    return login_user(user, db)