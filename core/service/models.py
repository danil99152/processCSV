from pydantic import BaseModel


class FileModel(BaseModel):
    userId: int
    title: str
    body: str


class Result(BaseModel):
    postId: int
    result: str
    userId: int


class FileProcessStatus(BaseModel):
    status: str
    result: list[Result] = None
