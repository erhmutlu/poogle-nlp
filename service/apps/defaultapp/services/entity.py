# -*- coding: utf-8 -*-

from elasticsearch_dsl import Q
import re
from apps.defaultapp.es_docs import Entity
from apps.defaultapp.tools.number import NumberFinder
from apps.defaultapp.tools.str import erase_extra_whitespaces, erase_matched_words
from apps.search.elasticsearch.es import Es
from apps.search.elasticsearch.query_executor import QueryExecutor

__author__ = 'erhmutlu'


class EntityService:

    @staticmethod
    def find_entities(user_input):
        numbers, user_input = EntityService.__find_number_entities_and_clear_input(user_input)

        es = Es()
        q = Q('match', entity_synonyms=user_input)
        es_entities = QueryExecutor.execute_search(es.client, Entity, q)
        return numbers + es_entities

    @staticmethod
    def __find_number_entities_and_clear_input(user_input):
        numbers = EntityService.__detect_numbers(user_input)

        entities = EntityService.__make_all_numbers_entity_obj(numbers)
        user_input = EntityService.__clear_input(numbers, user_input)

        return entities, user_input

    @staticmethod
    def __detect_numbers(sentence):
        numberFinder = NumberFinder()
        return numberFinder.find(sentence)

    @staticmethod
    def __make_all_numbers_entity_obj(numbers):
        entities = [Entity(entity_synonyms=[number.get('digit'), number.get('word')], entity_key='@Number',
                           presentation_value=number.get('digit')) for number in numbers]
        return entities

    @staticmethod
    def __clear_input(numbers, user_input):
        for number in numbers:
            user_input = erase_matched_words(user_input, number.get('word'))

        return user_input
