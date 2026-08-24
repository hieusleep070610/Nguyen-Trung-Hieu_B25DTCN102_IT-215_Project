from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from schemas.schema import UserCreate, UserLogin
from models.user import UserModel
from core.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


def register_user(user: UserCreate, db: Session):

    existing_email = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )

    new_user = UserModel(
        email=user.email,
        full_name=user.full_name,
        password_hash=get_password_hash(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(user: UserLogin, db: Session):

    db_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng"
        )

    access_token = create_access_token(
        {
            "user_id": db_user.id,
            "role":db_user.role  
        }
    )

    return {
        "access_token":access_token,
        "token_type": "bearer"
    }