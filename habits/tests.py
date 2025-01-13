from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import CustomUser


class HabitApiTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="usertest@sky.pro")
        self.habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-07 08:00",
            action="Test action",
            periodicity="every day",
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тест создания привычки"""
        data = {
            "time": "2024-12-07 09:00",
            "action": "Test action",
            "periodicity": "every day",
        }
        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_with_unpleasant_associated_habit(self):
        """Тестирование отношения между приятной привычкой и связанной"""
        associated_habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-07 08:00",
            action="Unpleasant Habit",
            periodicity="every day",
            time_to_complete=1,
            sign_of_a_pleasant_habit=False,
        )
        data = {
            "time": "2024-12-07 09:00",
            "action": "Test action",
            "periodicity": "every day",
            "time_to_complete": 1,
            "associated_habit": associated_habit.pk,
        }

        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Связанная привычка должна быть приятной", str(response.json()))

    def test_habit_create_with_associated_habit_and_reward(self):
        """Тестирование использование приятной привычки и вознаграждения"""
        associated_habit = Habit.objects.create(
            owner=self.user,
            time="2024-12-07 08:00",
            action="associated_habit",
            periodicity="every day",
            time_to_complete=1,
            sign_of_a_pleasant_habit=True,
        )

        data = {
            "time": "2024-12-07 09:00",
            "action": "Test action",
            "periodicity": "every day",
            "time_to_complete": 1,
            "associated_habit": associated_habit.pk,
            "reward": "test reward",
        }

        response = self.client.post("/habits/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Одновременное использование связанной привычки и вознаграждения недопустимо.",
            str(response.json()),
        )

    def test_habit_create_with_time_to_complete(self):
        """Тестирование время выполнения привычки"""
        data = {
            "time": "2024-12-07 09:00",
            "action": "Test action",
            "periodicity": "every day",
            "time_to_complete": 200,
        }

        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения привычки не должно превышать 120 секунд",
            str(response.json()),
        )

    def test_habit_create_with_a_pleasant_habit_and_reward(self):
        """Тестирование отсутствия связанной привычки и вознаграждения"""
        data = {
            "time": "2024-12-07 09:00",
            "action": "Test action",
            "periodicity": "every day",
            "time_to_complete": 1,
            "sign_of_a_pleasant_habit": True,
            "reward": "test reward",
        }

        response = self.client.post("/habits/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "У приятной привычки не может быть вознаграждения или связанной привычки.",
            str(response.json()),
        )

    def test_habit_retrieve(self):
        """Тест просмотра"""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_update(self):
        "Тест обновления"
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"action": "Test action 2", "periodicity": "every day"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Test action 2")

    def test_habit_delete(self):
        """Тест удаления"""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
