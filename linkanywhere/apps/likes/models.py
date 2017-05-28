from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='likes', verbose_name=_('user')
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('created')
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')
        unique_together = ('content_type', 'object_id', 'user')
