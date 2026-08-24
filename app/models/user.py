from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100),unique=True,nullable=False)
    password_hash = Column(String(100),nullable=False)
    full_name = Column(String(50),nullable=False)
    role = Column(String(20),default="USER")
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,server_default=func.now())
    owned_projects = relationship("ResearchProjectModel",back_populates="owner")
    tasks = relationship("ResearchTaskModel",back_populates="assignee")