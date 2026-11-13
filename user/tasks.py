from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_confirmation_email(
    user_email: str, user_first_name: str, token_id: str
) -> None:
    link = f"{settings.FRONTEND_URL}/confirm-email/{token_id}/"

    send_mail(
        subject="Confirm your email",
        message=f"Hi {user_first_name},\n\nConfirm your email by opening this link:\n{link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
    )
