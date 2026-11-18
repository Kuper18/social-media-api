from rest_framework import serializers

from user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "avatar",
            "bio",
            "city",
            "country",
            "education",
            "birth_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "avatar",
            "created_at",
            "updated_at",
        )


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "avatar")
