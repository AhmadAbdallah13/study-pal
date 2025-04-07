import enum
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class QuizTypeEnum(str, enum.Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    short_answer = "short_answer"


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    created_at = Column(DateTime, default=datetime.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))

    created_by = relationship("User", back_populates="quizzes")
    workspace = relationship("Workspace", back_populates="quizzes")
    questions = relationship(
        "QuizQuestion", back_populates="quiz", cascade="all, delete"
    )


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question = Column(String, nullable=False)
    type = Column(Enum(QuizTypeEnum), nullable=False)
    options = Column(JSON, nullable=True)
    correct_answer = Column(String, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
