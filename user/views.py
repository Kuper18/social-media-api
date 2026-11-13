from django.db import transaction
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import EmailConfirmationToken
from user.serializers import UserSerializer
from user.utils import send_confirmation_email


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = EmailConfirmationToken.objects.create(user=user)

        send_confirmation_email(user, token)

        return Response(
            {"detail": "Account created. Check your email to confirm it."},
            status=status.HTTP_201_CREATED,
        )


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
        user.is_active = True
        user.save()
        token.delete()

        return Response(
            {"detail": "Email confirmed."}, status=status.HTTP_200_OK
        )
