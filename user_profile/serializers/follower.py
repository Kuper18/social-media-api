from rest_framework import serializers

from user_profile.models import Follower


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = (
            "id",
            "following",
            "follower",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )

    def validate(self, attr):
        following = attr.get("following")
        follower = attr.get("follower")

        if following == follower:
            raise serializers.ValidationError("You can't follow yourself.")

        return attr
