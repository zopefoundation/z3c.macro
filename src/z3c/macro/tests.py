##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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

from zope import component
from zope.app.testing import setup
from zope.configuration import xmlconfig
import doctest
import itertools
import unittest
import z3c.pt
import z3c.ptcompat

import z3c.macro.tales
import z3c.macro.zcml

# default template class
_templateViewClass = z3c.macro.zcml.ViewPageTemplateFile


def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root


def setUpZPT(test):
    setUp(test)
    from zope.browserpage import metaconfigure
    metaconfigure.registerType('macro', z3c.macro.tales.MacroExpression)

    # apply correct template classes
    global _templateViewClass
    _templateViewClass = z3c.macro.zcml.ViewPageTemplateFile
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
    z3c.macro.zcml.ViewPageTemplateFile = ViewPageTemplateFile


def setUpZ3CPT(suite):
    setUp(suite)
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()
    xmlconfig.XMLConfig('configure.zcml', z3c.ptcompat)()

    # apply correct template classes
    global _templateViewClass
    _templateViewClass = z3c.macro.zcml.ViewPageTemplateFile
    from z3c.pt.pagetemplate import ViewPageTemplateFile
    z3c.macro.zcml.ViewPageTemplateFile = ViewPageTemplateFile


def tearDown(test):
    setup.placefulTearDown()
    global _templateViewClass
    z3c.macro.zcml.ViewPageTemplateFile = _templateViewClass


def test_suite():
    tests = ((
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        doctest.DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ) for setUp in (setUpZ3CPT, setUpZPT))

    return unittest.TestSuite(itertools.chain(*tests))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
