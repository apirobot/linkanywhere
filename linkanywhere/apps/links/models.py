import uuid

from django.db import models

from behaviors.behaviors import Slugged, Timestamped


class Category(Slugged, models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    @property
    def slug_source(self):
        return self.name


class Link(Timestamped, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    category = models.ForeignKey(
        'links.Category', on_delete=models.CASCADE, related_name='links'
    )

    def __str__(self):
        return '{0}: {1}'.format(self.title, self.url)
