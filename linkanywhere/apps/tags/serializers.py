from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    links = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'links',
        )
