from fastapi import FastAPI

from app.auth import routers as auth_routers
from app.flashcards import routers as flashcards_routers
from app.quizzes import routers as quizzes_routers
from app.workspaces import routers as workspace_routers

app = FastAPI()

app.include_router(auth_routers.router, prefix="/auth")
app.include_router(workspace_routers.router, prefix="/workspaces")
app.include_router(flashcards_routers.router, prefix="/flashcards")
app.include_router(quizzes_routers.router, prefix="/quizzes")
