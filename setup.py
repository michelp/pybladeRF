#!/usr/bin/env python
"""
=========
pybladeRF
=========
"""
from setuptools import setup, find_packages

setup(
  name="pybladeRF",
  version="0.0.1",
  packages=find_packages(exclude=['tests.*', 'tests', '.virt']),

  tests_require=['nose'],
  test_suite='nose.collector',

  author='Michel Pelletier',
  author_email='pelletier.michel@yahoo.com',
  description='pyczmq libbladeRF wrapper',
  long_description=__doc__,
  license='LGPL v3',
  url='https://github.com/michelp/pyczmq',
      install_requires=[
        'cffi',
        ],
)
