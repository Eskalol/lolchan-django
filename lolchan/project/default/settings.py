"""
Django settings for lolchan project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from os.path import join
from os.path import dirname
from lolchan.project.default.projectspecific_settings import *  # noqa


REPOROOT_DIR = dirname(dirname(dirname(dirname(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(%a+ly@5m4g6fl2yhc2(i#cfz+x&_$uyh9o8%z6srhk)-)yzm('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'rest_framework_swagger',
    'rest_framework',
    'crispy_forms',
    'django_cradmin.apps.cradmin_generic_token_with_metadata',
    'django_cradmin.apps.cradmin_authenticate',
    'django_cradmin.apps.cradmin_email',
    'ievv_opensource.ievvtasks_common',
    'django_cradmin',
    'lolchan.lolchan_core.apps.LolChanCoreConfig',
    'lolchan.lolchan_lobby',
    'lolchan.lolchan_channel',
    'lolchan.lolchan_api',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

DATETIME_INPUT_FORMATS = (
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
)

LANGUAGE_CODE = 'nb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Setup static files to be served at /static/.
STATIC_URL = '/static/'

# Use bootstrap3 template pack to django-crispy-forms.
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Setup user uploads directory
MEDIA_ROOT = join(REPOROOT_DIR, 'media')
MEDIA_URL = '/media/'


# Thumbnails (sorl-thumbnail)
# See: http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html
#THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'
#THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
#THUMBNAIL_PREFIX = 'sorlcache/'
#THUMBNAIL_DEBUG = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(REPOROOT_DIR,  'templates'),
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django_cradmin.context_processors.cradmin',
            ],
        },
    },
]


###########################
# REST API related settings
###########################

SWAGGER_SETTINGS = {
    'info': {
        'title': 'lolchan API documentation',
    }
}
REST_FRAMEWORK = {
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework_swagger.views.get_restructuredtext',
}
