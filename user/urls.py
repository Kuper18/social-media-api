from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import ConfirmEmailView, CreateUserView, ResendConfirmationView

urlpatterns = (
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("login/", TokenObtainPairView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "verify/<uuid:pk>/",
        ConfirmEmailView.as_view(),
        name="verify-user",
    ),
    path(
        "resend/verification/",
        ResendConfirmationView.as_view(),
        name="resend-verify-user",
    ),
)

app_name = "user"
