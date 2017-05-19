from rest_framework import viewsets, mixins

from .models import Category, Link
from .serializers import CategorySerializer, LinkSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class LinkViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
