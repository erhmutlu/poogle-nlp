import json
import random
import string
import uuid
from elasticsearch import Elasticsearch
from rest_framework.test import APITestCase, APIClient
from service.apps.defaultapp.es_docs import Entity, Intent
from django.conf import settings
from apps.search.elasticsearch.es import Es
import time

__author__ = 'erhmutlu'


class IntentAPITest(APITestCase):

    api_client = APIClient()
    es = Es()

    def __generate_intent_obj(self):
        param = '@' + self.__generate_random_str()
        action = 'get_' + self.__generate_random_str()
        sentence = param + self.__generate_random_str()

        data = {'params': [param], 'action': action, 'sentence': sentence}

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
        intent_api_url = '/api/intent/'

        data = self.__generate_intent_obj()
        resp = self.__call_post(intent_api_url, data)

        content = json.loads(resp.content)

        for key in data:
            self.assertEqual(data[key], content[key])

        id = content['id']
        self.assertIsNotNone(content['id'])

        self.es.delete_doc_item(doc=Intent, id=id)

    def test_successful_best_match(self):

        data = self.__generate_intent_obj()
        i = Intent(sentence=data['sentence'], original_sentence=data['sentence'],
                   action=data['action'], params=data['params'])

        i.save(using=self.es.client)
        id = i._id
        time.sleep(3)

        sentence = data['sentence']

        intent_match_api_url = '/api/intent/match/?sentence=%s' % sentence
        resp = self.__call_get(intent_match_api_url)

        content = json.loads(resp.content)

        matched = sentence in [matches['sentence'] for matches in content['best_matches']]
        self.assertTrue(matched)
        self.es.delete_doc_item(doc=Intent, id=id)

    def successful_delete(self):
        intent_api_url = '/api/entity/'
        data = self.__generate_intent_obj()
        i = Intent(sentence=data['sentence'], original_sentence=data['sentence'],
                   action=data['action'], params=data['params'])

        i.save(using=self.es.client)
        id = i._id
        time.sleep(3)
        self.__call_delete(intent_api_url)
        self.assertRaises(Exception, Intent.get(using=self.es.client, id=id), "entity should have deleted")
