from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.auth import RoleEnum, User, WorkspaceMember


def require_role(
    workspace_id: int, roles: list[RoleEnum], current_user: User, db: Session
):
    membership = (
        db.query(WorkspaceMember)
        .filter_by(workspace_id=workspace_id, user_id=current_user.id)
        .first()
    )
    if not membership or membership.role not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return True
