from typing import List

from celery_config import celery_task
from service.article import ScrapArticle


@celery_task.task
def scrap_article_task() -> List[dict]:
    print("scrap_article_task 시작.")
    data = ScrapArticle().scrap_articles()
    return data
