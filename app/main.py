from fastapi import FastAPI
from app.routers import users
from app.auth.views import router as auth_router
from app.workspaces import views

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(views.router, prefix="/workspaces")
