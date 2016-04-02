__author__ = 'erhmutlu'

from django.apps import AppConfig


class NLPDefaultApp(AppConfig):
    name = 'apps.defaultapp'
    label = 'defaultapp'
    verbose_name = "Default App"


class SearchApp(AppConfig):
    name = 'apps.search'
    label = 'search'
    verbose_name = "Search App"
