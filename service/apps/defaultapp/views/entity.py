import json
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_406_NOT_ACCEPTABLE, HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, \
    HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from elasticsearch_dsl import Q
from apps.defaultapp.es_docs import Entity
from apps.defaultapp.serializers.entity import EntitySerializer
from poogleauth.permissions import IsAdmin
from apps.search.elasticsearch.es import Es
from apps.search.elasticsearch.query_executor import QueryExecutor

__author__ = 'erhmutlu'


class EntityViewSet(viewsets.ViewSet):
    permission_classes = (IsAdmin,)

    def create(self, request):
        serializer = EntitySerializer(data=request.data)

        if serializer.is_valid():
            validated = serializer.validated_data

            synonyms = validated.get('entity_synonyms')
            key = validated.get('entity_key')
            presentation_value = validated.get('presentation_value')

            es = Es()

            boolQuery = Q('bool', should=[])
            for synonym in synonyms:
                boolQuery.should.append(Q('match', entity_synonyms=synonym))

            search_result = QueryExecutor.execute_search(es.client, Entity, boolQuery)

            if len(search_result) == 0:
                e = Entity(entity_synonyms=synonyms, entity_key=key, presentation_value=presentation_value)
                e.save(using=es.client)
                return Response(e.dict_with_id(), status=HTTP_201_CREATED)

            else:
                return Response({"message": "Already exist!", 'match': search_result}, status=HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'Missing parameters!'}, status=HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'])
    def match(self, request):
        searched = request.query_params.get('synonym', None)
        if searched:
            es = Es()
            q = Q('match', entity_synonyms=searched)
            search_result = QueryExecutor.execute_search(es.client, Entity, q)
            if len(search_result) > 0:
                return Response(search_result, status=HTTP_302_FOUND)
            else:
                return Response({"message": 'not found any match!'}, status=HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Missing parameters!'}, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if not pk:
            return Response({'message': 'Missing parameters!'}, status=HTTP_400_BAD_REQUEST)

        try:
            es = Es()
            es.delete_doc_item(doc=Entity, id=pk)

            return Response({'message': 'Entity is deleted!'})
        except Exception as e:
            return Response({'message': 'Entity with id \'%s\' could not found!' % pk}, status=HTTP_404_NOT_FOUND)




