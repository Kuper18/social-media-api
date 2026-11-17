from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import EmailConfirmationToken
from user.serializers.resend_confirmation_token import (
    ResendConfirmationTokenSerializer,
)
from user.tasks import send_confirmation_email


class ConfirmEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, pk) -> Response:
        token = (
            EmailConfirmationToken.objects.filter(pk=pk)
            .select_related("user")
            .first()
        )

        if token is None:
            return self._get_400_response()

        if token.is_expired:
            token.delete()
            return self._get_400_response()

        user = token.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])
        token.delete()

        return Response(
            {"detail": "Email confirmed."}, status=status.HTTP_200_OK
        )

    @staticmethod
    def _get_400_response() -> Response:
        return Response(
            {"detail": "Invalid or expired token."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResendConfirmationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendConfirmationTokenSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = (
            get_user_model()
            .objects.filter(email=email, is_verified=False)
            .first()
        )

        if user:
            user.email_confirmation_token.all().delete()
            token = EmailConfirmationToken.objects.create(user=user)
            send_confirmation_email.delay_on_commit(
                user_email=user.email,
                token_id=token.pk,
                user_first_name=user.first_name,
            )

        return Response(
            {"detail": "If the account exists, an email was sent."},
            status=status.HTTP_200_OK,
        )
