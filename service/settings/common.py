# -*- coding: utf-8 -*-

__author__ = 'erhmutlu'

#TODO this should be added
SECRET_KEY = 'dbx657err4u@70t&=o-e7n^3zm(ayn$pqpq4rln_i6!(ynqs0r'


LOCAL_APPS = (
    'apps.apps.SearchApp',
    'apps.apps.NLPDefaultApp',
)

THIRDPARTY_APPS = (
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'django_extensions',
    'poogleauth'
)


DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRDPARTY_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer'
    ),
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'apps.defaultapp.wsgi.application'
ROOT_URLCONF = 'apps.defaultapp.urls'

STATIC_URL = '/static/'

AUTH_USER_MODEL = "poogleauth.User"


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


NUMBER_MAPPING =[
    {"word": u"bir", "digit": 1},
    {"word": u"iki", "digit": 2},
    {"word": u"üç", "digit": 3},
    {"word": u"dört", "digit": 4},
    {"word": u"beş", "digit": 5},
    {"word": u"altı", "digit": 6},
    {"word": u"yedi", "digit": 7},
    {"word": u"sekiz", "digit": 8},
    {"word": u"dokuz", "digit": 9},
    {"word": u"on", "digit": 10},
    {"word": u"yirmi", "digit": 20},
    {"word": u"otuz", "digit": 30},
    {"word": u"kırk", "digit": 40},
    {"word": u"elli", "digit": 50},
    {"word": u"altmış", "digit": 60},
    {"word": u"yetmiş", "digit": 70},
    {"word": u"seksen", "digit": 80},
    {"word": u"doksan", "digit": 90},
    {"word": u"yüz", "digit": 100},
    {"word": u"bin", "digit": 1000},
    {"word": u"milyon", "digit": 1000000},
]

REGEX_MILLIONS = ur'(.*?)milyon|([1-9]{1}[0-9]{6,8})'
REGEX_THOUSANDS = ur'(.*?)bin|([1-9]{1}[0-9]{3,5})'
REGEX_HUNDREDS = ur'(.*?)yüz|([1-9]{1}[0-9]{2})'
REGEX_TWO_DIGITS = ur'\b((on)|(yirmi)|(otuz)|(kırk)|(elli)|(seksen)|(doksan))\b|\b(altmış)|(yetmiş)|\b([1-9]{1}[0-9]{1})'
REGEX_ONE_DIGIT = ur'(\b((bir)|(iki)|(dört)|(yedi)|(sekiz)|(dokuz))\b)|(üç)|\b((beş)|(altı))|\b([1-9]{1})'


REGEX_IS_NUMBER = ur'%s|%s|%s|%s|%s' % (REGEX_MILLIONS, REGEX_THOUSANDS, REGEX_HUNDREDS, REGEX_TWO_DIGITS, REGEX_ONE_DIGIT)

REGEX_NUMBER_AS_WORD = ur'(milyon)|(bin)|(yüz)'

REGEX_APPENDIX = ur'[\']*(da[n]{0,1}|de[n]{0,1}|ta[n]{0,1}|te[n]{0,1})\b'




ENTITY_KEY_CURRENCY = '@Currency'
ENTITY_KEY_NUMBER = '@Number'
ENTITY_KEY_CITY = '@City'
ENTITY_KEY_MONTH = '@Month'
ENTITY_KEY_TEAM = '@TEAM'

SHAPER_CLASS_MAPPINGS = [
    {'action': 'convert_currency_units', 'clz': 'Currency'},
    {'action': 'get_weather_by_city', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_hour', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_date', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_date_hour', 'clz': 'Weather'},
    {'action': 'get_teams_match_score', 'clz': 'Score'},
    {'action': 'get_matches_of_week', 'clz': 'Score'},
    {'action': 'get_films_release_soon', 'clz': 'Movie'},
    {'action': 'get_films_released_already', 'clz': 'Movie'},
    {'action': 'get_films_released_this_week', 'clz': 'Movie'}
]