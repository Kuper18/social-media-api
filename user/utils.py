import os
import uuid

from django.utils.text import slugify

from user.models import Profile


def generate_avatar_path(instance: Profile, filename: str) -> str:
    _, extension = os.path.splitext(filename)

    return f"avatars/{slugify(instance.nickname)}-{uuid.uuid4()}.{extension}"
