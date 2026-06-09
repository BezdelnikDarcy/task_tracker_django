from celery import shared_task
import time
from account.models import User


@shared_task
def add(x, y):
    import time
    time.sleep(5)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def scheduled_task_every_3_min_40_sec():
    #Выполняется каждые 3 минуты 40 секунд
    print(f"Task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return f"Scheduled task completed at {time.strftime('%H:%M:%S')}"


@shared_task
def scheduled_task_limited_times():
    #Выполняется 3 раза с 19 по 21 число каждый час
    print(f"Limited task executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return f"Limited task completed"

@shared_task
def solar_sunrise_greeting():
    #Отправляет приветствие на восходе солнца
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        print(f"🌅 Good morning {admin.username}! The sun has risen!")
        # Здесь реальная отправка email
    return "Sunrise greetings sent"

@shared_task
def weekly_email_newsletter():
    #Еженедельная рассылка email
    users = User.objects.filter(is_active=True)
    for user in users:
        print(f"📧 Weekly newsletter sent to {user.email}")
        # Здесь реальная отправка email
    return f"Weekly newsletter sent to {users.count()} users"