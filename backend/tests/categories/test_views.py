import pytest
from nose.tools import eq_

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.categories.models import Category
from .. import factories as f

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestCategoryViewSet:

    ############################
    # Create
    ############################

    def test_create_category(self, client, admin_client):
        data = {'name': 'Test category'}
        url = reverse('api:category-list')

        response = client.post(url)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = admin_client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['name'], 'Test category')

    ############################
    # List
    ############################

    def test_list_categories(self, client):
        category_1 = f.CategoryFactory()
        f.CategoryFactory()
        url = reverse('api:category-list')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data), 2)
        eq_(response.data[0]['id'], str(category_1.id))

    ############################
    # Delete
    ############################

    def test_delete_category(self, client, admin_client):
        category_1 = f.CategoryFactory()
        url = reverse('api:category-detail', kwargs={'pk': category_1.id})

        response = client.delete(url)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = admin_client.delete(url)
        eq_(response.status_code, status.HTTP_204_NO_CONTENT)
        eq_(Category.objects.count(), 0)
