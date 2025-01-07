from django.urls import path
from rest_framework.routers import SimpleRouter
from users.views import CustomUserViewSet, CustomUserCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig


app_name = UsersConfig.name

router = SimpleRouter()
router.register("users", CustomUserViewSet, basename="user")


urlpatterns = [
    path("register/", CustomUserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh")
]

urlpatterns += router.urls
