import pytest
from nose.tools import eq_

from rest_framework import (
    generics, serializers, status
)

from linkanywhere.apps.base.permissions import IsAdminOrReadOnly
from tests.models import BasicModel
from .. import factories as f

pytestmark = pytest.mark.django_db


class BasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicModel
        fields = '__all__'


class InstanceView(generics.ListCreateAPIView):
    queryset = BasicModel.objects.all()
    serializer_class = BasicSerializer
    permission_classes = (IsAdminOrReadOnly, )


instance_view = InstanceView.as_view()


def test_anonymous_user_has_read_only_permissions(rf):
    request = rf.post('/', {'text': 'some text'})
    response = instance_view(request)

    eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)


def test_authenticated_user_has_read_only_permissions(rf):
    request = rf.post('/', {'text': 'some text'})
    request.user = f.UserFactory.create()
    response = instance_view(request)

    eq_(response.status_code, status.HTTP_403_FORBIDDEN)


def test_admin_user_has_create_permissions(rf, admin_user):
    request = rf.post('/', {'text': 'some text'})
    request.user = admin_user
    response = instance_view(request)

    eq_(response.status_code, status.HTTP_201_CREATED)
