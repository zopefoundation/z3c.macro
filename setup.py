##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


CHAMELEON_REQUIRES = [
    'z3c.pt >= 2.1',
    'z3c.ptcompat >= 1.0',
]

TESTS_REQUIRE = CHAMELEON_REQUIRES + [
    'z3c.template',
    'zope.browserpage >= 3.12',
    'zope.testing',
    'zope.testrunner',
]

setup(
    name='z3c.macro',
    version='2.2.1',
    author="Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Simpler definition of ZPT macros.",
    long_description=(
        read('README.rst')
        + '\n\n' +
        'Detailed Documentation\n'
        '======================\n'
        + '\n\n' +
        read('src', 'z3c', 'macro', 'README.rst')
        + '\n\n' +
        read('src', 'z3c', 'macro', 'zcml.rst')
        + '\n\n' +
        read('CHANGES.rst')
    ),
    license="ZPL 2.1",
    keywords="zope3 macro pagetemplate zpt",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope :: 3',
    ],
    url='https://github.com/zopefoundation/z3c.macro',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require={
        'test': TESTS_REQUIRE,
        'chameleon': CHAMELEON_REQUIRES,
    },
    install_requires=[
        'setuptools',
        'zope.component',
        'zope.configuration',
        'zope.interface',
        'zope.pagetemplate >= 3.6.2',
        'zope.publisher',
        'zope.schema',
        'zope.tales',
    ],
    tests_require=TESTS_REQUIRE,
    test_suite='z3c.macro.tests.test_suite',
    include_package_data=True,
    zip_safe=False,
)
