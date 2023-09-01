from fastapi import FastAPI, Depends, HTTPException
from typing import List
from datetime import date

from schema.request import UserRequest, ArticleRequest
from schema.response import ArticleListRankSchema, ArticleSchema, UserSchema, JWTSchema
from database.repository import ArticleRepository, UserRepository
from database.orm import Article, User
from security import get_access_token
from service.user import UserService

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


@app.post("/article", status_code=201)
def create_article_handler(
    request: ArticleRequest,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    article_repo: ArticleRepository = Depends(),
) -> ArticleSchema:

    validate: str | None = user_service.verify_token(access_token=access_token)
    if not validate:
        raise HTTPException(status_code=401, detail="Token Has Expired")

    publish_date: date = date.fromisoformat(request.publish_date)
    articles: List[Article] = article_repo.get_search_articles(
        title=request.title,
        journal=request.journal,
        publish_date=publish_date
    )
    if len(articles) > 0:
        raise HTTPException(status_code=400, detail="Bad Request")

    article: Article = article_repo.save_article(
        Article(
            title=request.title,
            image=request.image,
            journal=request.journal,
            url=request.url,
            view=request.view,
            publish_date=publish_date
        )
    )

    return ArticleSchema.from_orm(article)


@app.post("/user/signup", status_code=201)
def create_user_handler(
    request: UserRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
) -> UserSchema:

    user: User | None = user_repo.get_user_by_username(username=request.username)
    if user:
        raise HTTPException(status_code=400, detail="User Already Exist")

    hashed_password: str = user_service.hash_password(password=request.password)

    user: User = User(username=request.username, password=hashed_password)
    user: User = user_repo.save_user(user=user)

    return UserSchema.from_orm(user)


@app.post("/user/login", status_code=200)
def login_user_handler(
    request: UserRequest,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
):

    user: User | None = user_repo.get_user_by_username(username=request.username)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    verified: bool = user_service.verify_password(password=request.password, hashed_password=user.password)

    if not verified:
        raise HTTPException(status_code=401, detail="Not Authorized")

    access_token: str = user_service.create_jwt(username=user.username)

    return JWTSchema(access_token=access_token)
