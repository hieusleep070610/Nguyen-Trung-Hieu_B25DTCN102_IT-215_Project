from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.user import UserModel
from models.research_task import ResearchTaskModel
from models.research_project import ResearchMemberModel
from schemas.schema import ResearchTaskCreate,ResearchTaskUpdate
from utils.exceptions import *

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
        forbidden("Không có quyền hạn")
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
def get_tasks(
    project_id: int,
    current_user: UserModel,
    db: Session,
    search=None,
    status_filter=None,
    priority=None,
    assignee_id=None,
    limit=10,
    offset=0,
    sort_by="created_at",
    order="desc"
):
    check_member(project_id,current_user.id,db)

    query = (
        db.query(ResearchTaskModel).filter(ResearchTaskModel.project_id == project_id))
    if search:
        query = query.filter(ResearchTaskModel.title.contains(search))
    if status_filter:
        query = query.filter(ResearchTaskModel.status == status_filter)
    if priority:
        query = query.filter(ResearchTaskModel.priority == priority)
    if assignee_id:
        query = query.filter(ResearchTaskModel.assignee_id == assignee_id)
    # sắp xếp
    if sort_by == "due_date":
        if order == "asc":
            query = query.order_by(ResearchTaskModel.due_date.asc())
        else:
            query = query.order_by(ResearchTaskModel.due_date.desc())
    else:

        if order == "asc":
            query = query.order_by(ResearchTaskModel.created_at.asc())
        else:
            query = query.order_by( ResearchTaskModel.created_at.desc())
    return (query.offset(offset).limit(limit).all())

# Lấy danh sách nhiệm vụ chi tiết
def get_task(task_id: int,current_user: UserModel,db: Session):
    task = (db.query(ResearchTaskModel).filter(ResearchTaskModel.id == task_id).first())

    if not task:
        not_found("Task không tồn tại")

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
        forbidden("Chỉ OWNER được giao việc này")
    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == assignee_id
        )
        .first()
    )

    if not member:
        bad_request("User không thuộc project")
    task.assignee_id = assignee_id
    db.commit()
    db.refresh(task)

    return task

def update_task(
    task_id: int,
    data: ResearchTaskUpdate,
    current_user: UserModel,
    db: Session
):
    task = get_task(
        task_id,
        current_user,
        db
    )
    member = (
        db.query(ResearchMemberModel)
        .filter(
            ResearchMemberModel.project_id == task.project_id,
            ResearchMemberModel.user_id == current_user.id
        )
        .first()
    )

    data_dict = data.model_dump(exclude_unset=True)
    # OWNER sửa tất cả
    if member.role == "OWNER":
        for key, value in data_dict.items():
            setattr(task, key, value)
    # ASSIGNEE chỉ sửa status
    elif task.assignee_id == current_user.id:
        allowed_field = ["status"]
        for key, value in data_dict.items():
            if key not in allowed_field:
                forbidden("Assignee chỉ được cập nhật status")
            setattr(task, key, value)
    else:
        forbidden("Không có quyền")

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
        forbidden("Chỉ OWNER được xóa")

    db.delete(task)
    db.commit()

    return {
        "message": "Xóa thành công"
    }
