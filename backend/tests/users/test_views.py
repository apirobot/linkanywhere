import pytest
from nose.tools import eq_

from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.links.constants import DRAFT, PUBLISHED
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestUserViewSet:

    ############################
    # List
    ############################

    def test_list_users(self, client):
        user_1 = f.UserFactory.create()
        f.UserFactory.create()
        url = reverse('api:user-list')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data), 2)
        eq_(response.data[0]['id'], str(user_1.id))

    ############################
    # Retrieve
    ############################

    def test_retrieve_user(self, client):
        user_1 = f.UserFactory.create()
        f.LikeLinkFactory(user=user_1)
        f.LikeLinkFactory(user=user_1)
        url = reverse('api:user-detail', kwargs={'username': user_1.username})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['id'], str(user_1.id))
        eq_(len(response.data['liked_links']), 2)

    def test_retrieve_user_with_published_and_draft_links(self, client):
        user_1 = f.UserFactory.create()
        f.LinkFactory(owner=user_1, publication_status=PUBLISHED)
        f.LinkFactory(owner=user_1, publication_status=PUBLISHED)
        f.LinkFactory(owner=user_1, publication_status=DRAFT)
        url = reverse('api:user-detail', kwargs={'username': user_1.username})

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['published_links']), 2)
        eq_(len(response.data['draft_links']), 1)
