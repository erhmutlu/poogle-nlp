# -*- coding: utf-8 -*-

import re
from apps.defaultapp.tools.str import can_convert_to_int, erase_matched_words, erase_extra_whitespaces, \
    erase_beginning_to_matched_word, erase_matched_word_to_end, is_blank_or_none, erase_punctuation_signs
from django.conf import settings
import operator
from Queue import Queue
from apps.defaultapp.tools.tokenizer import perform_whitespace_tokenizer

__author__ = 'erhmutlu'


class NumberFinder:

    finders = ['MillionsFinder', 'ThousandsFinder', 'HundredsFinder', 'TensFinder', 'OnesFinder']

    def find(self, sentence):
        original = sentence
        without_puncs = erase_punctuation_signs(sentence)
        founds = self.__internal_find(without_puncs)
        if len(founds) > 1:
            founds = self.__sort_founds(original, founds)
        return founds

    def __internal_find(self, sentence):
        founds = []
        queue = Queue()
        queue.put(sentence)
        while not queue.empty():
            sentence = queue.get_nowait()
            found = self.__operate_finders(sentence)
            if found is not None:
                founds.append(found)
                word = found['word']

                before = erase_matched_word_to_end(sentence, word)
                if not is_blank_or_none(before):
                    queue.put(before)

                after = erase_beginning_to_matched_word(sentence, word)
                if not is_blank_or_none(after):
                    queue.put(after)

        return founds

    def __operate_finders(self, sentence):
        found = None
        for finder in self.finders:
            clz = self.__obtain_finder_clz(finder)
            number_dict = clz.find(sentence)
            if number_dict is not None:
                found = number_dict
                break

        return found

    def __sort_founds(self, original_sentence, founds):
        indexed = self.__append_founds_with_index(original_sentence, founds)
        indexed.sort(key=operator.itemgetter('index'))
        return [i['f'] for i in indexed]

    def __append_founds_with_index(self,  original_sentence, founds):
        tmp = []
        for f in founds:
            word = f['word']
            index = original_sentence.find(word)
            tmp.append({'f': f, 'index': index})

        return tmp

    def __obtain_finder_clz(self, clz_name):
        clz = globals()[clz_name]()
        return clz


class MillionsFinder:

    @staticmethod
    def find(sentence):
        original = sentence
        millions_in_digit, millions_in_word = NumberFinderHelper.get_millions(sentence)
        if millions_in_digit != 0:
            str = millions_in_word
            number = millions_in_digit
            sentence = erase_matched_words(sentence, millions_in_word)
            thousands_in_digit, thousands_in_word = NumberFinderHelper.get_thousands(sentence)
            if thousands_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, thousands_in_word):
                str = str + ' ' + thousands_in_word
                number += thousands_in_digit
                sentence = erase_matched_words(sentence, thousands_in_word)
            hundreds_in_digit, hundreds_in_word = NumberFinderHelper.get_hundreds(sentence)
            if hundreds_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, hundreds_in_word):
                str = str + ' ' + hundreds_in_word
                number += hundreds_in_digit
                sentence = erase_matched_words(sentence, hundreds_in_word)
            tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(sentence)
            if tens_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, tens_in_word):
                str = str + ' ' + tens_in_word
                number += tens_in_digit
                sentence = erase_matched_words(sentence, tens_in_word)
            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(sentence)
            if digits_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, digits_in_word):
                str = str + ' ' + digits_in_word
                number += digits_in_digit

            return NumberFinderHelper.to_dict(str, number)
        else:
            return None


class ThousandsFinder:
    @staticmethod
    def find(sentence):
        original = sentence
        thousands_in_digit, thousands_in_word = NumberFinderHelper.get_thousands(sentence)
        if thousands_in_digit != 0:
            str = thousands_in_word
            number = thousands_in_digit
            sentence = erase_matched_words(sentence, thousands_in_word)
            hundreds_in_digit, hundreds_in_word = NumberFinderHelper.get_hundreds(sentence)
            if hundreds_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, hundreds_in_word):
                str = str + ' ' + hundreds_in_word
                number += hundreds_in_digit
                sentence = erase_matched_words(sentence, hundreds_in_word)
            tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(sentence)
            if tens_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, tens_in_word):
                str = str + ' ' + tens_in_word
                number += tens_in_digit
                sentence = erase_matched_words(sentence, tens_in_word)
            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(sentence)
            if digits_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, digits_in_word):
                str = str + ' ' + digits_in_word
                number += digits_in_digit

            return NumberFinderHelper.to_dict(str, number)
        else:
            return None


