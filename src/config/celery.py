import os
from datetime import timedelta
from celery.schedules import crontab, solar
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # Каждые 3 минуты 40 секунд
    'every-3min-40sec': {
        'task': 'task_manager.tasks.scheduled_task_every_3_min_40_sec',
        'schedule': timedelta(minutes=3, seconds=40),
    },
    # 3 раза с 19 по 21 число, каждый час
    'limited-dates-task': {
        'task': 'task_manager.tasks.scheduled_task_limited_times',
        'schedule': crontab(
            hour='*',  # каждый час
            day_of_month='19-21',  # с 19 по 21 число
            minute='0'
        ),
        'args': (),
        'kwargs': {},
    },
    # Каждый день на восходе солнца
    'sunrise-greeting': {
        'task': 'task_manager.tasks.solar_sunrise_greeting',
        'schedule': solar('sunrise', 53.9045, 27.5615),  # Минск
    },
    # Еженедельная рассылка по понедельникам в 9:00
    'weekly-newsletter': {
        'task': 'task_manager.tasks.weekly_email_newsletter',
        'schedule': crontab(day_of_week=1, hour=9, minute=0),  # Понедельник, 9:00
    },
}

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')