from django.test import TestCase
from io import StringIO
from unittest import mock
from unittest.mock import MagicMock

from rack.models import (
    Comic,
    DosageUpdateReport,
    Strip,
    StripImage,
    StripManager
)

from rack.tasks import _parse_json_data
from rack.tests.factories import (
    ComicFactory, DosageUpdateReportFactory, StripFactory
)
from rack.tests.mocks import mock_django_storage


class ComicTestCase(TestCase):
    def setUp(self):
        self.comic = comic = ComicFactory.create()

    def test_has_problem(self):
        report = DosageUpdateReportFactory.create(
            comic=self.comic,
            status=1
        )
        self.assertFalse(self.comic.has_problem)

        report.status = 3
        report.save()
        self.assertTrue(self.comic.has_problem)

    def test_name_property(self):
        names = [
            ('BetweenFailures', None, 'Between Failures'),
            ('Arcamax/MotherGooseAndGrimm', None, 'Mother Goose And Grimm (Arcamax)'),
            ('SnafuComics/PowerPuffGirls', 'The Powerpuff Girls (Snafu Comics)', None),
        ]
        for data in names:
            comic = ComicFactory.create(dosage_name=data[0], override_name=data[1])
            if data[2]:
                self.assertEqual(comic.name, data[2])
            else:
                self.assertEqual(comic.name, data[1])



class StripTestCase(TestCase):
    def setUp(self):
        json_path = 'rack/tests/json/dilbert_latest.json'
        strips = _parse_json_data(json_path)
        self.latest_dilbert = strips[0]

        self.comic = ComicFactory.create(dosage_name='Dilbert')
        # xkcd has a quirk module
        self.xkcd = ComicFactory.create(dosage_name='xkcd')

    @mock_django_storage(save_path="strips/Dilbert/2014-05-08.gif")
    def test_get_or_create_with_images(self):
        Strip.objects.get_or_create_with_images(self.comic, self.latest_dilbert)
        Strip.objects.get_or_create_with_images(self.comic, self.latest_dilbert)
        self.assertEqual(Strip.objects.count(), 1)

