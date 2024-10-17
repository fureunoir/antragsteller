from celery import Celery
from os import getenv

# Celery configuration
REDIS_URL = getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "antragsteller",
    broker=REDIS_URL,  # Redis is used as the broker
    backend=REDIS_URL,  # Redis is used as the result backend
)

# Celery configuration
celery_app.conf.update(
    result_expires=3600,  # Set expiration time for task results (optional)
    timezone="UTC",  # Use UTC for time zone (adjust if needed)
    beat_schedule={
        "example_task": {
            "task": "src.tasks.sample_task",
            "schedule": 10.0,  # Run the task every 10 seconds
        },
    },
)

# Automatically discover tasks in the 'app.tasks' module
celery_app.autodiscover_tasks(["src.tasks"])
