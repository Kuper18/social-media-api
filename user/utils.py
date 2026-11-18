import os
import uuid

from django.utils.text import slugify


def generate_avatar_path(instance, filename: str) -> str:
    _, extension = os.path.splitext(filename)

    return f"avatars/{slugify(instance.nickname)}-{uuid.uuid4()}.{extension}"
