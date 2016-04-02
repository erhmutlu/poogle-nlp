from django.conf import settings
from apps.defaultapp.shapers import *

__author__ = 'erhmutlu'


class IntentResponseShaper:

    def shape(self, user_input, intent):
        action_name = intent.get('action')

        clz = self.__find_clz(action_name)
        func = getattr(clz, action_name, None)
        resp = func(user_input, intent) if func is not None else intent

        append_resp_with_action_name(resp, action_name)

        return self.__make_final_response(resp, clz)

    def __find_clz(self, action_name):
        mapping = getattr(settings, 'SHAPER_CLASS_MAPPINGS', None)
        if map is not None:
            f = filter(lambda x: x['action'] == action_name, mapping)
            c = f[0].get('clz') if len(f) == 1 else 'IntentResponseShaper'
            return globals()[c]()

    def __find_clz_name(self, clz):
        return clz.__class__.__name__

    def __make_final_response(self, intent, clz):
        obj = {
            'intent': intent,
            'class': self.__find_clz_name(clz)
        }
        return obj



