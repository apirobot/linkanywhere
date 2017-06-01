import mock
import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

from linkanywhere.apps.links.constants import DRAFT, PUBLISHED
from linkanywhere.apps.links.models import Link
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_link__str__():
    user = f.LinkFactory.create()
    eq_(user.__str__(), '{0}: {1}'.format(user.title, user.url))


def test_link_relation_with_category():
    category_1 = f.CategoryFactory.create()
    link_1 = f.LinkFactory.create(category=category_1)
    link_2 = f.LinkFactory.create(category=category_1)

    eq_(link_1.category, category_1)
    eq_(link_2.category, category_1)


def test_link_relation_with_tags():
    tag_1 = f.TagFactory.create()
    tag_2 = f.TagFactory.create()
    link_1 = f.LinkFactory.create(tags=[tag_1, tag_2])
    link_2 = f.LinkFactory.create(tags=[tag_1])

    assert_queryset_equal(
        link_1.tags.all(),
        [repr(tag_1), repr(tag_2)],
        ordered=False
    )
    assert_queryset_equal(
        link_2.tags.all(),
        [repr(tag_1)],
        ordered=False
    )


def test_link_total_likes():
    link_1 = f.LinkFactory.create()
    with mock.patch('linkanywhere.apps.links.models.Link.likes') as likes_mock:
        link_1.total_likes
        likes_mock.count.assert_called()


def test_link_published_and_draft_statuses():
    f.LinkFactory.create(publication_status=DRAFT)
    f.LinkFactory.create(publication_status=DRAFT)
    f.LinkFactory.create(publication_status=PUBLISHED)

    eq_(Link.objects.published().count(), 1)
    eq_(Link.objects.draft().count(), 2)
