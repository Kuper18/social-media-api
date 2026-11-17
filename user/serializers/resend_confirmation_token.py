from rest_framework import serializers


class ResendConfirmationTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
