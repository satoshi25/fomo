from fastapi import FastAPI, Depends, HTTPException
from typing import List
from datetime import date

from schema.response import ArticleListRankSchema, ArticleSchema
from database.repository import ArticleRepository

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"message": "hello world"}


@app.get("/articles/{publish_date}/rank", status_code=200)
def get_rank_articles_handler(
    publish_date: str,
    article_repo: ArticleRepository = Depends()
) -> ArticleListRankSchema:

    publish_date: date = date.fromisoformat(publish_date)
    articles: List[ArticleSchema] | None = article_repo.get_rank_articles(publish_date=publish_date)
    if not articles:
        raise HTTPException(status_code=404, detail="Articles Not Found")

    return ArticleListRankSchema(
        articles=[
            ArticleSchema.from_orm(article) for article in sorted(
                articles,
                key=lambda el: el.view, reverse=True
            )[:10]
        ]
    )


@app.get("/articles/{publish_date}/{journal}/rank", status_code=200)
def get_rank_journal_articles_handler(
    publish_date: str,
    journal: str,
    article_repo: ArticleRepository = Depends(),
) -> ArticleListRankSchema:

    publish_date: date = date.fromisoformat(publish_date)
    articles: List[ArticleSchema] | None = article_repo.get_rank_journal_articles(
        publish_data=publish_date, journal=journal
    )
    if not articles:
        raise HTTPException(status_code=404, detail="Articles Not Found")

    return ArticleListRankSchema(
        articles=[
            ArticleSchema.from_orm(article) for article in sorted(
                articles,
                key=lambda el: el.view, reverse=True
            )[:10]
        ]
    )
