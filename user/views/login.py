from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import VerifiedTokenObtainPairSerializer


class LoginView(TokenObtainPairView):
    serializer_class = VerifiedTokenObtainPairSerializer
    throttle_scope = "login"
