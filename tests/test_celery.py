from app.core.celery_app import celery_app, test_resilience_task


def test_celery_application_config():
    assert celery_app.main == "resilience_worker"

    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.timezone == "UTC"
    assert celery_app.conf.task_track_started is True


def test_celery_resilience_task_execution():
    result = test_resilience_task()
    assert result == "Platform resilience check: OK"
