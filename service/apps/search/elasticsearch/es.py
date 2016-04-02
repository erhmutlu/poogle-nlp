from functools import wraps
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.exceptions import AuthorizationException
import json
from django.conf import settings
from elasticsearch_dsl import DocType
from apps.search.elasticsearch.exceptions import DocTypeRequiredError

__author__ = 'erhmutlu'


def parameter_doc_type_required(orig_func):
    @wraps(orig_func)
    def func(*args, **kwargs):
        doc = kwargs.get('doc', None)
        if doc:
            if issubclass(doc, DocType):
                return orig_func(*args, **kwargs)
            else:
                raise DocTypeRequiredError(doc)
        else:
            raise DocTypeRequiredError

    return func


def index_should_exist(orig_func):
    @wraps(orig_func)
    def func(*args, **kwargs):
        doc = kwargs.get('doc', None)
        if doc:
            index = doc._get_index()
            es = Es()
            exist = es.check_index_exist(index=index)
            if not exist:
                es.init_index(index)
            return orig_func(*args, **kwargs)
        else:
            raise DocTypeRequiredError
        return orig_func

    return func


class Es:

    client = None

    def __init__(self, host=settings.ELASTICSEARCH_HOST):
        self.client = Elasticsearch(host)

    def init_index(self, index):
        self.client.indices.create(index=index)

    def delete_index(self, index):
        self.client.indices.delete(index=index)

    def open_index(self, index):
        self.client.indices.open(index=index)

    def close_index(self, index):
        self.client.indices.close(index=index)

    def check_index_exist(self, index):
        try:
            self.client.indices.get(index=index)
            return True
        except NotFoundError:
            return False

    def check_index_open(self, index):
        try:
            self.client.indices.status(index=index)
            return True
        except AuthorizationException:
            return False

    @parameter_doc_type_required
    @index_should_exist
    def init_mapping(self, doc):
        #TODO close and open should be extracted
        index = doc._get_index()
        self.close_index(index=index)

        doc.init(using=self.client)

        self.open_index(index=index)

    @parameter_doc_type_required
    def delete_doc_item(self, doc, id):
        doc.get(using=self.client, id=id).delete(using=self.client)
