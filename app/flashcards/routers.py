from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routers import get_current_user
from app.database import get_db
from app.flashcards import crud
from app.flashcards.requests_schemas import (
    FlashcardCreate,
    FlashcardOut,
    FlashcardUpdate,
)
from app.models.auth import RoleEnum, User
from app.permissions import require_role

router = APIRouter()


@router.post("/create", response_model=FlashcardOut)
def create_flashcard(
    card: FlashcardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new flashcard.
    """
    require_role(
        workspace_id=card.workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor],
        current_user=current_user,
        db=db,
    )
    return crud.create_flashcard(db, card, user_id=current_user.id)


@router.get("/workspace/{workspace_id}", response_model=list[FlashcardOut])
def get_workspace_flashcards(
    workspace_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """
    Get all flashcards for a specific workspace.
    """
    return crud.get_flashcards_by_workspace(db, workspace_id, skip, limit)


@router.get("/get/{card_id}", response_model=FlashcardOut)
def get_flashcard(card_id: int, db: Session = Depends(get_db)):
    """
    Get a specific flashcard by its ID.
    """
    db_card = crud.get_flashcard(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return db_card


@router.put("/update/{card_id}", response_model=FlashcardOut)
def update_flashcard(
    card_id: int,
    update_data: FlashcardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a specific flashcard by its ID.
    """
    require_role(
        workspace_id=update_data.workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor],
        current_user=current_user,
        db=db,
    )
    db_card = crud.update_flashcard(db, card_id, update_data)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return db_card


@router.delete("/delete/{workspace_id}/{card_id}")
def delete_flashcard(
    workspace_id: int,
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a specific flashcard by its ID.
    """
    require_role(
        workspace_id=workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor],
        current_user=current_user,
        db=db,
    )
    db_card = crud.delete_flashcard(db, card_id)
    if not db_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return {"message": "Deleted"}
