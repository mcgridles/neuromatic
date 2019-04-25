#!/usr/bin/env python
from setuptools import setup

setup(
    name='neuromatic',
    version='1.0',
    description='Neural network prototyping tool built on Keras',
    author='Connor Arnold, Henry Gridley, Griffin Knipe, & Daniel Vosburg',
    url='https://github.com/mcgridles/neuromatic/',
    packages=['backend', 'examples', 'files', 'interface', 'logs', 'tests'],
    install_requires=[
        'keras==2.1.6',
        'pandas>=0.23.3',
        'sklearn>=0.0',
	'kiwisolver==1.0.1',
        'tensorflow==1.9.0',
        'numpy>=1.15.0',
        'scikit-learn>=0.19.2',
        'scipy>=1.1.0',
        'six>=1.11.0',
        'pytz>=2018.5',
        'python-dateutil>=2.7.3',
        'opencv-python>=3.4.2.17',
        'matplotlib>=2.2.3',
        'h5py>=2.8.0',
        'pyyaml>=3.13',
        'cython>=0.28.5',
        'absl-py'
    ]
)
