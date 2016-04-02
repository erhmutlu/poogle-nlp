from elasticsearch_dsl import Q
__author__ = 'erhmutlu'


class QueryExecutor:

    @staticmethod
    def execute_search(client, doc, query):
        result = doc.search(using=client).query(query).execute()

        hits = []
        for hit in result.hits.hits:
            obj = hit.get('_source')
            obj['id'] = hit.get('_id')
            hits.append(obj)

        return hits

    @staticmethod
    def execute_search_single(client, doc, query):
        result = QueryExecutor.execute_search(client, doc, query)

        return result[0] if result else None
