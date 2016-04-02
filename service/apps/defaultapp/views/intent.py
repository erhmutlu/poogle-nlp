from elasticsearch_dsl import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE, HTTP_404_NOT_FOUND, \
    HTTP_302_FOUND
from apps.defaultapp.es_docs import Intent
from apps.defaultapp.serializers.intent import IntentSerializer
from poogleauth.permissions import IsAdmin
from apps.search.elasticsearch.es import Es
from apps.search.elasticsearch.query_executor import QueryExecutor

__author__ = 'erhmutlu'


class IntentViewSet(viewsets.ViewSet):
    permission_classes = (IsAdmin,)

    def create(self, request):
        data = request.data

        serializer = IntentSerializer(data=data)
        if serializer.is_valid():
            validated = serializer.validated_data

            sentence = validated.get('sentence')
            params = validated.get('params')
            action = validated.get('action')

            es = Es()

            words = sentence.split(' ')
            should = []
            for word in words:
                should.append(Q('match', original_sentence=word))

            words_code = len(words)
            boolQuery = Q('bool', should=should, minimum_should_match=words_code)

            search_result = QueryExecutor.execute_search(es.client, Intent, boolQuery)

            matched = []
            for obj in search_result:
                tmp = obj['sentence'].split(' ')
                if len(tmp) == words_code:
                    matched.append(obj)

            if len(matched) == 0:
                i = Intent(sentence=sentence, params=params, action=action, original_sentence=sentence)
                i.save(using=es.client)
                return Response(i.dict_with_id(), status=HTTP_201_CREATED)
            else:
                return Response({"message": "found a match!", 'match': search_result}, status=HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'Parameter error!'}, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def match(self, request):
        searched = request.query_params.get('sentence', None)
        if searched:
            es = Es()
            words = searched.split(' ')

            should = []
            for word in words:
                should.append(Q('match', original_sentence=word))

            words_code = len(words)
            boolQuery = Q('bool', should=should, minimum_should_match=words_code)

            search_result = QueryExecutor.execute_search(es.client, Intent, boolQuery)

            if len(search_result) > 0:
                matched = []
                similar = []
                for obj in search_result:
                    tmp = obj['sentence'].split(' ')
                    if len(tmp) == words_code:
                        matched.append(obj)
                    else:
                        similar.append(obj)

                return Response({"similar": similar, "best_matches": matched }, status=HTTP_302_FOUND)
            else:
                return Response({"message": 'not found any match!'}, status=HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'Missing parameters!'}, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if not pk:
            return Response({'message': 'Missing parameters!'}, status=HTTP_400_BAD_REQUEST)

        try:
            es = Es()
            es.delete_doc_item(doc=Intent, id=pk)

            return Response({'message': 'Intent is deleted!'})
        except Exception as e:
            return Response({'message': 'Intent with id \'%s\' could not found!' % pk}, status=HTTP_404_NOT_FOUND)