from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

from config import settings


class Follower(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("follower", "following"),
                name="unique_follow_relationship",
            ),
            CheckConstraint(
                condition=~Q(follower=F("following")),
                name="prevent_self_follow",
            ),
        )

    def __str__(self):
        return str(self.created_at)
