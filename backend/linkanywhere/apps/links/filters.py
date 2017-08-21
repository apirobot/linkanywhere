from django_filters import rest_framework as filters

from .models import Link


class LinkFilter(filters.FilterSet):
    category = filters.CharFilter(name='category__name')
    tag = filters.CharFilter(name='tags__name')

    class Meta:
        model = Link
        fields = ('category', 'tag')
