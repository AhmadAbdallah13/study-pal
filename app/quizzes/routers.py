from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.routers import get_current_user
from app.database import get_db
from app.models.auth import RoleEnum, Workspace
from app.models.quizzes import Quiz, QuizQuestion
from app.permissions import require_role
from app.quizzes.requests_schemas import (
    QuizCreate,
    QuizOut,
    QuizQuestionCreate,
    QuizQuestionOut,
)

router = APIRouter()


@router.post("/workspace/{workspace_id}/quiz/create", response_model=QuizOut)
def create_quiz(
    workspace_id: int,
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    require_role(
        workspace_id=workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor],
        current_user=current_user,
        db=db,
    )
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    new_quiz = Quiz(
        title=quiz.title,
        description=quiz.description,
        workspace_id=workspace_id,
        created_by_id=current_user.id,
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


@router.post("/{quiz_id}/add-question", response_model=QuizQuestionOut)
def add_question(
    quiz_id: int,
    question: QuizQuestionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    require_role(
        workspace_id=quiz.workspace_id,
        roles=[RoleEnum.admin, RoleEnum.editor],
        current_user=current_user,
        db=db,
    )

    new_question = QuizQuestion(
        quiz_id=quiz_id,
        question=question.question,
        type=question.type,
        options=question.options,
        correct_answer=question.correct_answer,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question
