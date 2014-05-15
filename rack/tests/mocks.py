from django.core.files.base import File
from django.core.files.storage import Storage
from io import StringIO
from unittest import mock
from unittest.mock import MagicMock

from rack.models import StripManager


DUMMY_CONTENT = "dummy content"


def _create_storage_mock():
    storage_mock = MagicMock(spec=Storage, name='StorageMock')

    storage_mock.path = MagicMock(name='path')
    storage_mock.save = MagicMock(name='save')
    storage_mock.open = MagicMock(name="open")
    storage_mock.open.return_value = MagicMock(name='read')
    storage_mock.open.return_value.read = MagicMock(name='read')

    storage_mock.save.return_value = 'dummy.gif'
    storage_mock.path.return_value = 'dummy.gif'
    storage_mock.open.return_value.read.return_value = DUMMY_CONTENT
    return storage_mock
storage_mock = _create_storage_mock()


class mock_django_storage(object):  # pylint: disable=C0103
    def __init__(self, save_path=None):
        self.save_path = save_path

    def __call__(self, callable):
        decorator = self

        @mock.patch(
            'django.core.files.storage.default_storage._wrapped', storage_mock
        )
        @mock.patch.object(StripManager, '_get_dosage_image')
        def wrapped(*args, **kwargs):
            mocked_get_dosage_image = args[1]
            mocked_get_dosage_image.return_value = StringIO(DUMMY_CONTENT)
            mocked_get_dosage_image.open = MagicMock(name='open')

            if decorator.save_path is not None:
                _original_save_path = storage_mock.save.return_value
                storage_mock.save.return_value = decorator.save_path

            retval = callable(*args[0:1], **kwargs)

            if decorator.save_path is not None:
                storage_mock.save.return_value = _original_save_path

            return retval
        return wrapped
