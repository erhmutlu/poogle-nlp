from rest_framework import serializers

__author__ = 'erhmutlu'


class EntitySerializer(serializers.Serializer):
    entity_key = serializers.CharField()
    entity_synonyms = serializers.ListField()
    value = serializers.CharField()
