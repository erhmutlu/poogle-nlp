# -*- coding: utf-8 -*-

from django.test import TestCase
from apps.defaultapp.services.intentresponse_shaper import IntentResponseShaper

__author__ = 'erhmutlu'


class IntentResponseShifterTest(TestCase):

    def setUp(self):
        self.shape_shifter = IntentResponseShaper()

    def test_convert_currency_units(self):
        sentence = '@Number @Currency kaç @Currency yapar'
        params = [
                    {'key': '@Number', 'value': 120, 'presentation_value': 120},
                    {'key': '@Currency', 'value': 'TRY', 'presentation_value': 'Türk Lirası'},
                    {'key': '@Currency', 'value': 'USD', 'presentation_value': 'Amerikan Doları'},
                  ]
        action = 'convert_currency_units'
        intent = {'sentence': sentence, 'original_sentence': sentence, 'params': params, 'action': action}
        sentence = "120 türk lirası kaç amerikan doları yapar"
        self.shape_shifter.shape(sentence, intent)

    # def test_get_weather(self):
    #     sentence = '@City hava nasıl olacak'
    #     params = [
    #         {'key': '@City', 'value': 'İstanbul', 'presentation_value': 'İstanbul'}
    #     ]
    #     action = 'get_weather'
    #     intent = {'sentence': sentence, 'original_sentence': sentence, 'params': params, 'action': action}
    #     sentence = 'İstanbulda hava nasıl olacak'
    #     self.shape_shifter.shape(sentence, intent)
