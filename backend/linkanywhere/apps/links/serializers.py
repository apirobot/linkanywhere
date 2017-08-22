from rest_framework import serializers

from linkanywhere.apps.categories.models import Category
from linkanywhere.apps.tags.relations import TagRelatedField
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    tags = TagRelatedField(many=True, required=False)

    url_domain = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = (
            'id',
            'owner',
            'title',
            'url',
            'url_domain',
            'description',
            'category',
            'tags',
            'total_likes',
            'created',
            'modified',
        )

    def get_url_domain(self, obj):
        return obj.get_url_domain()


class PublicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Link
        fields = ('publication_status', )
