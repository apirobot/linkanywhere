import uuid

from django.db import models

from linkanywhere.apps.base.behaviors import Published


class TestModel(models.Model):
    """
    Base for test models that sets app_label, so they play nicely.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        app_label = 'tests'
        abstract = True


class BasicModel(TestModel):
    text = models.CharField(max_length=100)


class LikeModel(TestModel):
    text = models.CharField(max_length=100)


class PublishedModel(Published, TestModel):
    pass
