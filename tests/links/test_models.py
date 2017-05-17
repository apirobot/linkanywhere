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
