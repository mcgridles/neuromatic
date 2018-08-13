#!/usr/bin/env python
from setuptools import setup

setup(name='neuromatic',
      version='1.0',
      description='Neuromatic API',
      author='CDGH',
      url='https://github.com/mcgridles/neuromatic/',
      packages=['backend', 'examples','files','interface','logs','tests'],
      install_requires=[
          'keras',
          'pandas',
          'sklearn',
          'tensorflow',
          'numpy',
          'scikit-learn',
          'scipy',
          'six',
          'pytz',
          'python-dateutil'
      ]
     )