from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from models.research_project import ResearchProjectModel,ResearchMemberModel
from schemas.schema import ResearchProjectCreate,ResearchProjectUpdate

from models.user import UserModel
# Tạo dự án
def create_project(data: ResearchProjectCreate,current_user: UserModel,db: Session):
    project = ResearchProjectModel(
        name=data.name,
        description=data.description,
        owner_id=current_user.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    owner_member = ResearchMemberModel(
        project_id=project.id,
        user_id=current_user.id,
        role="OWNER"
    )

    db.add(owner_member)
    db.commit()

    return project
# Lấy danh sách dự án
def get_projects(current_user: UserModel,db: Session):
    query = (
        db.query(ResearchProjectModel)
        # ghép dữ liệu từ 2 bảng 
        .join(
            ResearchMemberModel,
            ResearchProjectModel.id == ResearchMemberModel.project_id
        )
        .filter(
            ResearchMemberModel.user_id == current_user.id
        )
    )

    return query.all()
# Lấy chi tiết dự án
def get_project_detail(project_id: int,current_user: UserModel,db: Session):
    project = (db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first())

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )
    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xem"
        )

    return project
# kiểm tra xem người dùng hiện tại có phải OWNER của đề tài nghiên cứu hay không
def check_owner(project_id: int,user_id: int,db: Session):

    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == user_id,
            ResearchMemberModel.role == "OWNER"
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER được thực hiện"
        )

    return member
# Cập nhật dự án
def update_project(project_id: int,data: ResearchProjectUpdate,current_user: UserModel,db: Session):
    check_owner(project_id,current_user.id,db)

    project = (db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first())

    if not project:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )

    project.name = data.name
    project.description = data.description

    db.commit()
    db.refresh(project)

    return project
# Xoá dự án
def delete_project(project_id: int,current_user: UserModel,db: Session):

    check_owner(project_id,current_user.id,db)
    project = (db.query(ResearchProjectModel).filter(ResearchProjectModel.id == project_id).first())

    if not project:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy dự án"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Xóa thành công"
    }
# Thêm thành viên
def add_member(
    project_id: int,user_id: int,current_user: UserModel,db: Session):
    check_owner(project_id,current_user.id,db)

    user = (db.query(UserModel).filter(UserModel.id == user_id).first())

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )

    existing = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == user_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Người dùng đã là thành viên project"
        )

    member = ResearchMemberModel(
        project_id=project_id,
        user_id=user_id,
        role="MEMBER"
    )

    db.add(member)
    db.commit()

    return {
        "message": "Thêm thành viên thành công"
    }
# Xoá thành viên
def remove_member(project_id: int,user_id: int,current_user: UserModel,db: Session):

    check_owner(
        project_id,
        current_user.id,
        db
    )

    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == user_id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Member không tồn tại"
        )

    if member.role == "OWNER":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Không được xóa OWNER"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành công"
    }
# Lấy danh sách thành viên
def get_members(project_id: int,current_user: UserModel,db: Session):

    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == project_id,
            ResearchMemberModel.user_id == current_user.id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xem"
        )

    return (
        db.query(ResearchMemberModel).filter(ResearchMemberModel.project_id == project_id).all()
    )
