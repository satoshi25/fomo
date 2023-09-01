from celery import Celery
from celery.schedules import crontab

from src.config import CELERY_BROKER, CELERY_BACKEND, HOUR, MINUTE

celery_task = Celery(
    "tasks",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
    include=["src.service.celery_worker"],
    broker_connection_retry_on_startup=True,
)

celery_task.conf.timezone = "Asia/Seoul"

celery_task.conf.beat_schedule = {
    "run-scrap-every-day": {
        "task": "src.service.celery_worker.scrap_and_save_pipeline_task",
        "schedule": crontab(hour=HOUR, minute=MINUTE),
    }
}
