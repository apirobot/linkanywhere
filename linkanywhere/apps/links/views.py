from rest_framework import viewsets, mixins

from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
