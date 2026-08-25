from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from models.user import UserModel
from models.research_task import ResearchTaskModel
from models.research_project import ResearchMemberModel
from schemas.schema import ResearchTaskCreate,ResearchTaskUpdate

def check_member(project_id: int,user_id: int,db: Session):
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
            status_code=403,
            detail="Không có quyền hạn"
        )
    return member
# Tạo nhiệm vụ nghiên cứu
def create_task(project_id: int,data: ResearchTaskCreate,current_user: UserModel,db: Session):
    check_member(project_id,current_user.id,db)

    task = ResearchTaskModel(
        project_id=project_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        due_date=data.due_date,
        status="TODO"
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return task

# Lấy danh sách nhiệm vụ chi tiết
def get_task(task_id: int,current_user: UserModel,db: Session):
    task = (db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first())

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task không tồn tại"
        )

    check_member(
        task.project_id,
        current_user.id,
        db
    )

    return task
# Gán assignee
def assign_task(task_id: int,assignee_id: int,current_user: UserModel,db: Session):
    task = get_task(task_id,current_user,db)
    owner = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == current_user.id,
            ResearchMemberModel.role == "OWNER"
        )
        .first()
    )
    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER được giao việc"
        )
    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == assignee_id
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=400,
            detail="User không thuộc project"
        )
    task.assignee_id = assignee_id
    db.commit()
    db.refresh(task)

    return task

def update_task(task_id: int,data: ResearchTaskUpdate,current_user: UserModel,db: Session):
    task = get_task(task_id,current_user,db)

    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == current_user.id
        ).first())
# chủ đc sửa tất cả field
    if member.role == "OWNER":

        data_dict = data.model_dump()
        for key, value in data_dict.items():
            setattr(task, key, value)
# assignee chỉ đc sửa mỗi field trạng thái
    elif task.assignee_id == current_user.id:
        if data.status:
            task.status = data.status

    else:
        raise HTTPException(
            status_code=403,
            detail="Không có quyền"
        )

    db.commit()
    db.refresh(task)

    return task

def delete_task(task_id: int,current_user: UserModel,db: Session):
    task = get_task(task_id,current_user,db)

    owner = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == current_user.id,
            ResearchMemberModel.role == "OWNER"
        )
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=403,
            detail="Chỉ OWNER được xóa"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Xóa thành công"
    }