from pydantic import BaseModel
from typing import List
from datetime import date


class ArticleSchema(BaseModel):
    id: int
    title: str
    image: str
    journal: str
    url: str
    view: int
    publish_date: date

    class Config:
        orm_mode = True


class ArticleListRankSchema(BaseModel):
    articles: List[ArticleSchema]


class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class JWTSchema(BaseModel):
    access_token: str
