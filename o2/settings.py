# -*- coding: utf-8 -*-
import os
import mongoengine
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

ADMINS = (
    (u'Adriel Café', 'ac@adrielcafe.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
        #'NAME': os.path.join(PROJECT_DIR, 'o2.db'),
        #'USER': '',
        #'PASSWORD': '',
        #'HOST': '', 
        #'PORT': '',
    }
}
DATABASES['default'] =  dj_database_url.config()

MONGODB_USER = 'admin'
MONGODB_PASSWORD = 'admin'
#MONGODB_HOST = 'ds053148.mongolab.com'
#MONGODB_PORT = '53148'
MONGODB_HOST = '130.206.82.56'
MONGODB_PORT = '27017'
MONGODB_NAME = 'o2'
MONGODB_CONNECTION_STRING = 'mongodb://%s:%s@%s:%s/%s' % (MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST, MONGODB_PORT, MONGODB_NAME)

FIWARE_AUTH_USERNAME = 'ac@adrielcafe.com'
FIWARE_AUTH_PASSWORD = 'Cafe5813'

ALLOWED_HOSTS = ['*']

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

MEDIA_ROOT = 'mediafiles'
MEDIA_URL = '/media/'
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'ns(_6y=xj=b@jgx^$i9(7u$)7wqdt6r6s(%ph9$iymh5+n=(96'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'o2.urls'

WSGI_APPLICATION = 'o2.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'mongoengine.django.mongo_auth',
    'social.apps.django_app.me',
    'tastypie',
    'tastypie_mongoengine'
)

AUTH_USER_MODEL = 'mongo_auth.MongoUser'

MONGOENGINE_USER_DOCUMENT = 'o2.models.User'

SOCIAL_AUTH_USER_MODEL = 'o2.models.User'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'mongoengine.django.auth.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect'
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data'
)

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'

SOCIAL_AUTH_FACEBOOK_KEY = '597739496934802'
SOCIAL_AUTH_FACEBOOK_SECRET = 'ed997f5165d562f49b6fe498a308a902'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_about_me', 'user_birthday', 'user_location', 'user_website', 'user_photos', 'publish_actions']
SOCIAL_AUTH_TWITTER_KEY = '4Fy5wNNuuMxYL2HlY1a2ZQ'
SOCIAL_AUTH_TWITTER_SECRET = 'pZsAr29ZsVD2CXH1xWV3KBQquJfXEZuLtxYkYRNuUhE'
SOCIAL_AUTH_FOURSQUARE_KEY = '2BSOB3BLHD1WTQ5XZYWIKAGZ4ZEK2Q0M3A0JBZ0RS3YK0VCB'
SOCIAL_AUTH_FOURSQUARE_SECRET = 'LZXUBC0RLAXHM1IRJXD55JV13XW1QEENNIEKJGHEJ0CQMIVS'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1026711578846.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'GxvE4Iq1oNVp0HeaALdKhovU'
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = 'azslg0oxmogc'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = '3EluuYKygv1BQVX2'

LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/user/profile/'
URL_PATH = ''

SESSION_ENGINE = 'mongoengine.django.sessions'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Heroku Config
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


mongoengine.connect(MONGODB_NAME, host = MONGODB_CONNECTION_STRING)

try:
    from mongoengine.django.auth import Group
    
    group_count = Group.objects.count()
    if group_count == 0:
        group_users = Group(name = 'users')
        group_users.save()
        group_ombudsman = Group(name = 'ombudsman')
        group_ombudsman.save()
except Exception, e: 
    print str(e)