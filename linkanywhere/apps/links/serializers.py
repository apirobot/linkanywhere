from rest_framework import serializers

from .models import Category, Link


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
            'slug',
            'links',
        )


class LinkSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Link
        fields = (
            'id',
            'title',
            'url',
            'description',
            'category',
            'created',
            'modified',
        )
