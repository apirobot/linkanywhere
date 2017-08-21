import pytest
from nose.tools import eq_

from .. import factories as f

pytestmark = pytest.mark.django_db


class TestUserModel:

    def test__str__(self):
        user = f.UserFactory.create()
        eq_(user.__str__(), user.username)
