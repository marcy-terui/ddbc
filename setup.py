#!/usr/bin/env python
import os
import ddbc

from setuptools import setup, find_packages

description = 'Amazon DynamoDB as a cache store.'
long_description = description
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup_options = dict(
    name='ddbc',
    version=ddbc.__version__,
    description=description,
    long_description=long_description,
    author='Masashi Terui',
    author_email='marcy9114+pypi@gmail.com',
    url='https://github.com/marcy-terui/ddbc',
    packages=find_packages(exclude=['tests*', 'register']),
    install_requires=open('requirements.txt').read().splitlines(),
    setup_requires=[
        'nose',
        'mock',
        'coverage'
    ],
    license="MIT License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws dynamodb cache lambda',
)

setup(**setup_options)
