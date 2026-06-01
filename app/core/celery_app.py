from celery import Celery
from app.config import settings

celery_app = Celery(
    "resilience_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True
)

@celery_app.task(name="app.core.celery_app.test_resilience_task")
def test_resilience_task():
    return "Platform resilience check: OK"