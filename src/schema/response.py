from pydantic import BaseModel
from typing import List
from datetime import date


class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    journal: str
    url: str
    view: int
    publish_date: date

    class Config:
        orm_mode = True


class ArticleListRankSchema(BaseModel):
    articles: List[ArticleSchema]
