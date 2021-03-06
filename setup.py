#!/usr/bin/env python3

from setuptools import setup
from setuptools import find_packages


def requires(filename):
    """Returns a list of all pip requirements

    :param filename: the Pip requirement file (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    modules = []
    with open(filename, 'r') as pipreq:
        for line in pipreq:
            line = line.strip()
            # We don't want empty lines or lines referring to other files
            if line.startswith('#') or line.startswith('-r') or not line:
                continue
            modules.append(line)
    return modules


setup(name='sonnenhut',
      version='1.4.0',
      description='Simple dashboard for photographers',
      author='Dmitri Popov',
      author_email='dpopov@suse.de',
      url='https://github.com/dmpop/sonnenhut',
      scripts=['bin/sonnenhut'],
      include_package_data=True,
      data_files=[('sonnenhut', ['src/sonnenhut/sonnenhut.ini'])],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=requires('requirements.txt'),
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Framework :: Bottle',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Utilities'
                   ],
      # For "setup.py test"
      setup_requires=['pytest-runner'],
      tests_require=requires('devel_requirements.txt'),
      )
