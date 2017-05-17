import uuid

from django.db import models

from model_utils.models import TimeStampedModel


class Link(TimeStampedModel, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.url)
