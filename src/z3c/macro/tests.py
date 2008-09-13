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
import itertools

from zope import component
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from zope.app.testing import setup
from zope.configuration import xmlconfig

import z3c.pt.compat

def setUp(test):
    root = setup.placefulSetUp(site=True)
    test.globs['root'] = root

def setUpZPT(test):
    z3c.pt.compat.config.disable()
    setUp(test)
    
    from zope.app.pagetemplate import metaconfigure
    from z3c.macro import tales
    metaconfigure.registerType('macro', tales.MacroExpression)

    # register provider TALES
    from zope.app.pagetemplate import metaconfigure
    from zope.contentprovider import tales
    metaconfigure.registerType('provider', tales.TALESProviderExpression)

def setUpZ3CPT(suite):
    z3c.pt.compat.config.enable()
    setUp(suite)
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()

    from z3c.macro import tales
    component.provideUtility(
        tales.z3cpt, name='macro')
    
def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    tests = ((
        DocFileSuite('README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        DocFileSuite('zcml.txt', setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ) for setUp in (setUpZ3CPT, setUpZPT))

    return unittest.TestSuite(itertools.chain(*tests))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
