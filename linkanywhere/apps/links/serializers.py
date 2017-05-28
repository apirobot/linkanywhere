from rest_framework import serializers

from .relations import TagRelatedField
from .models import Category, Link, Tag


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


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    tags = TagRelatedField(many=True, required=False)

    class Meta:
        model = Link
        fields = (
            'id',
            'owner',
            'title',
            'url',
            'description',
            'category',
            'tags',
            'total_likes',
            'created',
            'modified',
        )


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
