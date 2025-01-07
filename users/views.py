from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from users.serializers import CustomUserSerializer
from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserCreateAPIView(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
