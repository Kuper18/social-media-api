from rest_framework import serializers

from user_profile.models import Profile


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
        )
        read_only_fields = (
            "id",
            "avatar",
            "created_at",
        )

    def validate(self, attrs):
        user = self.context["request"].user

        is_profile = Profile.objects.filter(user=user).exists()

        if is_profile and self.instance is None:
            raise serializers.ValidationError("You already have a profile.")

        return attrs


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "avatar",
            "city",
            "created_at",
        )


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        source="user.first_name", read_only=True
    )
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    followers = serializers.IntegerField(read_only=True)
    following = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "nickname",
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "city",
            "country",
            "education",
            "birth_date",
            "followers",
            "following",
            "created_at",
        )


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "avatar")
