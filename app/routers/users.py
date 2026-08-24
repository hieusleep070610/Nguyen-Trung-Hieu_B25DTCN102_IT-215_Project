from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from models.user import UserModel
from schemas.schema import UserResponse
from dependencies.dependencies import get_current_user,admin_required

router = APIRouter(prefix="/users",tags=["Users"])
# lấy token -> decode JWT -> lấy user_id -> truy xuất User trong DB
@router.get("/me",response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("")
def get_users(
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(admin_required) #role
):
    query = db.query(UserModel)

    if search:
        "tìm kiếm chuỗi có chứa một đoạn văn bản nào đó."
        query = query.filter((UserModel.full_name.contains(search))|(UserModel.email.contains(search)))

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)
    return query.all()