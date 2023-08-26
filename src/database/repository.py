from fastapi import Depends
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import date

from database.connection import get_db
from database.orm import Article


class ArticleRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_rank_articles(self, publish_date: date) -> List[Article] | None:

        articles: List[Article] | None = list(
            self.session.scalars(select(Article).where(Article.publish_date == publish_date))
        )

        return articles