class HundredsFinder:
    @staticmethod
    def find(sentence):
        original = sentence

        hundreds_in_digit, hundreds_in_word = NumberFinderHelper.get_hundreds(sentence)
        if hundreds_in_digit != 0:
            str = hundreds_in_word
            number = hundreds_in_digit
            sentence = erase_matched_words(sentence, hundreds_in_word)

            tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(sentence)
            if tens_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, tens_in_word):
                str = str + ' ' + tens_in_word
                number += tens_in_digit
                sentence = erase_matched_words(sentence, tens_in_word)

            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(sentence)
            if digits_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, digits_in_word):
                str = str + ' ' + digits_in_word
                number += digits_in_digit

            return NumberFinderHelper.to_dict(str, number)
        else:
            return None


class TensFinder:
    @staticmethod
    def find(sentence):
        original = sentence

        tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(sentence)
        if tens_in_digit != 0:
            str = tens_in_word
            number = tens_in_digit
            right_of_found = erase_beginning_to_matched_word(sentence, tens_in_word)
            sentence = right_of_found if right_of_found is not None else ''

            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(sentence)
            if digits_in_digit != 0 and NumberFinderHelper.check_found_number_in_sentence(original, str, digits_in_word):
                str = str + ' ' + digits_in_word
                number += digits_in_digit

            return NumberFinderHelper.to_dict(str, number)
        else:
            return None


class OnesFinder:
    @staticmethod
    def find(sentence):
        digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(sentence)
        if digits_in_digit != 0:
            str = digits_in_word
            number = digits_in_digit

            return NumberFinderHelper.to_dict(str, number)
        else:
            return None


