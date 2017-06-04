import pytest
from nose.tools import eq_

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.tags.models import Tag
from .. import factories as f

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_create_tag(client):
    url = reverse('tag-list')
    data = {'name': 'Test tag'}

    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, status.HTTP_201_CREATED)
    eq_(response_content['name'], 'Test tag')


def test_list_tags(client):
    tag_1 = f.TagFactory.create()
    f.TagFactory.create()

    url = reverse('tag-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(tag_1.id))


def test_destroy_tag(client):
    tag_1 = f.TagFactory.create()

    url = reverse('tag-detail', kwargs={'pk': tag_1.id})
    response = client.delete(url)

    eq_(response.status_code, status.HTTP_204_NO_CONTENT)
    eq_(Tag.objects.count(), 0)
