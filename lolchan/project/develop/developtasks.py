import os
import shutil
from os.path import exists, join
import textwrap
from invoke import task, run
from invoke_extras.context_managers import shell_env


DUMPDATA_DATAFILE = join(
    'lolchan', 'project', 'develop', 'dumps', 'dev', 'data.json')
LANGUAGE_CODES = ['en', 'nb']


def _manage(args, echo=True, **kwargs):
    command = 'python manage.py {0} --traceback'.format(args)
    return run(command, echo=echo, **kwargs)


@task
def migrate(djangoenv='develop'):
    """
    Runs the migrate django management command.
    """
    with shell_env(DJANGOENV=djangoenv):
        _manage('migrate --noinput')



@task
def resetdb(djangoenv='develop'):
    """
    Remove db.sqlite if it exists, and run the ``migrate`` task.
    """
    with shell_env(DJANGOENV=djangoenv):
        _manage('dbdev_reinit')
    migrate(djangoenv)


@task
def recreate_devdb(djangoenv='develop'):
    """
    Recreate the test database.
    """
    resetdb(djangoenv)
    with shell_env(DJANGOENV=djangoenv, IEVV_ELASTICSEARCH_DO_NOT_REGISTER_INDEX_UPDATE_TRIGGERS='true'):
        _manage('loaddata {}'.format(DUMPDATA_DATAFILE))
        _manage('ievv_elasticsearch_rebuild_index ALL')


@task
def dbdev_restore_and_migrate(backupdirectory):
    """
    Restore from the given dbdev backup and migrate the database.

    Example::

        $ inv dbdev_restore_and_migrate dbdev_tempdata/PostgresBackend-backups/backup-2015-06-05_15-16-08-176777
    """
    _manage('dbdev_restore {}'.format(backupdirectory))
    migrate()


@task
def dump_devdb_as_json():
    result = _manage('dumpdata --indent=2 --exclude=contenttypes '
                     '--exclude=auth.Permission '
                     '--exclude=thumbnail.KVStore '
                     '--exclude=sessions.Session', hide=True)
    with open(DUMPDATA_DATAFILE, 'wb') as outfile:
        outfile.write(result.stdout.encode('utf-8'))


@task
def makemessages():
    """
    Runs /path/to/reporoot/manage.py makemessages for the given locale (default to nb).
    """
    for languagecode in LANGUAGE_CODES:
        _manage('makemessages -l {} -i "static/*" -i "libs/*"'.format(languagecode))


@task
def compilemessages():
    """
    Runs /path/to/reporoot/manage.py compilemessages.
    """
    _manage('compilemessages')
