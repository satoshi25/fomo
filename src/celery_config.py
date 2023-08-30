from celery import Celery
from celery.schedules import crontab


celery_task = Celery(
    "tasks",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0",
    include=["service.celery_worker"],
    broker_connection_retry_on_startup=True,
)

celery_task.conf.timezone = "Asia/Seoul"

celery_task.conf.beat_schedule = {
    "run-scrap-every-day": {
        "task": "service.celery_worker.scrap_and_save_pipeline_task",
        "schedule": crontab(hour="23", minute="0"),
    }
}
