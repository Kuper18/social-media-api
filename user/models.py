import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from config import settings
from user.managers import UserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_conformation_token",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    _TOKEN_LIFETIME = timedelta(hours=24)

    def __str__(self):
        return str(self.created_at)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + self._TOKEN_LIFETIME
