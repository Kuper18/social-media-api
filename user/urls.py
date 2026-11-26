from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from user.views import (
    ConfirmEmailView,
    CreateUserView,
    ForgotPasswordView,
    LoginView,
    ResendConfirmationView,
    ResetPasswordView,
)

urlpatterns = (
    path("register/", CreateUserView.as_view(), name="create-user"),
    path("login/", LoginView.as_view(), name="login-user"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "verify/<uuid:pk>/",
        ConfirmEmailView.as_view(),
        name="verify-user",
    ),
    path(
        "resend-verification/",
        ResendConfirmationView.as_view(),
        name="resend-verify-user",
    ),
    path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
)

app_name = "user"
