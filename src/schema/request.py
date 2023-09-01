from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str


class ArticleRequest(BaseModel):
    title: str
    image: str
    journal: str
    url: str
    view: int
    publish_date: str
