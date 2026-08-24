from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class ResearchTaskModel(Base):
    __tablename__ = "research_tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer,ForeignKey("research_projects.id"),nullable=False)
    title = Column(String(100),nullable=False)
    description = Column(Text)
    assignee_id = Column(Integer,ForeignKey("users.id"))
    status = Column(String(20),nullable=False)
    priority = Column(String(20),nullable=False)
    due_date = Column(DateTime)
    created_at = Column(DateTime,server_default=func.now())
    project = relationship("ResearchProjectModel",back_populates="tasks")
    assignee = relationship("UserModel",back_populates="tasks")