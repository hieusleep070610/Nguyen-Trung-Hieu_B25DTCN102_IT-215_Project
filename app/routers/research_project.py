from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import get_db
from dependencies.dependencies import get_current_user
from models.user import UserModel
from schemas.schema import (ResearchProjectCreate,ResearchProjectUpdate,ResearchProjectResponse,MemberCreate,MemberResponse)

from services.research_projects import *

router = APIRouter(prefix="/research-projects",tags=["Research Projects"])

@router.post("",response_model=ResearchProjectResponse)
def create_pj(
    data: ResearchProjectCreate,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return create_project(data,current_user,db)

@router.get("")
def get_all_pj(
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_projects(current_user,db,search)

@router.get("/{project_id}",response_model=ResearchProjectResponse)
def get_detail_pj(project_id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return get_project_detail(project_id,current_user,db)

@router.put("/{project_id}")
def update_pj(
    project_id: int,
    data: ResearchProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return update_project(project_id,data,current_user,db)

@router.delete("/{project_id}")
def delete_pj(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return delete_project(project_id,current_user,db)

@router.post("/{project_id}/members")
def add_members(
    project_id: int,
    data: MemberCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return add_member(project_id,data.user_id,current_user,db)

@router.delete("/{project_id}/members/{user_id}")
def remove_members(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return remove_member(project_id,user_id,current_user,db)

@router.get("/{project_id}/members",response_model=list[MemberResponse])
def get_members_api(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_members(project_id,current_user,db)
