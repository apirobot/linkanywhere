from django.db.transaction import atomic
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from rest_framework.compat import is_authenticated

from .models import Like


def add_like(obj, user):
    """Add a like to an object.

    If the user has already liked the object nothing happens,
    so this function can be considered idempotent.

    :param obj: Any Django model instance.
    :param user: User adding the like. :class:`~linkanywhere.apps.users.models.User` instance.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    with atomic():
        like, is_created = Like.objects.get_or_create(
            content_type=obj_type, object_id=obj.id, user=user
        )

    return like


def remove_like(obj, user):
    """Remove an user like from an object.

    If the user has not liked the object nothing happens,
    so this function can be considered idempotent.

    :param obj: Any Django model instance.
    :param user: User removing his like. :class:`~linkanywhere.apps.users.models.User` instance.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    with atomic():
        qs = Like.objects.filter(content_type=obj_type, object_id=obj.id,
                                 user=user)
        if not qs.exists():
            return
        qs.delete()


def get_liked(model, user_or_id):
    """Get the objects liked by an user.

    :param user_or_id: :class:`~linkanywhere.apps.users.models.User` instance or id.
    :param model: Show only objects of this kind. Can be any Django model class.

    :return: Queryset of objects representing the likes of the user.
    """
    obj_type = ContentType.objects.get_for_model(model)

    if isinstance(user_or_id, get_user_model()):
        user_id = user_or_id.id
    else:
        user_id = user_or_id

    return model.objects.filter(likes__user_id=user_id,
                                likes__content_type=obj_type)


def is_fan(obj, user):
    """Check whether a `user` has liked an `obj` or not.

    :param obj: Any Django model instance.
    :param user: :class:`~linkanywhere.apps.users.models.User` instance.

    :return: True or False
    """
    if not is_authenticated(user):
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()
