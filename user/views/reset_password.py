from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import (
    default_token_generator,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import ResetPassword
from user.serializers.reset_password import ResetPasswordSerializer


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, token: str):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]
        reset_token = ResetPassword.objects.filter(token=token).first()

        user = (
            get_user_model().objects.filter(email=reset_token.email).first()
            if reset_token
            else None
        )
        if not user or not default_token_generator.check_token(
            user, token=token
        ):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])
        ResetPassword.objects.filter(email=user.email).delete()

        return Response(
            {"detail": "Password reset."}, status=status.HTTP_200_OK
        )
