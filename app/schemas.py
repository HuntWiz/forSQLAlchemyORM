from pydantic import BaseModel


class CreatePost(BaseModel):
    title: str
    content: str
    tags_id: list[int] = []


class UpdatePost(BaseModel):
    title: str
    content: str
    tags_id: list[int] = []


class CreateTag(BaseModel):
    title: str


class UpdateTag(BaseModel):
    title: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True