from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class VerifiedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise exceptions.AuthenticationFailed(
                "Email is not verified. Please verify your email and try again.",
                code="email_not_verified",
            )

        return data
