from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import UserModel
from dependencies.dependencies import get_current_user
from schemas.schema import ResearchTaskCreate,ResearchTaskUpdate
from services.research_tasks import *

router = APIRouter(tags=["Research Tasks"])

@router.post("/research-projects/{project_id}/research-tasks")
# Tạo nhiệm vụ
def create_task_api(
    project_id: int,
    data: ResearchTaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return create_task(project_id,data,current_user,db)

@router.get("/research-tasks/{task_id}")
def get_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_task(task_id,current_user,db)

@router.patch("/research-tasks/{task_id}/assign")
# gán assign
def assign_task_api(
    task_id: int,
    assignee_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return assign_task(task_id,assignee_id,current_user,db)

@router.patch("/research-tasks/{task_id}")
def update_task_api(
    task_id: int,
    data: ResearchTaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return update_task(task_id,data,current_user,db)

@router.delete("/research-tasks/{task_id}")
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return delete_task(task_id,current_user,db)
