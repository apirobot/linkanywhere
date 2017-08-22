from rest_framework import serializers

from linkanywhere.apps.likes.services import get_liked
from linkanywhere.apps.links.models import Link
from linkanywhere.apps.links.serializers import LinkSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    draft_links = serializers.SerializerMethodField()
    published_links = serializers.SerializerMethodField()
    liked_links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'draft_links',
            'published_links',
            'liked_links',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_liked_links(self, obj):
        return LinkSerializer(
            get_liked(Link, obj),
            many=True,
            context=self.context
        ).data

    def get_draft_links(self, obj):
        return LinkSerializer(
            obj.links.draft(),
            many=True,
            context=self.context
        ).data

    def get_published_links(self, obj):
        return LinkSerializer(
            obj.links.published(),
            many=True,
            context=self.context
        ).data
