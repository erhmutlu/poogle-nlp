from django.test import TestCase
from apps.defaultapp.es_docs import Entity

__author__ = 'erhmutlu'


class EntityImportTest(TestCase):
    def test_create_instance(self):
        e = Entity()
        self.assertIsInstance(e, Entity)

