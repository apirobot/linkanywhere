from unittest import mock

import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

from linkanywhere.apps.links.constants import DRAFT, PUBLISHED
from linkanywhere.apps.links.models import Link
from .. import factories as f

pytestmark = pytest.mark.django_db


class TestLinkModel:

    def test__str__(self):
        user = f.LinkFactory()
        eq_(user.__str__(), '{0}: {1}'.format(user.title, user.url))

    def test_relation_with_category(self):
        category_1 = f.CategoryFactory()
        link_1 = f.LinkFactory(category=category_1)
        link_2 = f.LinkFactory(category=category_1)

        eq_(link_1.category, category_1)
        eq_(link_2.category, category_1)

    def test_relation_with_tags(self):
        tag_1 = f.TagFactory()
        tag_2 = f.TagFactory()
        link_1 = f.LinkFactory(tags=[tag_1, tag_2])
        link_2 = f.LinkFactory(tags=[tag_1])

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

    def test_total_likes(self):
        link_1 = f.LinkFactory()
        with mock.patch('linkanywhere.apps.links.models.Link.likes') as likes_mock:
            link_1.total_likes
            likes_mock.count.assert_called()

    def test_get_url_domain(self):
        link_1 = f.LinkFactory(url='http://stackoverflow.com/questions/17/blah-blah')
        link_2 = f.LinkFactory(url='http://www.google.com/blah-blah')
        link_3 = f.LinkFactory(url='http://news.cnn.com/blah-blah')

        eq_(link_1.get_url_domain(), 'stackoverflow.com')
        eq_(link_2.get_url_domain(), 'google.com')
        eq_(link_3.get_url_domain(), 'cnn.com')

    def test_published_and_draft_statuses(self):
        f.LinkFactory(publication_status=DRAFT)
        f.LinkFactory(publication_status=DRAFT)
        f.LinkFactory(publication_status=PUBLISHED)

        eq_(Link.objects.published().count(), 1)
        eq_(Link.objects.draft().count(), 2)
