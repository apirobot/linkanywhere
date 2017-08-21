import pytest
from nose.tools import eq_

from linkanywhere.apps.likes.models import Like
from linkanywhere.apps.likes.services import add_like, remove_like, get_liked
from linkanywhere.apps.links.models import Link
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


def test_get_liked(client):
    user_1 = f.UserFactory.create()
    f.LikeLinkFactory(user=user_1)
    f.LikeLinkFactory(user=user_1)

    eq_(len(get_liked(Link, user_1)), 2)
