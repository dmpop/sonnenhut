Sonnenhut 1.0.1
===============

A simple Python script for photographers that displays basic information such
as current weather conditions and golden hour for a specified location.

The script provides the following information:

-  Golden hour start and duration
-  Brief weather summary
-  Current temperature, wind speed, and humidity
-  Precipitation warning

The script also shows notes from the accompanying *sonnenhut.txt* file
(created automatically during the fist run).

Installation
============

To install Sonnenhut, use the following steps:

#. Clone this repository::

    $ git clone https://github.com/dmpop/sonnenhut
    $ cd sonnenhut

#. Create a Python 3 environment and activate it::

    $ pyvenv .env
    $ source .env/bin/activate

#. Optionally update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the package::

    $ ./setup.py develop

If you need to install it from GitHub directly, use this URL::

    git+https://github.com/dmpop/sonnenhut.git@develop

After the installation in your Python virtual environment, the script
`sonnenhut` is available.

Usage
-----

Run the ``./sonnenhut.py fürth`` command (replace *fürth* with the desired city)

For quick access, create an alias in the *~/.bashrc* file (replace
*fürth* with the desired city):

::

    alias sonnenhut='/path/to/sonnenhut.py fürth'

Credits
-------

Thanks to Thomas Schraitle for help and guidance.

License
-------

`The GNU General Public License version
3 <https://www.gnu.org/licenses/gpl-3.0.txt>`__