class NumberFinderHelper:
    @staticmethod
    def get_millions(sentence):
        result = re.search(settings.REGEX_MILLIONS, sentence)

        if result is not None:
            matched = result.group()

            if can_convert_to_int(matched):
                return int(matched), matched

            million_str = erase_matched_words(matched, u'milyon')
            foreword = NumberFinderHelper.get_number_related_forewords(million_str)
            # TODO if foreword is None at this point ??
            val = 1000000
            str = ''
            hundreds_in_digit, hundreds_in_word = NumberFinderHelper.get_hundreds(foreword)
            if hundreds_in_digit != 0:
                str = str + hundreds_in_word + u' '
                foreword = erase_matched_words(foreword, hundreds_in_word)
            tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(foreword)
            if tens_in_digit != 0:
                str = str + tens_in_word + u' '
                foreword = erase_matched_words(foreword, tens_in_word)
            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(foreword)
            if digits_in_digit != 0:
                str = str + digits_in_word + u' '
                foreword = erase_matched_words(foreword, digits_in_word)

            total_multiplier = NumberFinderHelper.__calculate_prefix_of_number((hundreds_in_digit, tens_in_digit, digits_in_digit))
            str = erase_extra_whitespaces(str)
            return (val * total_multiplier, str + u' milyon') if total_multiplier >= 1 else (val, u'bir milyon')
        return 0, ''

    @staticmethod
    def get_thousands(sentence):
        result = re.search(settings.REGEX_THOUSANDS, sentence)

        if result is not None:
            matched = result.group()

            if can_convert_to_int(matched):
                return int(matched), matched

            thousand_str = erase_matched_words(matched, u'bin')
            val = 1000
            str = ''

            hundreds_in_digit, hundreds_in_word = NumberFinderHelper.get_hundreds(thousand_str)
            if hundreds_in_digit != 0:
                str = str + hundreds_in_word + ' '
                thousand_str = erase_matched_words(thousand_str, hundreds_in_word)
            tens_in_digit, tens_in_word = NumberFinderHelper.get_tens(thousand_str)
            if tens_in_digit != 0:
                str = str + tens_in_word + ' '
                thousand_str = erase_matched_words(thousand_str, tens_in_word)
            digits_in_digit, digits_in_word = NumberFinderHelper.get_digits(thousand_str)
            if digits_in_digit != 0:
                str = str + digits_in_word + ' '
                thousand_str = erase_matched_words(thousand_str, digits_in_word)

            total_multiplier = NumberFinderHelper.__calculate_prefix_of_number((hundreds_in_digit, tens_in_digit, digits_in_digit))

            str = erase_extra_whitespaces(str)
            return (val * total_multiplier, str + u' bin') if total_multiplier >= 1 else (val, u'bin')
        return 0, ''

    @staticmethod
    def get_hundreds(sentence):
        result = re.search(settings.REGEX_HUNDREDS, sentence)

        if result is not None:
            matched = result.group()

            if can_convert_to_int(matched):
                return int(matched), matched

            hundred_str = erase_matched_words(matched, u'yüz')
            val = 100

            in_digit, in_words = NumberFinderHelper.get_digits(hundred_str)

            if in_digit == 0 or in_digit == 1:
                 str = u'yüz'

            else:
                if in_digit == 1:
                     str = u'yüz'
                else:
                    val = val * in_digit
                    str = in_words + u' yüz'

            return val, str
        return 0, ''

    @staticmethod
    def get_tens(sentence):
        result = re.search(settings.REGEX_TWO_DIGITS, sentence)
        if result is not None:
            tens_str = result.group()
            # if can_convert_to_int(tens_str):
            #     return int(tens_str), tens_str

            if NumberFinderHelper.is_prefix_whitespace(sentence, tens_str) and NumberFinderHelper.is_postfix_correct(sentence, tens_str):
                return NumberMapper.map_str_to_digit(tens_str), tens_str
        return 0, ''

    @staticmethod
    def get_digits(sentence):
        result = re.search(settings.REGEX_ONE_DIGIT, sentence, flags=re.UNICODE)

        if result is not None:
            digits_str = result.group()

            if NumberFinderHelper.is_prefix_whitespace(sentence, digits_str) and NumberFinderHelper.is_postfix_correct(sentence, digits_str):
                return NumberMapper.map_str_to_digit(digits_str), digits_str
        return 0, ''

    @staticmethod
    def is_prefix_whitespace(sentence, found):
        index = sentence.find(found)
        return index == 0 or sentence[index-1] == ' '

    @staticmethod
    def is_postfix_correct(sentence, found):
        index = sentence.find(found)
        substring = sentence[index+len(found): len(sentence)]
        tmp = perform_whitespace_tokenizer(substring) if substring != '' and substring[0] != ' ' else ['']

        postfix = tmp[0] if len(tmp) > 0 else None

        return postfix is None or postfix == '' or re.search(ur'\b%s' % settings.REGEX_APPENDIX, postfix) is not None


    @staticmethod
    def __calculate_prefix_of_number(numbers):
        return sum(numbers)

    @staticmethod
    def to_dict(word, digit):
        return {
            'word': word,
            'digit': digit
        }

    @staticmethod
    def check_found_number_in_sentence(sentence, old_num_str_, found_num_str):
        str = old_num_str_ + ' ' + found_num_str
        return len(re.findall('(.*?(%s))' % str, sentence)) > 0

    @staticmethod
    def get_number_related_forewords(foreword):
     tmp = []
     s = foreword.split(' ')
     for x in reversed(s):
         match = re.search(settings.REGEX_IS_NUMBER, x)
         if match is not None:
             tmp.append(x)
         else:
             break

     return ' '.join(tmp[::-1]) if len(tmp) > 0 else []


class NumberMapper:
    @staticmethod
    def map_str_to_digit(number_str):
        try:
            digit = int(number_str)
            return digit
        except Exception:
            search = number_str

            mappings = getattr(settings, 'NUMBER_MAPPING')
            match = filter(lambda x: x['word'] == search or x['digit'] == search, mappings)
            if len(match) == 1:
                return match[0]['digit']
            raise Exception('mapping not found')