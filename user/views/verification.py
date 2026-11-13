from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import EmailConfirmationToken
from user.utils import send_confirmation_email


class ConfirmEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, pk) -> Response:
        token = get_object_or_404(
            EmailConfirmationToken.objects.select_related("user"),
            pk=pk,
        )

        if token.is_expired:
            token.delete()
            return Response(
                {"detail": "Token expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = token.user
        user.is_verified = True
        user.save()
        token.delete()

        return Response(
            {"detail": "Email confirmed."}, status=status.HTTP_200_OK
        )


class ResendConfirmationView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        email = request.data.get("email", None)

        if email is None:
            return Response(
                {"detail": "Please provide an email address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = (
            get_user_model()
            .objects.filter(email=email, is_verified=False)
            .first()
        )

        if user:
            user.email_confirmation_token.all().delete()
            token = EmailConfirmationToken.objects.create(user=user)
            send_confirmation_email(user, token)

        return Response(
            {"detail": "If the account exists, an email was sent."},
            status=status.HTTP_200_OK,
        )
