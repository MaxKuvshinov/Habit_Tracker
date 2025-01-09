from celery import shared_task
from habits.models import Habit
from habits.services import send_message_telegram
from config import settings
from django.utils.timezone import now


@shared_task()
def send_time_reminder():
    """Напоминание о выполнени привычки в TG."""
    current_time = now()
    habits = Habit.objects.filter(owner__telegram_id__isnull=False).select_related("owner")

    for habit in habits:
        if habit.time <= current_time:
            telegram_id = habit.owner.telegram_id

            if habit.place:
                message = (
                    f"Не забудьте про {habit.action} в {habit.place}."
                    if habit.place else f"Не забудьте про {habit.action}."
                )

            send_message_telegram(telegram_id, message)
            habit.time += habit.get_periodicity_timedelta()
            habit.save()
