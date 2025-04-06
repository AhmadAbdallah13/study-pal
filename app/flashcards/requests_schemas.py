from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class FlashcardBase(BaseModel):
    question: str
    answer: str
    markdown_enabled: Optional[bool] = True
    image_url: Optional[HttpUrl] = None


class FlashcardCreate(FlashcardBase):
    workspace_id: int


class FlashcardUpdate(FlashcardBase):
    workspace_id: int


class FlashcardOut(FlashcardBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        orm_mode = True
