import pytest

from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password

from linkanywhere.apps.users.serializers import UserSerializer

from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='function')
def user_data():
    return model_to_dict(f.UserFactory.build())


def test_user_serializer_with_empty_data():
    serializer = UserSerializer(data={})
    assert not serializer.is_valid()


def test_user_serializer_with_valid_data(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()


def test_user_serializer_hashes_password(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()

    user = serializer.save()
    assert check_password(user_data.get('password'), user.password)
