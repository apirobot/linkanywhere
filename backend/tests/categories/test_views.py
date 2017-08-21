import pytest
from nose.tools import eq_

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.categories.models import Category
from .. import factories as f

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_create_category(client, admin_client):
    url = reverse('api:category-list')
    data = {'name': 'Test category'}

    response = client.post(url)
    eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    response = admin_client.post(url, data)
    response_content = response.data
    eq_(response.status_code, status.HTTP_201_CREATED)
    eq_(response_content['name'], 'Test category')


def test_list_categories(client):
    category_1 = f.CategoryFactory.create()
    f.CategoryFactory.create()

    url = reverse('api:category-list')
    response = client.get(url)
    response_content = response.data

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(category_1.id))


def test_destroy_category(client, admin_client):
    category_1 = f.CategoryFactory.create()

    url = reverse('api:category-detail', kwargs={'pk': category_1.id})

    response = client.delete(url)
    eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

    response = admin_client.delete(url)
    eq_(response.status_code, status.HTTP_204_NO_CONTENT)
    eq_(Category.objects.count(), 0)
