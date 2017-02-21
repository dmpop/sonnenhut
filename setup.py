#!/usr/bin/env python3

from setuptools import setup

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
            if line.startswith('#') or not line:
                continue
            modules.append(line)
    return modules

setup(name='sonnenhut',
      version='1.0',
      description='A simple tool for photographers',
      author='Dmitri Popov',
      author_email='dpopov@suse.de',
      url='https://github.com/dmpop/sonnenhut',
      scripts=['bin/sonnenhut.py'],
      install_requires=requires('requirements.txt'),
)
