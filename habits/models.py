from django.db import models
from users.models import CustomUser
import datetime
from enum import Enum


class Periodicity(Enum):
    EVERY_MINUTE = "every minute"
    EVERY_HOUR = "every hour"
    EVERY_DAY = "every day"
    EVERY_OTHER_DAY = "every other day"
    ONCE_EVERY_THREE_DAYS = "once every three days"
    ONCE_EVERY_FOUR_DAYS = "once every four days"
    ONCE_EVERY_FIVE_DAYS = "once every five days"
    ONCE_EVERY_SIX_DAYS = "once every six days"
    ONCE_A_WEEK = "once a week"


class Habit(models.Model):

    # OWNER_CHOICES = [
    #     ("every minute", "каждую минуту"),
    #     ("every hour", "каждый час"),
    #     ("every day", "каждый день"),
    #     ("every other day", "через день"),
    #     ("once every three days", "раз в 3 дня"),
    #     ("once every four days", "раз в 4 дня"),
    #     ("once every five days", "раз в 5 дня"),
    #     ("once every six days", "раз в 6 дня"),
    #     ("once a week", "раз в неделю"),
    # ]

    owner = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=50,
        verbose_name="Место выполнения привычки",
        blank=True,
        null=True,
        help_text="Укажите место выполнения привычки",
    )
    time = models.DateTimeField(
        verbose_name="Время выполнения привычки",
        blank=True,
        null=True,
        help_text="Укажите время выполнения привычки",
    )
    action = models.CharField(
        max_length=150,
        verbose_name="Действие привычки",
        blank=True,
        null=True,
        help_text="Укажите необходимое действие привычки",
    )
    sign_of_a_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Приятная привычка",
    )
    associated_habit = models.ForeignKey(
        "self",
        verbose_name="Связанная привычка",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Укажите приятную связанную привычку",
    )
    periodicity = models.CharField(
        max_length=50,
        verbose_name="Периодичность выполнения привычки",
        choices=[(tag.value, tag.value) for tag in Periodicity],
        default=Periodicity.EVERY_DAY.value,
        help_text="Укажите периодичность выполнения",
    )
    reward = models.CharField(
        max_length=150,
        verbose_name="Вознаграждение",
        blank=True,
        null=True,
        help_text="Укажите вознаграждение",
    )
    time_to_complete = models.IntegerField(
        default=1,
        verbose_name="Время на выполнение",
        help_text="Укажите предположительно потраченное время на привычку",
    )
    sign_of_publicity = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Опубликовать для общего доступа",
    )

    def __str__(self):
        return f"Привычка: {self.action}, место:{self.place}, время: {self.time}"

    def get_periodicity_timedelta(self):
        """Метод получения интервала времени для периодичности"""
        periodicity_map = {
            Periodicity.EVERY_MINUTE: datetime.timedelta(minutes=1),
            Periodicity.EVERY_HOUR: datetime.timedelta(hours=1),
            Periodicity.EVERY_DAY: datetime.timedelta(days=1),
            Periodicity.EVERY_OTHER_DAY: datetime.timedelta(days=2),
            Periodicity.ONCE_EVERY_THREE_DAYS: datetime.timedelta(days=3),
            Periodicity.ONCE_EVERY_FOUR_DAYS: datetime.timedelta(days=4),
            Periodicity.ONCE_EVERY_FIVE_DAYS: datetime.timedelta(days=5),
            Periodicity.ONCE_EVERY_SIX_DAYS: datetime.timedelta(days=6),
            Periodicity.ONCE_A_WEEK: datetime.timedelta(weeks=1),
        }
        try:
            periodicity_enum = Periodicity(self.periodicity)
            return periodicity_map.get(periodicity_enum, None)
        except ValueError:
            return None

    # def get_periodicity_timedelta(self):
    #     if self.periodicity == "every minute":
    #         return datetime.timedelta(minutes=1)
    #     elif self.periodicity == "every hour":
    #         return datetime.timedelta(hours=1)
    #     elif self.periodicity == "every day":
    #         return datetime.timedelta(days=1)
    #     elif self.periodicity == "every other day":
    #         return datetime.timedelta(days=2)
    #     elif self.periodicity == "once every three days":
    #         return datetime.timedelta(days=3)
    #     elif self.periodicity == "once every four days":
    #         return datetime.timedelta(days=4)
    #     elif self.periodicity == "once every five days":
    #         return datetime.timedelta(days=5)
    #     elif self.periodicity == "once every six days":
    #         return datetime.timedelta(days=6)
    #     elif self.periodicity == "once a week":
    #         return datetime.timedelta(weeks=1)
    #     else:
    #         return None

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
