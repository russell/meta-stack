#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "python-keystoneclient",
    "python-novaclient",
    "python-neutronclient",
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='meta_stack',
    version='0.1.0',
    description="A tool to help organising accounts and connections to OpenStack.",
    long_description=readme,
    author="Russell Sim",
    author_email='russell.com@gmail.com',
    url='',
    packages=[
        'meta_stack',
    ],
    package_dir={'meta_stack':
                 'meta_stack'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache-2",
    zip_safe=False,
    keywords='meta_stack',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'meta-stack = meta_stack.cli:main',
        ],
    },
)
