from urllib.parse import urljoin

import pytest
from nose.tools import eq_

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework import status

from linkanywhere.apps.links.constants import DRAFT, PUBLISHED
from linkanywhere.apps.links.models import Link
from .. import factories as f

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestLinkViewSet:

    ############################
    # Create
    ############################

    def test_create_link(self, client):
        category_1 = f.CategoryFactory()
        tag_1 = f.TagFactory()
        tag_2 = f.TagFactory()
        user = f.UserFactory()
        data = {
            'title': 'Test link',
            'url': 'https://testlink.com',
            'description': 'Test link description',
            'category': category_1.name,
            'tags': [tag_1.name, tag_2.name]
        }
        url = reverse('api:link-list')

        client.login(user)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['category'], category_1.name)
        eq_(response.data['tags'], [tag_1.name, tag_2.name])

    def test_created_link_has_an_owner(self, client):
        category_1 = f.CategoryFactory()
        user_1 = f.UserFactory()
        data = {
            'title': 'Test link',
            'url': 'https://testlink.com',
            'description': 'Test link description',
            'category': category_1.name,
        }
        url = reverse('api:link-list')

        client.login(user_1)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(Link.objects.get(title='Test link').owner, user_1)

    def test_create_link_with_not_created_tags(self, client):
        category_1 = f.CategoryFactory()
        user = f.UserFactory()
        data = {
            'title': 'Test link',
            'url': 'https://testlink.com',
            'description': 'Test link description',
            'category': category_1.name,
            'tags': ['some tag 1', 'some tag 2']
        }
        url = reverse('api:link-list')

        client.login(user)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_201_CREATED)
        eq_(response.data['tags'], ['some tag 1', 'some tag 2'])

    ############################
    # List
    ############################

    def test_list_links(self, client):
        link_1 = f.LinkFactory()
        f.LinkFactory()
        url = reverse('api:link-list')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 2)
        eq_(response.data['results'][0]['id'], str(link_1.id))

    def test_list_only_published_links(self, client):
        f.LinkFactory(publication_status=DRAFT)
        f.LinkFactory(publication_status=PUBLISHED)
        f.LinkFactory(publication_status=PUBLISHED)
        url = reverse('api:link-list')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 2)

    def test_list_only_draft_links(self, client, admin_client):
        user_1 = f.UserFactory()
        f.LinkFactory(publication_status=DRAFT)
        f.LinkFactory(publication_status=PUBLISHED)
        f.LinkFactory(publication_status=PUBLISHED)
        url = reverse('api:link-draft')

        client.login(user_1)
        response = client.get(url)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

        response = admin_client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 1)

    def test_list_links_filtered_by_category_and_tag(self, client):
        category_1 = f.CategoryFactory()
        tag_1 = f.TagFactory()
        f.LinkFactory(category=category_1)
        f.LinkFactory(tags=[tag_1])
        f.LinkFactory(category=category_1, tags=[tag_1])
        f.LinkFactory()

        # by category

        url = urljoin(reverse('api:link-list'),
                      '?category={}'.format(category_1.name))
        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 2)

        # by tag

        url = urljoin(reverse('api:link-list'),
                      '?tag={}'.format(tag_1.name))
        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 2)

        # by category & tag

        url = urljoin(reverse('api:link-list'),
                      '?category={}&tag={}'.format(category_1.name, tag_1.name))
        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 1)

    def test_search_links(self, client):
        f.LinkFactory(description='some description here')
        f.LinkFactory()
        url = urljoin(reverse('api:link-list'),
                      '?search=some+description')

        response = client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(len(response.data['results']), 1)

    ############################
    # Update
    ############################

    @pytest.mark.parametrize('publication_status, readable_publication_status', [
        (PUBLISHED, 'published'),
        (DRAFT, 'draft')
    ])
    def test_change_publication_status_of_a_link(self, publication_status, readable_publication_status,
                                                 client, admin_client):
        user_1 = f.UserFactory()
        link_1 = f.LinkFactory(publication_status=publication_status)
        link_1_id = link_1.id
        data = {
            'publication_status': publication_status
        }
        url = reverse('api:link-change-publication-status',
                      kwargs={'pk': link_1_id})

        client.login(user_1)
        response = client.post(url, data)
        eq_(response.status_code, status.HTTP_403_FORBIDDEN)

        response = admin_client.post(url, data)
        eq_(response.status_code, status.HTTP_200_OK)
        eq_(response.data['status'], 'publication status has changed to ' + readable_publication_status)
        eq_(Link.objects.get(id=link_1_id).publication_status, publication_status)

    def test_publication_status_is_required(self, admin_client):
        link_1 = f.LinkFactory()
        url = reverse('api:link-change-publication-status',
                      kwargs={'pk': link_1.id})

        response = admin_client.post(url)
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    ############################
    # Delete
    ############################

    def test_delete_link(self, client):
        category_1 = f.CategoryFactory()
        link_1 = f.LinkFactory(category=category_1)
        user = f.UserFactory()
        url = reverse('api:link-detail', kwargs={'pk': link_1.id})

        client.login(user)
        response = client.delete(url)
        eq_(response.status_code, status.HTTP_204_NO_CONTENT)
        eq_(Link.objects.count(), 0)
        eq_(category_1.links.count(), 0)

    ############################
    # Likes
    ############################

    def test_like_link(self, client):
        user = f.UserFactory()
        link_1 = f.LinkFactory()
        url = reverse('api:link-like', kwargs={'pk': link_1.id})

        response = client.post(url)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)
        eq_(link_1.likes.count(), 0)

        client.login(user)
        for _ in range(2):  # like one link two times
            response = client.post(url)

            eq_(response.status_code, status.HTTP_200_OK)
            eq_(link_1.likes.count(), 1)

    def test_unlike_link(self, client):
        user = f.UserFactory()
        link_1 = f.LinkFactory()
        f.LikeLinkFactory(content_object=link_1, user=user)
        url = reverse('api:link-unlike', kwargs={'pk': link_1.id})

        response = client.post(url)
        eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)
        eq_(link_1.likes.count(), 1)

        client.login(user)
        for _ in range(2):  # unlike one link two times
            response = client.post(url)

            eq_(response.status_code, status.HTTP_200_OK)
            eq_(link_1.likes.count(), 0)
