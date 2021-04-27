# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in edu_tz/__init__.py
from edu_tz import __version__ as version

setup(
	name='edu_tz',
	version=version,
	description='edu_tz',
	author='Aakvatech',
	author_email='info@aakvatech.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
