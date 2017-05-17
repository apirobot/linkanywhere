import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_link__str__():
    user = f.LinkFactory.create()
    assert user.__str__() == '{0}: {1}'.format(user.title, user.url)
