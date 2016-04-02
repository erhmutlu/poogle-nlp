# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from apps.defaultapp.services.entity import EntityService
from apps.defaultapp.services.intentresponse_shaper import IntentResponseShaper
from apps.defaultapp.services.recognition import IntentRecognitionService
from apps.defaultapp.tools.str import erase_punctuation_signs, erase_extra_whitespaces

__author__ = 'erhmutlu'


class IntentRecognitionViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def recognize(self, request):
        data = request.query_params
        if 'sentence' in data:
            user_input = data.get('sentence')
            user_input = self.__clear_input(user_input)

            entities = EntityService.find_entities(user_input=user_input)
            user_input, keys = IntentRecognitionService.eliminate_entities_in_sentence(user_input=user_input, entities=entities)

            search_result = IntentRecognitionService.exact_recognize(user_input=user_input, keys=keys)
            if search_result is None:
                search_result = IntentRecognitionService.approximate_recognize(user_input=user_input, keys=keys)

            if search_result is not None:
                search_result['params'] = keys

                shape_shifter = IntentResponseShaper()
                response = shape_shifter.shape(data.get('sentence'), search_result)

                return Response(response, status=HTTP_200_OK)
            else:
                return Response({'error': 'Söylediğinizi anlayamadım'}, status=HTTP_404_NOT_FOUND)

        else:
            return Response({'message': 'error'}, status=HTTP_400_BAD_REQUEST)

    def __clear_input(self, user_input):
        user_input = erase_punctuation_signs(user_input)
        user_input = erase_extra_whitespaces(user_input)
        return user_input
