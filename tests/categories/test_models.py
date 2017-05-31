import pytest
from nose.tools import eq_
from django_nose.tools import assert_queryset_equal

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_category__str__():
    category = f.CategoryFactory.create()
    eq_(category.__str__(), category.name)


def test_category_relation_with_links():
    category_1 = f.CategoryFactory.create()
    link_1 = f.LinkFactory.create(category=category_1)
    link_2 = f.LinkFactory.create(category=category_1)

    assert_queryset_equal(
        category_1.links.all(),
        [repr(link_1), repr(link_2)],
        ordered=False
    )
