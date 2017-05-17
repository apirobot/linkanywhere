import pytest

from django.core.urlresolvers import reverse

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_users(client):
    user_1 = f.UserFactory.create()
    f.UserFactory.create()

    url = reverse('users:user-list')
    response = client.get(url)
    response_content = response.data

    assert response.status_code == 200
    assert len(response_content) == 2
    assert response_content[0]['id'] == str(user_1.id)


def test_retrieve_user(client):
    user_1 = f.UserFactory.create()

    url = reverse('users:user-detail', kwargs={'username': user_1.username})
    response = client.get(url)
    response_content = response.data

    assert response.status_code == 200
    assert response_content['id'] == str(user_1.id)
