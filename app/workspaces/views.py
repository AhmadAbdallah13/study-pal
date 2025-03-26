from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Workspace, User
from app.auth.views import get_current_user
from app.workspaces.request_models import CreateWorkspaceRequest

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_workspace(
    body: CreateWorkspaceRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    workspace = Workspace(name=body.name, owner_id=user.id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace


@router.get("/get-user-workspaces")
def get_workspaces(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return db.query(Workspace).filter(Workspace.owner_id == user.id).all()
