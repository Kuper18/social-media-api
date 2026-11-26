from django.db import models
from django.db.models.functions import Lower

from config import settings
from user_profile.utils import generate_avatar_path


class Profile(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(blank=True, upload_to=generate_avatar_path)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("nickname"),
                name="unique_nickname_ci",
            )
        ]

    def __str__(self):
        return self.nickname
