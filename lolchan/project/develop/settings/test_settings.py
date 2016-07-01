from .developsettings_common import *

# We test against the english original text
LANGUAGE_CODE = 'en'


# Faster tests with less time spent on hashing passwords
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)


# Disable migrations when running tests
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
