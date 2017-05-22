import pytest
from nose.tools import eq_

from django.core.urlresolvers import reverse

from rest_framework import status

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_users(client):
    user_1 = f.UserFactory.create()
    f.UserFactory.create()

    url = reverse('users:user-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(user_1.id))


def test_retrieve_user(client):
    user_1 = f.UserFactory.create()

    url = reverse('users:user-detail', kwargs={'username': user_1.username})
    response = client.get(url)
    response_content = response.data

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(response_content['id'], str(user_1.id))
