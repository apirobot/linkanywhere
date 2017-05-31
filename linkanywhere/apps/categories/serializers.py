from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    links = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'links',
        )
