# -*- coding: utf-8 -*-
from itertools import groupby

from elasticsearch_dsl import Q
import math
import re
from apps.defaultapp.es_docs import Intent
from apps.defaultapp.tools.str import erase_extra_whitespaces, erase_matched_words
from apps.defaultapp.tools.tokenizer import perform_whitespace_tokenizer
from apps.search.elasticsearch.es import Es
from apps.search.elasticsearch.query_executor import QueryExecutor
import difflib
from collections import defaultdict, Counter

__author__ = 'erhmutlu'


class IntentRecognitionService:

    @staticmethod
    def eliminate_entities_in_sentence(user_input, entities):
        user_input = erase_extra_whitespaces(user_input)
        keys = []
        for match in entities:
            for synonym in match['entity_synonyms']:
                old = user_input
                erased = erase_matched_words(user_input, synonym)
                user_input = erase_extra_whitespaces(erased)

                if old.lower() != user_input.lower():
                    keys.append({'key': match['entity_key'], 'value': match['value'],
                                 'presentation_value': synonym})
                    break

        user_input = erase_extra_whitespaces(user_input)
        return user_input, keys

    @staticmethod
    def exact_recognize(user_input, keys=None):
        es = Es()
        must = [Q('match', params=key['key']) for key in keys] if keys is not None else []
        should = [Q('match', sentence={"query": user_input, "operator": "and"})]

        query = Q('bool', must=must, should=should, minimum_should_match=len(should))
        result = QueryExecutor.execute_search(es.client, Intent, query)
        exact_param_count_results = IntentRecognitionService.eliminates_intents_with_extra_params(result, keys)

        return IntentRecognitionService.find_closest_match(exact_param_count_results, user_input)

    @staticmethod
    def approximate_recognize(user_input, keys=None):
        es = Es()
        inputs = perform_whitespace_tokenizer(user_input)
        should = [Q('match', sentence=input.strip()) for input in inputs]
        must = [Q('match', params=key['key']) for key in keys] if keys is not None else []

        min_should_match = IntentRecognitionService.__calculate_min_should_match(should)
        query = Q('bool', must=must, should=should, minimum_should_match=min_should_match)
        result = QueryExecutor.execute_search(es.client, Intent, query)
        exact_param_count_results = IntentRecognitionService.eliminates_intents_with_extra_params(result, keys)

        return IntentRecognitionService.find_closest_match(exact_param_count_results, user_input)

    @staticmethod
    def find_closest_match(intents, input):
        length = len(intents)
        if length > 0:
            possibilities = [intent.get('sentence') for intent in intents]
            best_sentences = difflib.get_close_matches(cutoff=0.6, n=1, word=input, possibilities=possibilities)
            if len(best_sentences) > 0:
                return filter(lambda i: i['sentence'] == best_sentences[0], intents)[0]

        return intents[0] if length == 1 else None

    @staticmethod
    def __calculate_word_count(sentence, keys):
        return len(sentence.split(' ')) + len(keys)

    @staticmethod
    def eliminates_intents_with_extra_params(intents, keys):
        groups_of_keys = IntentRecognitionService.__get_defaultdict_of_keys(keys)
        groups_of_intents = IntentRecognitionService.__get_defaultdict_of_intents(intents)

        resp = []
        for gi in groups_of_intents:
            counter = gi.get('counter')
            intent = gi.get('intent')
            n_of_p = len(intent.get('params')) if intent.get('params') is not None else 0
            if n_of_p == len(keys):
                possible = True
                for c in counter:
                    if len(groups_of_keys[c]) != counter[c]:
                        possible = False
                        break
                if possible:
                    resp.append(intent)

        return resp

    @staticmethod
    def __calculate_min_should_match(should):
        return int(math.floor(len(should) * 3 / 4))

    @staticmethod
    def __get_defaultdict_of_keys(objs):
        groups = defaultdict(list)
        for o in objs:
            groups[o.get('key')].append(o)
        return groups

    @staticmethod
    def __get_defaultdict_of_intents(intents):

        group = []
        for intent in intents:
            params = intent.get('params')
            c = Counter(params)
            group.append({'intent': intent, 'counter': c})

        return group
