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


def test_create_link(client):
    category_1 = f.CategoryFactory.create()
    tag_1 = f.TagFactory.create()
    tag_2 = f.TagFactory.create()
    user = f.UserFactory.create()

    client.login(user)
    url = reverse('api:link-list')
    data = {
        'title': 'Test link',
        'url': 'https://testlink.com',
        'description': 'Test link description',
        'category': category_1.name,
        'tags': [tag_1.name, tag_2.name]
    }

    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, status.HTTP_201_CREATED)
    eq_(response_content['category'], category_1.name)
    eq_(response_content['tags'], [tag_1.name, tag_2.name])


def test_created_link_is_associated_with_user(client):
    category_1 = f.CategoryFactory.create()
    user = f.UserFactory.create()

    client.login(user)
    url = reverse('api:link-list')
    data = {
        'title': 'Test link',
        'url': 'https://testlink.com',
        'description': 'Test link description',
        'category': category_1.name,
    }

    response = client.post(url, data)

    eq_(response.status_code, status.HTTP_201_CREATED)
    eq_(Link.objects.get(title='Test link').owner, user)


def test_create_link_with_not_created_tags(client):
    category_1 = f.CategoryFactory.create()
    user = f.UserFactory.create()

    client.login(user)
    url = reverse('api:link-list')
    data = {
        'title': 'Test link',
        'url': 'https://testlink.com',
        'description': 'Test link description',
        'category': category_1.name,
        'tags': ['some tag 1', 'some tag 2']
    }
    response = client.post(url, data)
    response_content = response.data

    eq_(response.status_code, status.HTTP_201_CREATED)
    eq_(response_content['tags'], ['some tag 1', 'some tag 2'])


def test_list_links(client):
    link_1 = f.LinkFactory.create()
    f.LinkFactory.create()

    url = reverse('api:link-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(link_1.id))


def test_list_only_published_links(client):
    f.LinkFactory.create(publication_status=DRAFT)
    f.LinkFactory.create(publication_status=PUBLISHED)
    f.LinkFactory.create(publication_status=PUBLISHED)

    url = reverse('api:link-list')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)


def test_list_only_draft_links(client, admin_client):
    user_1 = f.UserFactory.create()
    f.LinkFactory.create(publication_status=DRAFT)
    f.LinkFactory.create(publication_status=PUBLISHED)
    f.LinkFactory.create(publication_status=PUBLISHED)

    url = reverse('api:link-draft')

    client.login(user_1)
    response = client.get(url)
    eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    response = admin_client.get(url)
    response_content = response.data['results']
    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 1)


def test_list_links_filtered_by_category_and_tag(client):
    category_1 = f.CategoryFactory.create()
    tag_1 = f.TagFactory.create()
    f.LinkFactory.create(category=category_1)
    f.LinkFactory.create(tags=[tag_1])
    f.LinkFactory.create(category=category_1, tags=[tag_1])
    f.LinkFactory.create()

    # by category

    url = urljoin(reverse('api:link-list'),
                  '?category={}'.format(category_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)

    # by tag

    url = urljoin(reverse('api:link-list'),
                  '?tag={}'.format(tag_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 2)

    # by category & tag

    url = urljoin(reverse('api:link-list'),
                  '?category={}&tag={}'.format(category_1.name, tag_1.name))
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 1)


def test_destroy_link(client):
    category_1 = f.CategoryFactory.create()
    link_1 = f.LinkFactory.create(category=category_1)
    user = f.UserFactory.create()

    client.login(user)
    url = reverse('api:link-detail', kwargs={'pk': link_1.id})
    response = client.delete(url)

    eq_(response.status_code, status.HTTP_204_NO_CONTENT)
    eq_(Link.objects.count(), 0)
    eq_(category_1.links.count(), 0)


def test_search_links(client):
    f.LinkFactory.create(description='some description here')
    f.LinkFactory.create()

    url = urljoin(reverse('api:link-list'),
                  '?search=some+description')
    response = client.get(url)
    response_content = response.data['results']

    eq_(response.status_code, status.HTTP_200_OK)
    eq_(len(response_content), 1)


def test_like_link(client):
    user = f.UserFactory.create()
    link_1 = f.LinkFactory.create()

    url = reverse('api:link-like', kwargs={'pk': link_1.id})
    response = client.post(url)

    eq_(response.status_code, status.HTTP_401_UNAUTHORIZED)
    eq_(link_1.likes.count(), 0)

    client.login(user)
    for _ in range(2):  # like one link two times
        response = client.post(url)

        eq_(response.status_code, status.HTTP_200_OK)
        eq_(link_1.likes.count(), 1)


def test_unlike_link(client):
    user = f.UserFactory.create()
    link_1 = f.LinkFactory.create()
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


@pytest.mark.parametrize('publication_status', [
    PUBLISHED,
    DRAFT
])
def test_change_publication_status_of_a_link(publication_status, client, admin_client):
    user_1 = f.UserFactory.create()
    link_1 = f.LinkFactory.create(publication_status=publication_status)
    link_1_id = link_1.id

    url = reverse('api:link-change-publication-status',
                  kwargs={'pk': link_1_id})
    data = {
        'publication_status': publication_status
    }

    client.login(user_1)
    response = client.post(url, data)
    eq_(response.status_code, status.HTTP_403_FORBIDDEN)

    response = admin_client.post(url, data)
    response_content = response.data
    eq_(response.status_code, status.HTTP_200_OK)
    eq_(response_content['status'], 'publication status changed')
    eq_(Link.objects.get(id=link_1_id).publication_status, publication_status)
