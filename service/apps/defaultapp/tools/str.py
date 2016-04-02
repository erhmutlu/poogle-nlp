# -*- coding: utf-8 -*-

import re
from django.conf import settings

__author__ = 'erhmutlu'


def erase_extra_whitespaces(str):
    regex = re.compile('([ ]{2,})')
    return regex.sub(' ', str.lower()).strip()


def erase_punctuation_signs(str):
    regex = re.compile('[:\.\?,]+')
    tmp = regex.sub(' ', str.lower()).strip()

    regex = re.compile("\'[A-Za-z]+")
    return regex.sub('', str)


def erase_matched_words(sentence, searched):

    if can_convert_to_int(searched):
        return __erase_matched_int_value(sentence, searched)

    reg_str = '(%s)[\S]*'

    try:
        regex = re.compile(reg_str % (str(searched).lower()))
    except UnicodeEncodeError as e:
        regex = re.compile(reg_str % unicode(searched).lower())

    erased = regex.sub('', sentence.lower())
    return erase_extra_whitespaces(erased)


def __erase_matched_int_value(sentence, searched):
    reg_str = '(%s)\W'
    found = re.findall(reg_str % searched, sentence)
    if len(found) > 0:
        f = found[0]
        index = find_index_of_word(sentence, f)
        erased = sentence[0:index] + ' ' + sentence[index+len(f): len(sentence)]
    else:
        reg_str = '(%s)'
        regex = re.compile(reg_str % (str(searched).lower()))
        erased = regex.sub('', sentence.lower())

    return erased


def erase_beginning_to_matched_word(sentence, searched):
    s = to_string(searched).lower()

    if len(s.split(' ')) == 1:
        results = re.findall('(%s[\S]*)( %s)*' % (s, settings.REGEX_NUMBER_AS_WORD), sentence)
        if len(results) >= 1:
            for result in results:
                res = erase_extra_whitespaces(' '.join(result))
                if res == s:
                    index = find_index_of_word(sentence, res)
                    erased = sentence[index+len(res):len(sentence)]
                    return erase_extra_whitespaces(erased)
    else:
        regex = re.compile('(.*?)(%s)[\S]*' % s)
        erased = regex.sub('', sentence.lower())
        return erase_extra_whitespaces(erased)


def erase_matched_word_to_end(sentence, searched):
    s = to_string(searched).lower()

    if len(s.split(' ')) == 1:
        results = re.findall(ur'(%s[\S]*)( %s)*' % (s, settings.REGEX_NUMBER_AS_WORD), sentence)
        if len(results) >= 1:
            for result in results:
                res = erase_extra_whitespaces(' '.join(result))
                if res == s or re.search('(%s[\S])' % s, res) is not None:
                    index = find_index_of_word(sentence, res)
                    erased = sentence[0:index]
                    return erase_extra_whitespaces(erased)
    else:
        regex = re.compile('(%s)[ \S]*' % s)
        erased = regex.sub('', sentence.lower())
        return erase_extra_whitespaces(erased)


def can_convert_to_int(str):
    try:
        i = int(str)
        return True
    except Exception:
        return False


def is_blank_or_none(str):
    return str is None or re.match('[ ]+', str) or str == ''


def find_index_of_word(sentence, word):

    try:
        w = str(word)
    except UnicodeEncodeError as e:
        w = unicode(word)

    if not can_convert_to_int(word):
        w = w.lower()

    return sentence.lower().find(w)


def to_string(input):
    try:
        s = str(input)
    except UnicodeEncodeError as e:
        s = unicode(input)

    return s


def to_two_digit_num(num):
    n = int(num)
    if n in range(0,10):
        val = '0' + str(n)
    else:
        val = str(n)

    return val