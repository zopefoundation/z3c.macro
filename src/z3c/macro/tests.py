##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
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
"""Viewlet tests

$Id$
"""
__docformat__ = 'restructuredtext'

import unittest
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import setup


def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

    from zope.app.pagetemplate import metaconfigure
    from z3c.macro import tales
    metaconfigure.registerType('macro', tales.MacroExpression)

    # register provider TALES
    from zope.app.pagetemplate import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)


def tearDown(test):
    setup.placefulTearDown()


def test_suite():
    return unittest.TestSuite((
        DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
