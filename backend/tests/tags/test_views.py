import pytest
from nose.tools import eq_

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.tags.models import Tag
from .. import factories as f

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestTagViewSet:

    ############################
    # Create
    ############################

    def test_create_tag(self, client):
        data = {'name': 'Test tag'}
        url = reverse('api:tag-list')

        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['name'], 'Test tag')

    ############################
    # List
    ############################

    def test_list_tags(self, client):
        tag_1 = f.TagFactory.create()
        f.TagFactory.create()
        url = reverse('api:tag-list')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data), 2)
        eq_(response.data[0]['id'], str(tag_1.id))

    ############################
    # Delete
    ############################

    def test_delete_tag(self, client):
        tag_1 = f.TagFactory.create()
        url = reverse('api:tag-detail', kwargs={'pk': tag_1.id})

        response = client.delete(url)
        eq_(response.status_code, status.HTTP_204_NO_CONTENT)
        eq_(Tag.objects.count(), 0)
