from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='metalang',
      version=version,
      description="",
      long_description="",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='',
      author='',
      author_email='johnjohn.tedro@gmail.com',
      url='toolchain.eu',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data = {
        # Include all templates.
        'metalang': [
          'data/*.tpl.py',
          'data/*.tpl.cpp',
          'data/*.tpl.hpp'
        ]
      },
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        "pyparsing"
      ],
      entry_points={
        "console_scripts": """
          metalang = metalang:entrypoint
        """
        }
      )
