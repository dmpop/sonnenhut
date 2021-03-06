Sonnenhut 1.4.0
===============

.. image:: https://travis-ci.org/dmpop/sonnenhut.svg?branch=develop
    :target: https://travis-ci.org/dmpop/sonnenhut

A simple Python-based web app for photographers that displays basic information such
as current weather conditions and golden hour for a specified location.

The app provides the following information:

-  Geographical coordinates and time zone of the specified city
-  Random Unsplash photo taken in the specified city
-  Golden hour start and duration
-  Weather forecast
-  Current temperature, wind speed, and precipitation probability

The app also shows notes from the accompanying *sonnenhut.md* file
(created automatically during the first run) and articles from the RSS feed
specified in the *sonnenhut.ini* file.

Quick Start
===========

#. Run the following command to install Sonnenhut::

     $ pip3 install git+https://github.com/dmpop/sonnenhut.git@develop

#. Modify the *sonnenhut.ini* file, if necessary.

#. To update Sonnenhut, run the following command::

     $ pip3 install -U git+https://github.com/dmpop/sonnenhut.git@develop

Installation
============

#. Install the required packages:

   * openSUSE::

       $ sudo zypper in python3 python3-virtualenv python3-pip

   * Fedora::

       $ sudo dnf install python3 python3-virtualenv python3-pip

   * Debian and Ubuntu::

       $ sudo apt-get install python3 python3-venv python3-virtualenv python3-pip

#. Clone the project's repository::

    $ git clone https://github.com/dmpop/sonnenhut
    $ cd sonnenhut

#. Create a Python 3 environment and activate it::

    $ python3 -m venv .env
    $ source .env/bin/activate

#. Optionally update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the required modules::

    $ pip install -r requirements.txt

#. Install the package::

    $ ./setup.py develop

#. Edit the ``sonnenhut.ini`` configuration file, if necessary.

Usage
-----

Run the ``sonnenhut`` command and point your browser to
`<http://127.0.0.1:8080/sonnenhut/city>`_ (replace *city* with the actual name of the
desired city).

Add notes to the *sonnenhut.md* text file. You can use Markdown for text formatting.

Credits
-------

Thanks to Thomas Schraitle for help and guidance.

License
-------

`The GNU General Public License version
3 <https://www.gnu.org/licenses/gpl-3.0.txt>`__
