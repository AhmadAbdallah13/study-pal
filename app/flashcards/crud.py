from sqlalchemy.orm import Session

from app.flashcards.requests_schemas import FlashcardCreate, FlashcardUpdate
from app.models.flashcards import Flashcard


def create_flashcard(db: Session, flashcard: FlashcardCreate, user_id: int):
    db_card = Flashcard(**flashcard.model_dump(), created_by_id=user_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_flashcard(db: Session, flashcard_id: int):
    return db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()


def get_flashcards_by_workspace(db: Session, workspace_id: int, skip=0, limit=20):
    return (
        db.query(Flashcard)
        .filter(Flashcard.workspace_id == workspace_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_flashcard(db: Session, flashcard_id: int, update_data: FlashcardUpdate):
    db_card = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if db_card:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(db_card, key, value)
        db.commit()
        db.refresh(db_card)
    return db_card


def delete_flashcard(db: Session, flashcard_id: int):
    db_card = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
    if db_card:
        db.delete(db_card)
        db.commit()
    return db_card
