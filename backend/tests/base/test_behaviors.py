import pytest
from nose.tools import eq_, ok_

from linkanywhere.apps.base.constants import DRAFT, PUBLISHED
from tests.models import PublishedModel

pytestmark = pytest.mark.django_db


@pytest.fixture
def published_instance():
    return PublishedModel.objects.create()


class TestPublishedBehavior:

    def test_draft_true_by_default(self, published_instance):
        ok_(published_instance.is_draft)

    def test_change_publication_status(self, published_instance):
        published_instance.publication_status = PUBLISHED
        published_instance.save()
        ok_(published_instance.is_published)

    def test_published_and_draft_statuses(self):
        PublishedModel.objects.create(publication_status=DRAFT)
        PublishedModel.objects.create(publication_status=DRAFT)
        PublishedModel.objects.create(publication_status=PUBLISHED)

        eq_(PublishedModel.objects.published().count(), 1)
        eq_(PublishedModel.objects.draft().count(), 2)
