import uuid

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import ugettext as _

from behaviors.behaviors import Published, Timestamped

from linkanywhere.apps.likes.models import Like
from .constants import DRAFT, PUBLISHED


class Link(Published, Timestamped, models.Model):

    PUBLICATION_STATUS_CHOICES = (
        (DRAFT, _('draft')),
        (PUBLISHED, _('published')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='links'
    )
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    likes = GenericRelation(Like)
    category = models.ForeignKey(
        'categories.Category', on_delete=models.CASCADE, related_name='links'
    )
    tags = models.ManyToManyField(
        'tags.Tag', related_name='links'
    )
    publication_status = models.CharField(
        max_length=1,
        choices=PUBLICATION_STATUS_CHOICES, default=DRAFT
    )

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.url)

    @property
    def total_likes(self):
        return self.likes.count()
