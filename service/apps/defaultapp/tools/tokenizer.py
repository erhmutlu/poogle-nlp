from apps.defaultapp.tools.str import erase_extra_whitespaces

__author__ = 'erhmutlu'


def perform_whitespace_tokenizer(val):
    val = erase_extra_whitespaces(val)
    return val.split(' ')
