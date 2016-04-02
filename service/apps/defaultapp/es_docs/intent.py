from elasticsearch_dsl import DocType, String, token_filter, analyzer
from django.conf import settings

__author__ = 'erhmutlu'

turkish_stop = token_filter('turkish_stop', type='stop', stopwords="_turkish_")
turkish_lowercase = token_filter('turkish_lowercase', type='lowercase', language="turkish")
turkish_stemmer = token_filter('turkish_stemmer', type='stemmer', language='turkish')

turkish_whitespace_analyzer = analyzer('turkish_whitespace_analyzer', tokenizer='whitespace', filter=['apostrophe', 'asciifolding',
                                                                                turkish_lowercase, turkish_stop,
                                                                                turkish_stemmer])


class Intent(DocType):
    sentence = String(analyzer=turkish_whitespace_analyzer, include_in_all=True)
    original_sentence = String(analyzer='whitespace', include_in_all=False)
    action = String(index='not_analyzed', include_in_all=False)
    params = String(index='not_analyzed', include_in_all=False)

    def dict_with_id(self):
        dict = super(DocType, self).to_dict()
        dict['id'] = self._id
        return dict

    @classmethod
    def _get_index(self, index=None):
        return settings.ELASTICSEARCH_INDEX

    @classmethod
    def _get_doctype(self):
        return settings.ELASTICSEARCH_INTENT_DOCTYPE

    class Meta:
        index = settings.ELASTICSEARCH_INDEX
        doc_type = settings.ELASTICSEARCH_INTENT_DOCTYPE


