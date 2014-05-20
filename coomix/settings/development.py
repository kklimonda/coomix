from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'development.db',
    }
}

DOSAGE_BASEPATH = "dosage/"

MEDIA_ROOT = '/home/kklimonda/code/personal/coomix/media/'
MEDIA_URL = "/media/"

SERVER_ENDPOINT = "http://localhost:8000/"
