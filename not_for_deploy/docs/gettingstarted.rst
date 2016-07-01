############################################################
Getting started with the Django app and/or the documentation
############################################################


************************
Install the requirements
************************
Install the following:

#. Python
#. PIP_
#. VirtualEnv_
#. virtualenvwrapper_
#. libjpeg, liblcms1, libfreetype6 and zlib for the required format support in Pillow
#. gettext for Django translations
#. nodejs and npm for our clientside stuff


Install the system packages on OSX with Homebrew
================================================
::

    $ brew install libjpeg little-cms freetype lzlib gettext nodejs

And symlink freetype to let Pillow find it (see `this StackOverflow post <http://stackoverflow.com/questions/20325473/error-installing-python-image-library-using-pip-on-mac-os-x-10-9>`_ for details)::

    $ ln -s /usr/local/include/freetype2 /usr/local/include/freetype

You will also have to add gettext to your path if you want to be able to update translation strings. You can eighter run ``brew link gettext --force``, or add ``/usr/local/Cellar/gettext/SOMETHING/bin/`` to your path.


Install the system packages on Ubuntu
================================================
::

    $ sudo apt-get install libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev gettext nodejs



***********************
Install in a virtualenv
***********************
Create a virtualenv using Python 3 (an isolated Python environment)::

    $ mkvirtualenv -p /usr/local/bin/python3 lolchan

Install the development requirements::

    $ pip install -r requirements/develop.txt


.. _enable-virtualenv:

.. note::

    Whenever you start a new shell where you need to use the virtualenv we created
    with ``mkvirtualenv`` above, you have to run::

        $ workon lolchan


*****************
Create a database
*****************
See :doc:`databasedumps`.





**************
Build the docs
**************
:ref:`Enable the virtualenv <enable-virtualenv>`, and run::

    $ cd not_for_deploy/docs/
    $ inv docs

Then open ``_build/index.html`` in a browser.




.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
