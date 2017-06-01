from rest_framework import viewsets, mixins, permissions

from linkanywhere.apps.likes.mixins import LikedMixin
from .filters import LinkFilter
from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(LikedMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.published()
    serializer_class = LinkSerializer
    filter_class = LinkFilter
    search_fields = ('title', 'description')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
