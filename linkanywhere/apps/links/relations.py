from rest_framework import serializers

from .models import Tag


class TagRelatedField(serializers.RelatedField):

    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):
        tag, is_created = Tag.objects.get_or_create(name=data)
        return tag

    def to_representation(self, value):
        return value.name
