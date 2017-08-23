from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from linkanywhere.apps.base.pagination import StandardPagination
from linkanywhere.apps.likes.mixins import LikedMixin
from .filters import LinkFilter
from .models import Link
from .serializers import LinkSerializer, PublicationStatusSerializer


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
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @list_route(permission_classes=[permissions.IsAdminUser])
    def draft(self, request):
        self.queryset = Link.objects.draft()
        return self.list(request)

    @detail_route(methods=['POST'], permission_classes=[permissions.IsAdminUser])
    def change_publication_status(self, request, pk=None):
        self.queryset = Link.objects.all()
        link = self.get_object()
        serializer = PublicationStatusSerializer(data=request.data)

        if serializer.is_valid():
            link.publication_status = serializer.data['publication_status']
            link.save()
            return Response({
                'status': 'publication status has changed to {}'.format(
                    link.get_publication_status_display())
            })

        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
