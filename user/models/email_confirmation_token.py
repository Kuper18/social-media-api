import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone

from config import settings


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_confirmation_token",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    _TOKEN_LIFETIME = timedelta(hours=24)

    def __str__(self):
        return str(self.created_at)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + self._TOKEN_LIFETIME
