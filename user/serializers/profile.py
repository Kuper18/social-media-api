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

    def validate(self, attrs):
        user = self.context["request"].user

        is_profile = Profile.objects.filter(user=user).exists()

        if is_profile and self.instance is None:
            raise serializers.ValidationError("You already have a profile.")

        return attrs


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "avatar")
