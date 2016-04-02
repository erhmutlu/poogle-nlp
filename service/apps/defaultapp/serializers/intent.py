from rest_framework import serializers

__author__ = 'erhmutlu'


class IntentSerializer(serializers.Serializer):
    sentence = serializers.CharField()
    action = serializers.CharField()
    params = serializers.ListField()
