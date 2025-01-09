from django.urls import path
from rest_framework.routers import SimpleRouter
from habits.views import HabitViewSet, PublicHabitListAPIView

from habits.apps import HabitsConfig


app_name = HabitsConfig.name


router = SimpleRouter()
router.register("", HabitViewSet, basename="habit")

urlpatterns = [
    path("public_habit/", PublicHabitListAPIView.as_view(), name="public_habit"),
] + router.urls
