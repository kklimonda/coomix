import json
import os
import shutil

from django.conf import settings
from django.test import TestCase
from io import StringIO
from unittest import mock
from unittest.mock import MagicMock

from rack.models import Comic, Strip, StripManager
from rack.tasks import _parse_json_data
from rack.tests.factories import ComicFactory
from rack.tests.mocks import storage_mock, DUMMY_CONTENT
from rack.tests.mocks import mock_django_storage


class JsonParserTestCase(TestCase):
    def setUp(self):
        self.comic = ComicFactory.create(dosage_name='Dilbert')

    @mock_django_storage()
    def test_latest_strip_json(self):
        """test if parsing a json generated for the latest strip works."""
        json_path = 'rack/tests/json/dilbert_latest.json'
        strips = _parse_json_data(json_path)
        self.assertEqual(len(strips), 1)

        data = strips[0]
        strip = Strip.objects.get_or_create_with_images(self.comic, data)

        self.assertEqual(strip.comic, self.comic)
        self.assertEqual(strip.images.count(), 1)
        self.assertEqual(strip.url, data['url'])

        for image in data['images']:
            db_image = strip.images.get(order=image['order'])
            self.assertEqual(db_image.image.path, 'dummy.gif')
            self.assertEqual(db_image.image.read(), DUMMY_CONTENT)

    @mock_django_storage()
    @mock.patch.object(shutil, 'copy')
    def test_basic_quirk_functions(self, mock_copy):
        json_path = 'rack/tests/json/xkcd_latest.json'
        xkcd = ComicFactory.create(dosage_name='xkcd')

        strips = _parse_json_data(json_path)

        strip = Strip.objects.get_or_create_with_images(xkcd, strips[0])
        copy_call_args = mock_copy.call_args[0]
        self.assertEqual(copy_call_args[0], 'dosage/xkcd/dummy.txt')
        self.assertEqual(
            copy_call_args[1], os.path.join(settings.MEDIA_ROOT, 'strips/xkcd/dummy.txt'))

        mock_open = MagicMock(name='open')
        mock_open.return_value = StringIO("dummy alt text")
        with mock.patch('builtins.open', mock_open):
            context = strip.quirk.get_extra_context(xkcd, strip)

        self.assertDictEqual(context, {
            'alt_text': 'dummy alt text'
        })
