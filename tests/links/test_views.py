import pytest

from django.core.urlresolvers import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_links(client):
    link_1 = f.LinkFactory.create()
    f.LinkFactory.create()

    url = reverse('links:link-list')
    response = client.get(url)
    response_content = response.data

    assert response.status_code == 200
    assert len(response_content) == 2
    assert response_content[0]['id'] == str(link_1.id)
