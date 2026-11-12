from django.db import transaction
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
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
    pass
