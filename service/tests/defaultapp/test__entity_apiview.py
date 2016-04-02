import json
import random
import string
import uuid
from elasticsearch import Elasticsearch
from rest_framework.test import APITestCase, APIClient
from service.apps.defaultapp.es_docs import Entity
from django.conf import settings
from service.apps.search.elasticsearch.es import Es
import time

__author__ = 'erhmutlu'


class EntityAPITest(APITestCase):

    api_client = APIClient()
    es = Es()

    def __generate_entity_obj(self):
        synonym1 = self.__generate_random_str()
        synonym2 = self.__generate_random_str()

        key = '@' + self.__generate_random_str()
        data = {'entity_synonyms': [synonym1, synonym2], 'entity_key': key, 'value': synonym1}

        return data

    def __generate_random_str(self, size=5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))

    def __call_post(self, url, data, clt=api_client):
        return clt.post(url, data=json.dumps(data), content_type="application/json")

    def __call_get(self, url, clt=api_client):
        return clt.get(url)

    def __call_delete(self, url, clt=api_client):
        return clt.delete(url)

    def test_successful_create_request(self):
        entity_api_url = '/api/entity/'

        data = self.__generate_entity_obj()
        resp = self.__call_post(entity_api_url, data)

        content = json.loads(resp.content)
        for key in data:
            self.assertEqual(data[key], content[key])

        self.assertIsNotNone(content['id'])
        id = content['id']

        self.es.delete_doc_item(doc=Entity, id=id)

    def test_successful_match_as_word(self):
        entity_match_api_url = '/api/entity/match/'

        data = self.__generate_entity_obj()
        e = Entity(entity_synonyms=data['entity_synonyms'], entity_key=data['entity_key'])
        e.save(using=self.es.client)
        id = e._id
        time.sleep(3)

        searched = data['entity_synonyms'][0]

        entity_match_api_url += '?synonym=%s' % searched
        resp = self.__call_get(entity_match_api_url)
        content = json.loads(resp.content)

        matched = False
        for obj in content:
            matched = searched in obj['entity_synonyms']

        self.es.delete_doc_item(doc=Entity, id=id)
        self.assertTrue(matched)

    def test_successful_match_in_sentence(self):
        entity_match_api_url = '/api/entity/match/'

        data = self.__generate_entity_obj()
        e = Entity(entity_synonyms=data['entity_synonyms'], entity_key=data['entity_key'])
        e.save(using=self.es.client)
        id = e._id
        time.sleep(3)

        searched = data['entity_synonyms'][0]

        entity_match_api_url += '?synonym=%s test ediyorum' % searched
        resp = self.__call_get(entity_match_api_url)
        content = json.loads(resp.content)

        matched = False
        for obj in content:
            matched = searched in obj['entity_synonyms']

        self.assertTrue(matched)
        self.es.delete_doc_item(doc=Entity, id=id)

    def test_successful_delete(self):
        entity_api_url = '/api/entity/'

        data = self.__generate_entity_obj()
        e = Entity(entity_synonyms=data['entity_synonyms'], entity_key=data['entity_key'])
        e.save(using=self.es.client)
        id = e._id
        time.sleep(3)

        self.__call_delete(entity_api_url)

        self.assertRaises(Exception, Entity.get(using=self.es.client, id=id), "entity should have deleted")
