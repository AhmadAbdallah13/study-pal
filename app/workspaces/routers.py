from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routers import get_current_user
from app.database import get_db
from app.models.auth import RoleEnum, User, Workspace, WorkspaceMember
from app.models.quizzes import Quiz
from app.permissions import require_role
from app.quizzes.requests_schemas import QuizOut
from app.workspaces.requests_schemas import CreateWorkspaceRequest, WorkspaceOut

router = APIRouter()


@router.post("/create", response_model=WorkspaceOut)
def create_workspace(
    body: CreateWorkspaceRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    workspace = Workspace(name=body.name, owner_id=user.id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    # Automatically assign the creator as Admin
    workspace_member = WorkspaceMember(
        user_id=user.id, workspace_id=workspace.id, role=RoleEnum.admin
    )
    db.add(workspace_member)
    db.commit()

    return workspace


@router.get("/get-user-workspaces")
def get_workspaces(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return db.query(Workspace).filter(Workspace.owner_id == user.id).all()


@router.post("/{workspace_id}/join")
def join_workspace(
    workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    """user joins a workspace as a viewer"""

    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Check if the user is already a member
    existing_member = (
        db.query(WorkspaceMember)
        .filter_by(user_id=user.id, workspace_id=workspace_id)
        .first()
    )
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member")

    new_member = WorkspaceMember(
        user_id=user.id, workspace_id=workspace_id, role=RoleEnum.viewer
    )
    db.add(new_member)
    db.commit()

    return {"message": "Joined workspace successfully"}


@router.delete("/{workspace_id}/delete")
def delete_workspace(
    workspace_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    if workspace.owner_id != user.id:
        raise HTTPException(
            status_code=403, detail="Only the owner can delete this workspace"
        )

    db.delete(workspace)
    db.commit()

    return {"message": "Workspace deleted successfully"}


@router.get("/{workspace_id}/get-all-quizzes", response_model=list[QuizOut])
def list_workspace_quizzes(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_role(
        workspace_id=workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor, RoleEnum.viewer],
        current_user=current_user,
        db=db,
    )
    quizzes = db.query(Quiz).filter(Quiz.workspace_id == workspace_id).all()
    return quizzes
