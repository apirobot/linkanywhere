from rest_framework import viewsets, mixins

from linkanywhere.apps.base.permissions import IsAdminOrReadOnly
from .filters import LinkFilter
from .models import Category, Link, Tag
from .serializers import CategorySerializer, LinkSerializer, TagSerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


class LinkViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    filter_class = LinkFilter
    search_fields = ('title', 'description')


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
