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
    links = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
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
            'links',
            'liked_links',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_liked_links(self, obj):
        return LinkSerializer(get_liked(Link, obj), many=True).data
