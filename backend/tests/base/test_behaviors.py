import datetime

from freezegun import freeze_time
from nose.tools import assert_almost_equal, eq_, ok_
import pytest
import pytz

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

    def test_changing_publication_date(self, published_instance):
        eq_(published_instance.publication_date, None)

        first, second, third = (
            datetime.datetime(2012, 1, 14, 3, 21, 34, tzinfo=pytz.utc),
            datetime.datetime(2013, 1, 14, 3, 21, 34, tzinfo=pytz.utc),
            datetime.datetime(2014, 1, 14, 3, 21, 34, tzinfo=pytz.utc))

        for time, status in zip((first, second, third),
                                (PUBLISHED, DRAFT, PUBLISHED)):
            with freeze_time(time):
                published_instance.publication_status = status
                published_instance.save()
                eq_(published_instance.publication_date, first)
