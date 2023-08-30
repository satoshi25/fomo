from pydantic import BaseModel
from datetime import date


class ArticleModel(BaseModel):
    title: str
    image: str
    journal: str
    url: str
    view: int
    publish_date: date
