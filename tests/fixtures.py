import pytest


@pytest.fixture()
def rf():
    """RequestFactory instance"""

    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@pytest.fixture()
def client():
    """A Django test client instance."""

    from rest_framework.test import APIClient

    return APIClient()
