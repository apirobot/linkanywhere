import pytest
from nose.tools import eq_

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_tag__str__():
    tag = f.TagFactory.create()
    eq_(tag.__str__(), tag.name)


def test_tag_relation_with_links():
    tag_1 = f.TagFactory.create()
    tag_2 = f.TagFactory.create()
    f.LinkFactory.create(tags=[tag_1, tag_2])
    f.LinkFactory.create(tags=[tag_1])

    eq_(tag_1.links.count(), 2)
    eq_(tag_2.links.count(), 1)
