import pytest
from nose.tools import eq_

from linkanywhere.apps.likes.models import Like
from linkanywhere.apps.likes.services import add_like, remove_like
from tests.models import LikeModel
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_add_and_remove_like():
    user = f.UserFactory.create()
    obj = LikeModel(text='some text')
    eq_(Like.objects.count(), 0)

    add_like(obj, user)
    eq_(Like.objects.count(), 1)

    add_like(obj, user)
    eq_(Like.objects.count(), 1)

    remove_like(obj, user)
    eq_(Like.objects.count(), 0)
