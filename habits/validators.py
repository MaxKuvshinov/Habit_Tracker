from rest_framework.exceptions import ValidationError


class AssociatedHabitOrRewardValidator:
    """Валидатор: использованиt связанной привычки и вознаграждения"""

    def __init__(self, associated_habit_field, reward_field):
        self.associated_habit_field = associated_habit_field
        self.reward_field = reward_field

    def __call__(self, attrs):
        associated_habit = attrs.get(self.associated_habit_field)
        reward = attrs.get(self.reward_field)

        if associated_habit and reward:
            raise ValidationError(
                "Одновременное использование связанной привычки и вознаграждения недопустимо."
            )


class TimeToCompleteValidator:
    """Валидатор: временя выполнения привычки"""

    def __init__(self, time_to_complete_field):
        self.time_to_complete_field = time_to_complete_field

    def __call__(self, attrs):
        time_to_complete = attrs.get(self.time_to_complete_field)

        if time_to_complete is not None and int(time_to_complete) > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд"
            )


class AssociatedHabitNotPleasantValidator:
    """Валидатор: связанная привычка должна быть приятной"""

    def __init__(self, associated_habit_field):
        self.associated_habit_field = associated_habit_field

    def __call__(self, attrs):
        associated_habit = attrs.get(self.associated_habit_field)

        if associated_habit and not associated_habit.sign_of_a_pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной")


class PleasantHabitNotRewardOrAssociatedHabitValidator:
    """Валидатор: приятная привычка не может быть связанной и не имеет вознаграждения"""

    def __init__(
        self, sign_of_a_pleasant_habit_field, associated_habit_field, reward_field
    ):
        self.sign_of_a_pleasant_habit_field = sign_of_a_pleasant_habit_field
        self.associated_habit_field = associated_habit_field
        self.reward_field = reward_field

    def __call__(self, attrs):
        sign_of_a_pleasant_habit = attrs.get(self.sign_of_a_pleasant_habit_field)
        associated_habit = attrs.get(self.associated_habit_field)
        reward = attrs.get(self.reward_field)

        if sign_of_a_pleasant_habit and (associated_habit or reward):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )


class DoingHabitAtLeastOnceAWeekValidator:
    """Валидатор: Периодичность выполнения привычки"""

    def __init__(self, periodicity_field):
        self.periodicity_field = periodicity_field

    def __call__(self, attrs):
        periodicity = attrs.get(self.periodicity_field)

        valid_periodicity = [
            "every minute",
            "every hour",
            "every day",
            "every other day",
            "once every three days",
            "once every four days",
            "once every five days",
            "once every six days",
            "once a week",
        ]

        if periodicity not in valid_periodicity:
            raise ValidationError(
                "Привычка должна выполняться не реже одного раза в неделю и не реже чем раз в 7 дней."
            )
