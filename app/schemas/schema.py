from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "USER"

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str
    password: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Project

class ResearchProjectCreate(BaseModel):
    name: str = Field(min_length=1 , max_length=255)
    description: Optional[str] = None


class ResearchProjectUpdate(BaseModel):
    name: str = Field(min_length=1,max_length=255)
    description: Optional[str] = None


class ResearchProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# task 

class ResearchTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = Field(default="MEDIUM",pattern="^(LOW|MEDIUM|HIGH)$")
    due_date: Optional[datetime] = None


class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = Field(default=None,pattern="^(LOW|MEDIUM|HIGH)$")
    status: Optional[str] = Field(default=None,pattern="^(TODO|IN_PROGRESS|DONE)$")
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class ResearchTaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    assignee_id: Optional[int]
    status: str
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MemberCreate(BaseModel):
    user_id: int
    role: str = "MEMBER"

class MemberResponse(BaseModel):
    user_id: int
    project_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)
