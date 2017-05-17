import pytest

from django.forms.models import model_to_dict

from linkanywhere.apps.links.serializers import LinkSerializer

from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='function')
def link_data():
    return model_to_dict(f.LinkFactory.build())


def test_link_serializer_with_empty_data():
    serializer = LinkSerializer(data={})
    assert not serializer.is_valid()


def test_link_serializer_with_valid_data(link_data):
    serializer = LinkSerializer(data=link_data)
    assert serializer.is_valid()
