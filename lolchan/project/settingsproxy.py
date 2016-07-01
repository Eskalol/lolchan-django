import os

"""
A simple Django settings module proxy that lets us configure Django
using the DJANGOENV environment variable.

Example (running tests)::

    $ DJANGOENV=test python manage.py test

Defaults to the ``develop`` enviroment, so developers can use ``python
manage.py`` without anything extra during development.
"""

DJANGOENV = os.environ.get('DJANGOENV', 'develop')

if DJANGOENV == 'develop':  # Used for local development
    from lolchan.project.develop.settings.develop_settings import *
elif DJANGOENV == 'test':  # Used when running the Django tests locally
    from lolchan.project.develop.settings.test_settings import *
elif DJANGOENV == 'production':  # Used in production
    from lolchan.project.production.production_settings import *
else:
    raise ValueError('Invalid value for the DJANGOENV environment variable: {}'.format(DJANGOENV))
