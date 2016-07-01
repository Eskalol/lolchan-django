import urlparse
from lolchan.project.default.settings import *  # noqa
import os


ROOT_URLCONF = 'lolchan.project.production.urls'

DEBUG = False
LANGUAGE_CODE = 'nb'
INSTALLED_APPS += (
    'gunicorn',
)


###########################
# Database
###########################
DATABASES = {}

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()


###########################
# Templates
###########################
TEMPLATES[0]['OPTIONS']['debug'] = False


########################################
# Cache
########################################
# Cache with https://addons.heroku.com/memcachedcloud
redis_url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '{hostname}:{port}'.format(
            hostname=redis_url.hostname, port=redis_url.port),
        'OPTIONS': {
            'PASSWORD': redis_url.password,
            'DB': 0,
        }
    }
}

#################################
# Heroku settings
#################################
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


#################################
# AWS settings
#################################
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SECURE_URLS = False
AWS_ACCESS_KEY_ID = os.environ['DJANGO_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['DJANGO_AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME']
MEDIA_URL = '//{bucket}.s3.amazonaws.com/'.format(bucket=AWS_STORAGE_BUCKET_NAME)

# Where to put user uploaded files relative to the root of the bucket?
MEDIA_ROOT = 'django_media_root'


##################################
# Search
##################################
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#         'URL': os.environ['SEARCHBOX_URL'],
#         'INDEX_NAME': 'documents',
#     },
# }


#################################
# Email
#################################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['MANDRILL_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['MANDRILL_APIKEY']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'eskil@appresso.no'



############################
# Force https
############################
MIDDLEWARE_CLASSES += [
    'lolchan.lolchan_core.middleware.SslSecureMiddleware',
]


############################
# Logging
############################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(name)s %(pathname)s:%(lineno)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stderr': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': False
        },
        'boto': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': True
        },
        'django.db': {
            'handlers': ['stderr'],
            'level': 'INFO',  # Do not set to debug - logs all queries
            'propagate': False
        },
        '': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
