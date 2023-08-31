from fastapi import FastAPI, Depends, HTTPException
from typing import List
from datetime import date

from schema.request import UserRequest
from schema.response import ArticleListRankSchema, ArticleSchema, UserSchema
from database.repository import ArticleRepository, UserRepository
from database.orm import Article, User

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
    articles: List[Article] | None = article_repo.get_rank_articles(publish_date=publish_date)
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
    articles: List[Article] | None = article_repo.get_rank_journal_articles(
        publish_date=publish_date, journal=journal
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


@app.get("/articles/{publish_date}/journal-rank-1", status_code=200)
def get_journal_rank_1_articles_handler(
    publish_date: str,
    article_repo: ArticleRepository = Depends(),
) -> ArticleListRankSchema:

    publish_date: date = date.fromisoformat(publish_date)
    articles: List[Article] | None = article_repo.get_rank_journal_rank_1_articles(publish_date=publish_date)
    if not articles:
        raise HTTPException(status_code=404, detail="Articles Not Found")

    return ArticleListRankSchema(
        articles=[
            ArticleSchema.from_orm(article) for article in articles
        ]
    )


@app.get("/articles/", status_code=200)
def get_search_articles_handler(
    publish_date: str | None = None,
    journal: str | None = None,
    title: str | None = None,
    article_repo: ArticleRepository = Depends()
) -> ArticleListRankSchema:

    if publish_date:
        publish_date: date = date.fromisoformat(publish_date)
    articles: List[Article] | None = article_repo.get_search_articles(
        publish_date=publish_date,
        journal=journal,
        title=title,
    )
    if not articles:
        raise HTTPException(status_code=404, detail="Articles Not Found")

    return ArticleListRankSchema(
        articles=[
            ArticleSchema.from_orm(article) for article in articles
        ]
    )


@app.post("/user/signup", status_code=201)
def create_user_handler(
    request: UserRequest,
    user_repo: UserRepository = Depends()
) -> UserSchema:

    user: User | None = user_repo.get_user_by_username(username=request.username)
    if user:
        raise HTTPException(status_code=400, detail="User already exist")

    user: User = User(username=request.username, password=request.password)
    user: User = user_repo.save_user(user=user)

    return UserSchema.from_orm(user)
