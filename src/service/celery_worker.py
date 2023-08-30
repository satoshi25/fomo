from typing import List
from datetime import date

from celery_config import celery_task
from service.article import ScrapArticle
from schema.scrap import ArticleModel


@celery_task.task
def scrap_article_task() -> List[dict]:
    scrap_data = ScrapArticle().scrap_articles()

    data = []
    for articles in scrap_data:
        journal = list(articles.keys())[0]
        for article in articles[journal]:
            publish_date = date.fromisoformat(article.get("publish_date"))
            converted_article = ArticleModel(
                title=article.get("title"),
                image=article.get("image"),
                journal=article.get("journal"),
                url=article.get("url"),
                view=article.get("view"),
                publish_date=publish_date
            )
            data.append(converted_article.dict())

    return data
