from django.test import TestCase
from rest_framework.test import APIClient, APITestCase


__author__ = 'erhmutlu'


class SimpleSample(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simplesample(self):
        first = 1
        second = 1
        self.assertEqual(first, second, "should be equal, but not!")