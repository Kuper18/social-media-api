from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import ResetPassword
from user.serializers import ForgotPasswordSerializer
from user.tasks import send_password_reset_email


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = get_user_model().objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)

            with transaction.atomic():
                ResetPassword.objects.filter(email=email).delete()
                ResetPassword.objects.create(email=email, token=token)
                send_password_reset_email.delay_on_commit(
                    token=token,
                    user_email=email,
                )

        return Response(
            {
                "detail": "If an account exists, we sent you an email to reset your password."
            },
            status=status.HTTP_200_OK,
        )
