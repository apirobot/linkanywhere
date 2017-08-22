import pytest
from nose.tools import eq_, ok_

from linkanywhere.apps.likes.models import Like
from linkanywhere.apps.likes import services
from linkanywhere.apps.links.models import Link
from tests.models import LikeModel
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_add_and_remove_like():
    user = f.UserFactory()
    obj = LikeModel(text='some text')
    eq_(Like.objects.count(), 0)

    services.add_like(obj, user)
    eq_(Like.objects.count(), 1)

    services.add_like(obj, user)
    eq_(Like.objects.count(), 1)

    services.remove_like(obj, user)
    eq_(Like.objects.count(), 0)


def test_get_liked(client):
    user_1 = f.UserFactory()
    f.LikeLinkFactory(user=user_1)
    f.LikeLinkFactory(user=user_1)

    eq_(len(services.get_liked(Link, user_1)), 2)


def test_is_fan():
    user_1 = f.UserFactory()
    link_1 = f.LinkFactory()
    link_2 = f.LinkFactory()

    f.LikeLinkFactory(content_object=link_1, user=user_1)

    ok_(services.is_fan(link_1, user_1))
    ok_(services.is_fan(link_2, user_1) is False)
