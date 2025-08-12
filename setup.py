#!/usr/bin/env python3

from setuptools import setup

setup(name='anigit',
      version='1.0',
      packages=['anigit'],
      entry_points={
          'console_scripts': [
              'anigit = anigit.cli:main'
          ]
      })
