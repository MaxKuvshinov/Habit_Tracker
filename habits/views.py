from rest_framework import viewsets, generics

from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer
from habits.models import Habit
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner, IsAuthenticated]
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class PublicHabitListAPIView(generics.ListAPIView):
    queryset = Habit.objects.filter(sign_of_publicity=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator
