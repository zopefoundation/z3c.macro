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
"""
import doctest
import itertools
import re
import unittest

import zope.component.testing
from zope.configuration import xmlconfig

from zope.testing import renormalizing

import z3c.macro.tales
import z3c.macro.zcml


def setUp(test):
    zope.component.testing.setUp(test)
    # root = setup.placefulSetUp(site=True)
    # test.globs['root'] = root


def setUpZPT(test):
    setUp(test)
    from zope.browserpage import metaconfigure
    metaconfigure.registerType('macro', z3c.macro.tales.MacroExpression)


def setUpZ3CPT(suite):
    setUp(suite)
    import z3c.pt
    import z3c.ptcompat
    xmlconfig.XMLConfig('configure.zcml', z3c.pt)()
    xmlconfig.XMLConfig('configure.zcml', z3c.ptcompat)()


def tearDown(test):
    zope.component.testing.tearDown(test)


checker = renormalizing.RENormalizing([
    (re.compile("u('.*?')"), r"\1"),
    (re.compile('u(".*?")'), r"\1"),
    # Python 3 adds module name to exceptions;
    # The output of this one is too complex for
    # IGNORE_EXCEPTION_MODULE_IN_PYTHON2
    (re.compile('zope.configuration.xmlconfig.ZopeXMLConfigurationError'),
     'ZopeXMLConfigurationError'),
])


def test_suite():
    tests = ((
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp, tearDown=tearDown,
            checker=checker,
            optionflags=(doctest.NORMALIZE_WHITESPACE
                         | doctest.ELLIPSIS
                         | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2),
        ),
        doctest.DocFileSuite(
            'zcml.rst',
            setUp=setUp, tearDown=tearDown,
            checker=checker,
            optionflags=(doctest.NORMALIZE_WHITESPACE
                         | doctest.ELLIPSIS
                         | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2),
        )
    ) for setUp in (setUpZ3CPT, setUpZPT))

    return unittest.TestSuite(itertools.chain(*tests))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
