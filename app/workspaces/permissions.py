from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import WorkspaceMember, RoleEnum

def get_workspace_role(workspace_id: int, user_id: int, db: Session):
    member = db.query(WorkspaceMember).filter_by(user_id=user_id, workspace_id=workspace_id).first()
    return member.role if member else None

def require_role(workspace_id: int, required_role: RoleEnum):
    def role_checker(user=Depends(get_current_user), db: Session = Depends(get_db)):
        role = get_workspace_role(workspace_id, user.id, db)
        if not role or role not in [required_role, RoleEnum.admin]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return role
    return role_checker
