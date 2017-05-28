from django.db import models
from django.db.transaction import atomic
from django.contrib.contenttypes.models import ContentType

from linkanywhere.apps.users.models import User
from .models import Like


def add_like(obj: models.Model, user: User) -> Like:
    """Add a like to an object.

    If the user has already liked the object nothing happens,
    so this function can be considered idempotent.

    :param obj: Any Django model instance.
    :param user: User adding the like.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    with atomic():
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=user
        )

    return like


def remove_like(obj: models.Model, user: User) -> None:
    """Remove an user like from an object.

    If the user has not liked the object nothing happens,
    so this function can be considered idempotent.

    :param obj: Any Django model instance.
    :param user: User removing his like.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    with atomic():
        qs = Like.objects.filter(content_type=obj_type, object_id=obj.id,
                                 user=user)
        if not qs.exists():
            return
        qs.delete()
