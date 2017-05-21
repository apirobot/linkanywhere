import pytest
from nose.tools import eq_

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_user__str__():
    user = f.UserFactory.create()
    eq_(user.__str__(), user.username)
