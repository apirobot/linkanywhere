import pytest

from nose.tools import ok_

from django.forms.models import model_to_dict

from linkanywhere.apps.links.serializers import (
    CategorySerializer, LinkSerializer
)
from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='function')
def category_data():
    return model_to_dict(f.CategoryFactory.build())


@pytest.fixture(scope='function')
def link_data():
    return model_to_dict(f.LinkFactory.build())


def test_category_serializer_with_empty_data():
    serializer = CategorySerializer(data={})
    ok_(serializer.is_valid() is False)


def test_category_serializer_with_valid_data(category_data):
    serializer = CategorySerializer(data=category_data)
    ok_(serializer.is_valid())


def test_link_serializer_with_empty_data():
    serializer = LinkSerializer(data={})
    ok_(serializer.is_valid() is False)


def test_link_serializer_with_valid_data(link_data):
    serializer = LinkSerializer(data=link_data)
    ok_(serializer.is_valid())
