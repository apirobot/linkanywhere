from django.db import models
from django.utils.translation import ugettext as _

from behaviors.querysets import PublishedQuerySet

from .constants import DRAFT, PUBLISHED, PUBLICATION_STATUS_CHOICES


class Published(models.Model):
    publication_status = models.CharField(
        _('publication status'),
        max_length=1,
        choices=PUBLICATION_STATUS_CHOICES,
        default=DRAFT
    )

    objects = PublishedQuerySet.as_manager()
    publications = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True

    @property
    def is_draft(self):
        return self.publication_status == DRAFT

    @property
    def is_published(self):
        return self.publication_status == PUBLISHED
