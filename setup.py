#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import flake8 as flake8
# import tox as tox

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'psutil',
    'requests'
]

test_requirements = [
    'flake8',
    'tox',
    'mock',
    'coverage'
]

setup(
    name='remotestatsclient',
    version='0.1.0',
    description="RemoteStats makes possible to inspect realtime information "
                "about a remote machine using a browser. This is the client"
                " to be installed in such machine.",
    long_description=readme + '\n\n' + history,
    author="Hugo Sadok",
    author_email='hugo@sadok.com.br',
    url='https://github.com/hugombarreto/remotestatsclient',
    packages=[
        'remotestatsclient',
    ],
    package_dir={'remotestatsclient':
                 'remotestatsclient'},
    entry_points={'console_scripts':
                      ['remotestatsclient=remotestatsclient.__main__:main']},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='remotestatsclient',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
