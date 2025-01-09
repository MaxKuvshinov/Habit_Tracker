from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    help = "Создание суперпользователя с email и паролем"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email", type=str, required=True, help="Email для суперпользователя"
        )
        parser.add_argument(
            "--password", type=str, required=True, help="Пароль для суперпользователя"
        )

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        # Проверка email
        if not email or "@" not in email:
            self.stdout.write(self.style.ERROR("Некорректный email"))
            return

        # Проверка длины пароля
        if len(password) < 8:
            self.stdout.write(self.style.ERROR("Пароль слишком короткий."))
            return

        try:
            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(f"Пользователь с email {email} уже существует.")
                )
                return

            user = CustomUser(email=email)
            user.set_password(password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Суперпользователь с email:{email} успешно создан")
            )
        except ValidationError as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка при создании пользователя: {e}")
            )
