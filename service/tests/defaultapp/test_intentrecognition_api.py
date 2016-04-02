import json
import uuid
from rest_framework.test import APITestCase, APIClient
from apps.defaultapp.es_docs import Entity, Intent
from apps.search.elasticsearch.es import Es
import time
import string
import random

__author__ = 'erhmutlu'


class IntentRecognitionAPITest(APITestCase):

    api_client = APIClient()
    es = Es()

    def __generate_entity(self):
        synonym1 = self.__generate_random_str()
        synonym2 = self.__generate_random_str()

        key = '@' + self.__generate_random_str()

        self.entity = Entity(entity_key=key, entity_synonyms=[synonym1, synonym2], value=synonym1)
        self.entity.save(using=self.es.client)

    def __generate_intent(self, word_count=None):
        if self.entity is not None:

            param = self.entity.entity_key
            action = 'get_' + self.__generate_random_str()

            if word_count is not None:
                str_list = [self.__generate_random_str() for irrelevant in range(0, word_count-1)]
                sentence = param + ' ' + ' '.join(str_list)
            else:
                sentence = param + self.__generate_random_str()

            self.intent = Intent(params=[param], sentence=sentence,
                                 original_sentence=sentence, action=action)
            self.intent.save(using=self.es.client)
        else:
            pass

    def __generate_random_str(self, size=5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(size))

    def __call_post(self, url, data, clt=api_client):
        return clt.post(url, data=json.dumps(data), content_type="application/json")

    def __call_get(self, url, clt=api_client):
        return clt.get(url)

    def __call_delete(self, url, clt=api_client):
        return clt.delete(url)

    def test_successful_exact_sentence_input_wordcount_five(self):
        self.__generate_entity()
        time.sleep(5)
        self.__generate_intent(word_count=5)
        self.assertIsNotNone(self.entity)
        self.assertIsNotNone(self.intent)
        time.sleep(5)

        sentence = self.intent.sentence
        sentence = sentence.replace(self.entity.entity_key, self.entity.entity_synonyms[0])

        url = '/api/intent-recognition/recognize/?sentence=' + sentence
        response = self.__call_get(url=url)

        self.es.delete_doc_item(doc=Entity, id=self.entity._id)
        self.es.delete_doc_item(doc=Intent, id=self.intent._id)

        content = json.loads(response.content)
        print dict(content)
        self.assertEqual(content['intent']['action'], self.intent.action)
