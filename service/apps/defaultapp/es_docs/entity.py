from elasticsearch_dsl import DocType, String, token_filter, analyzer
from django.conf import settings

__author__ = 'erhmutlu'

turkish_stop = token_filter('turkish_stop', type='stop', stopwords="_turkish_")
turkish_lowercase = token_filter('turkish_lowercase', type='lowercase', language="turkish")
turkish_stemmer = token_filter('turkish_stemmer', type='stemmer', language='turkish')
custom_shingle_filter = token_filter('custom_shingle_filter', type='shingle', max_shingle_size=3, min_shingle_size=2,
                                     output_unigrams=True)

entity_synonym_index_analyzer = analyzer('entity_synonym_index_analyzer', tokenizer='keyword', filter=[turkish_lowercase, 'asciifolding', turkish_stemmer])

entity_synonym_search_analyzer = analyzer('entity_synonym_search_analyzer', tokenizer='standard',
                                    filter=[turkish_lowercase, 'apostrophe', 'asciifolding',
                                            custom_shingle_filter, turkish_stemmer])


class Entity(DocType):
    entity_synonyms = String(index_analyzer=entity_synonym_index_analyzer,
                             search_analyzer=entity_synonym_search_analyzer,
                             include_in_all=True)
    entity_key = String(index='not_analyzed', include_in_all=False)
    value = String(index='not_analyzed', include_in_all=False)

    @classmethod
    def _get_index(self, index=None):
        return settings.ELASTICSEARCH_INDEX

    @classmethod
    def _get_doctype(self):
        return settings.ELASTICSEARCH_ENTITY_DOCTYPE

    def dict_with_id(self):
        dict = super(DocType, self).to_dict()
        dict['id'] = self._id
        return dict

    class Meta:
        index = settings.ELASTICSEARCH_INDEX
        doc_type = settings.ELASTICSEARCH_ENTITY_DOCTYPE
