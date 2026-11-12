from django.conf import settings
from django.core.mail import send_mail

from user.models import EmailConfirmationToken, User


def send_confirmation_email(user: User, token: EmailConfirmationToken) -> None:
    link = f"{settings.FRONTEND_URL}/confirm-email/{token.pk}/"

    send_mail(
        subject="Confirm your email",
        message=f"Hi {user.first_name},\n\nConfirm your email by opening this link:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
