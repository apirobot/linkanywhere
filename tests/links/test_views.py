import pytest

from nose.tools import eq_

from django.core.urlresolvers import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_links(client):
    link_1 = f.LinkFactory.create()
    f.LinkFactory.create()

    url = reverse('links:link-list')
    response = client.get(url)
    response_content = response.data

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(link_1.id))


def test_list_categories(client):
    category_1 = f.CategoryFactory.create()
    f.CategoryFactory.create()

    url = reverse('links:category-list')
    response = client.get(url)
    response_content = response.data

    eq_(response.status_code, 200)
    eq_(len(response_content), 2)
    eq_(response_content[0]['id'], str(category_1.id))
