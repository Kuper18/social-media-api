from django.db import models


class ResetPassword(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)
