from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class QuizTypeEnum(str, Enum):
    multiple_choice = "multiple_choice"
    true_false = "true_false"
    short_answer = "short_answer"


class QuizQuestionCreate(BaseModel):
    question: str
    type: QuizTypeEnum
    options: Optional[List[str]] = None
    correct_answer: str


class QuizQuestionOut(QuizQuestionCreate):
    id: int

    class Config:
        orm_mode = True


class QuizCreate(BaseModel):
    title: str
    description: Optional[str] = None


class QuizOut(QuizCreate):
    id: int
    created_at: datetime
    questions: List[QuizQuestionOut] = []

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
