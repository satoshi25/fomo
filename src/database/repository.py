from fastapi import Depends
from typing import List, Sequence
from sqlalchemy import select, func, desc
from sqlalchemy.engine.row import Row
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

    def get_rank_journal_articles(self, publish_date: date, journal: str) -> List[Article] | None:
        articles: List[Article] | None = list(
            self.session.scalars(
                select(Article).where(Article.publish_date == publish_date).where(Article.journal == journal)
            )
        )
        return articles

    def get_rank_journal_rank_1_articles(self, publish_date: date) -> List[Article] | None:

        sub_article = (
            select(
                Article,
                func.row_number().over(
                    partition_by=Article.journal,
                    order_by=desc(Article.view)
                ).label('rank')
            ).where(Article.publish_date == publish_date).subquery()
        )

        stmt = select(sub_article).where(sub_article.c.rank == 1).order_by(sub_article.c.view.desc())

        articles: Sequence[Row] | None = self.session.execute(stmt).fetchall()
        # articles 의 타입이 <class 'sqlalchemy.engine.row.Row'>를 담은 list 다.
        # 요소는 tuple 형태다.

        if not articles:
            articles = None
        else:
            articles = [
                Article(
                    id=article[0],
                    title=article[1],
                    image=article[2],
                    journal=article[3],
                    url=article[4],
                    view=article[5],
                    publish_date=article[6]
                )
                for article in articles
            ]

        return articles

    @staticmethod
    def save_articles(session: Session, articles: List[dict]) -> None:
        data = []
        for article in articles:
            row = {
                "title": article.get("title"),
                "image": article.get("image"),
                "journal": article.get("journal"),
                "url": article.get("url"),
                "view": article.get("view"),
                "publish_date": article.get("publish_date")
            }
            data.append(row)
        session.bulk_insert_mappings(Article, data)
        session.commit()
