import pytest

from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture()
def rf():
    """RequestFactory instance"""

    return APIRequestFactory()


@pytest.fixture()
def client():
    """A Django test client instance."""

    return APIClient()


@pytest.fixture()
def admin_client(db, admin_user):
    """A Django test client logged in as an admin user."""

    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client
