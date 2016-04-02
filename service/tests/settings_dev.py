from __future__ import absolute_import
from settings.common import *
import os


__author__ = 'erhmutlu'


BASE_DIR = os.path.dirname(__file__)
ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.db'),
    }
}

DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'tests',
)

TESTING = True

ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_INDEX = 'personal-nlp-test'
ELASTICSEARCH_ENTITY_DOCTYPE = 'entity'
ELASTICSEARCH_INTENT_DOCTYPE = 'intent'

