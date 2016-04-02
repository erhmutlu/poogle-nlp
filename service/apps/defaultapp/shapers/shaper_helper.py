import operator
from django.conf import settings
from apps.defaultapp.tools.str import find_index_of_word

__author__ = 'erhmutlu'


def sort_params(sentence, params):
        indexed = append_params_with_index_(sentence, params)
        indexed.sort(key=operator.itemgetter('index'))
        return [i['p'] for i in indexed]


def append_params_with_index_(sentence, params):
    tmp = []
    for p in params:
        v = p['presentation_value']
        index = find_index_of_word(sentence, v)
        tmp.append({'p': p, 'index': index})

    return tmp


def filter_by_entity_key(params, settings_key):

    key = getattr(settings, settings_key, None)
    if key is not None:
        return filter(lambda x: x.get('key') and x.get('key').lower() == str(key).lower(), params)
    raise EnvironmentError('settings_key not found')


def append_resp_with_action_name(resp, action):
    if resp.get('action') is None:
        resp['action'] = action
    return resp


def set_params(params, resp=None):
    o = resp if resp is not None else {}
    o['params'] = params
    return o