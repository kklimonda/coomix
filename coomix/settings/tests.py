from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'coomix.db',
    }
}

CELERY_ALWAYS_EAGER = True

DOSAGE_BASEPATH = "dosage/"