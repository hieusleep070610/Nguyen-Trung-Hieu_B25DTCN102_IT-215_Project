from fastapi import FastAPI,HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.user import UserModel
from models.research_project import ResearchProjectModel,ResearchMemberModel
from models.research_task import ResearchTaskModel
from db.database import Base, engine,get_db

from routers.auth import router as auth_router
from routers.users import router as user_router
from routers.research_project import router as project_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)

@app.get("/health-check")
def test_connect(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "success": True,
            "message": "Kết nối database thành công"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi kết nối database: {str(e)}"
        )