from sqlalchemy.orm import Session

from app.models.quizzes import QuizQuestion
from app.quizzes.requests_schemas import QuizCreate, QuizUpdate


def create_quiz(db: Session, quiz: QuizCreate, user_id: int):
    db_quiz = QuizQuestion(**quiz.model_dump(), created_by_id=user_id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def get_quizzes_by_workspace(db: Session, workspace_id: int, skip=0, limit=20):
    return (
        db.query(QuizQuestion)
        .filter(QuizQuestion.workspace_id == workspace_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_quiz(db: Session, quiz_id: int):
    return db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()


def update_quiz(db: Session, quiz_id: int, update_data: QuizUpdate):
    db_quiz = db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()
    if db_quiz:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(db_quiz, key, value)
        db.commit()
        db.refresh(db_quiz)
    return db_quiz


def delete_quiz(db: Session, quiz_id: int):
    db_quiz = db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
    return db_quiz
