from rest_framework import viewsets, mixins

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
