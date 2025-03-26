from pydantic import BaseModel


class CreateWorkspaceRequest(BaseModel):
    name: str


class GetWorkspaceRequest(BaseModel):
    username: str
    password: str
