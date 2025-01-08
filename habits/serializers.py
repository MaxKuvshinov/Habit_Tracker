from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    AssociatedHabitOrRewardValidator,
    TimeToCompleteValidator,
    AssociatedHabitNotPleasantValidator,
    PleasantHabitNotRewardOrAssociatedHabitValidator,
    DoingHabitAtLeastOnceAWeekValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            AssociatedHabitOrRewardValidator(
                associated_habit_field="associated_habit", reward_field="reward"
            ),
            TimeToCompleteValidator(time_to_complete_field="time_to_complete"),
            AssociatedHabitNotPleasantValidator(
                associated_habit_field="associated_habit"
            ),
            PleasantHabitNotRewardOrAssociatedHabitValidator(
                sign_of_a_pleasant_habit_field="sign_of_a_pleasant_habit",
                associated_habit_field="associated_habit",
                reward_field="reward",
            ),
            DoingHabitAtLeastOnceAWeekValidator(periodicity_field="periodicity"),
        ]
