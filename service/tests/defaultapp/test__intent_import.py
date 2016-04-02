from django.test import TestCase
from apps.defaultapp.es_docs import Intent

__author__ = 'erhmutlu'


class IntentImportTest(TestCase):
    def test_create_instance(self):
        i = Intent()
        self.assertIsInstance(i, Intent)

