from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base


class ResearchProjectModel(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255),nullable=False)
    description = Column(Text)
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime,server_default=func.now())
    owner = relationship("UserModel",back_populates="owned_projects")
    members = relationship("ResearchMemberModel",back_populates="project",cascade="all, delete-orphan")
    tasks = relationship("ResearchTaskModel",back_populates="project",cascade="all, delete-orphan")


class ResearchMemberModel(Base):
    __tablename__ = "research_members"

    project_id = Column(Integer,ForeignKey("research_projects.id"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
    role = Column(String(20),nullable=False)
    joined_at = Column(DateTime,server_default=func.now())
    project = relationship("ResearchProjectModel",back_populates="members")
    user = relationship("UserModel")