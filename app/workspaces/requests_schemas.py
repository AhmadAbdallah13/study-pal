from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
    name: str


class GetWorkspaceRequest(BaseModel):
    username: str
    password: str


class WorkspaceOut(CreateWorkspaceRequest):
    id: int

    class Config:
        orm_mode = True
