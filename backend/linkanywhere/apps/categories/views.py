from rest_framework import viewsets, mixins

from linkanywhere.apps.base.permissions import IsAdminOrReadOnly
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
