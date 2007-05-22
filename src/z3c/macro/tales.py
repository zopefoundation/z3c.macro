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
"""Provider tales expression registrations

$Id$
"""
__docformat__ = 'restructuredtext'
import zope.component
import zope.interface
from zope.tales import expressions

from z3c.macro import interfaces


class MacroExpression(expressions.StringExpr):
    """Collect named IMacroTemplate via a TAL namespace called ``macro``."""

    zope.interface.implements(interfaces.IMacroExpression)

    def __call__(self, econtext):
        name = super(MacroExpression, self).__call__(econtext)
        context = econtext.vars['context']
        request = econtext.vars['request']
        view = econtext.vars['view']

        return zope.component.getMultiAdapter((context, view, request),
            interface=interfaces.IMacroTemplate, name=name)
