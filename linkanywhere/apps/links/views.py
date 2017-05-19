from rest_framework import viewsets, mixins

from .models import Category, Link, Tag
from .serializers import CategorySerializer, LinkSerializer, TagSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LinkViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class TagViewSet(mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
