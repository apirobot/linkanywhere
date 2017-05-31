from rest_framework import viewsets, mixins, permissions

from linkanywhere.apps.likes.mixins import LikedMixin
from .filters import LinkFilter
from .models import Link, Tag
from .serializers import LinkSerializer, TagSerializer


class LinkViewSet(LikedMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_class = LinkFilter
    search_fields = ('title', 'description')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
