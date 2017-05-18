import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_category__str__():
    category = f.CategoryFactory.create()
    assert category.__str__() == category.name


def test_category_slug():
    category = f.CategoryFactory.create(name='Category number 1')
    assert category.slug == 'category-number-1'


def test_link__str__():
    user = f.LinkFactory.create()
    assert user.__str__() == '{0}: {1}'.format(user.title, user.url)


def test_link_and_category_relation():
    category_1 = f.CategoryFactory.create()
    link_1 = f.LinkFactory.create(category=category_1)
    link_2 = f.LinkFactory.create(category=category_1)

    assert link_1.category == category_1
    assert link_2.category == category_1
    assert category_1.links.count() == 2
