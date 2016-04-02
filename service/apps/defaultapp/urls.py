from apps.defaultapp.views import EntityViewSet
from apps.defaultapp.views.intent import IntentViewSet
from apps.defaultapp.views.intent_recognition import IntentRecognitionViewSet

__author__ = 'erhmutlu'

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'entity', EntityViewSet, base_name='entity')
router.register(r'entity/match/$', EntityViewSet.as_view({'get': 'match'}), base_name='entity-match')
router.register(r'intent', IntentViewSet, base_name='intent')
router.register(r'intent/match/$', IntentViewSet.as_view({'get': 'match'}), base_name='intent-match')

router.register(r'intent-recognition', IntentRecognitionViewSet, base_name='intent-recognition')


urlpatterns = [
    url(r'api/', include(router.get_urls())),
    url(r'^', include('poogleauth.urls')),
    # url(r'', include('apps.poogleauth.urls')),
]
