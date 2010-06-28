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
"""Provider tales expression registrations

$Id$
"""
__docformat__ = 'restructuredtext'

import re

import zope.component
import zope.interface
from zope.tales import expressions

from z3c.macro import interfaces

def get_macro_template(context, view, request, name):
    return zope.component.getMultiAdapter(
        (context, view, request), interface=interfaces.IMacroTemplate, name=name)

class MacroExpression(expressions.StringExpr):
    """Collect named IMacroTemplate via a TAL namespace called ``macro``."""

    zope.interface.implements(interfaces.IMacroExpression)

    def __call__(self, econtext):
        name = super(MacroExpression, self).__call__(econtext)
        context = econtext.vars['context']
        request = econtext.vars['request']
        view = econtext.vars['view']
        return get_macro_template(context, view, request, name)
    
try:
    from chameleon.zpt.expressions import ExpressionTranslator
    from chameleon.core import types
        
    class Z3CPTMacroExpression(ExpressionTranslator):
        """Collect named IMacroTemplate via a TAL namespace called ``macro``."""

        macro_regex = re.compile(r'^[A-Za-z][A-Za-z0-9_-]*$')
        symbol = '_get_macro_template'
        
        def validate(self, string):
            if self.macro_regex.match(string) is None:
                raise SyntaxError("%s is not a valid macro name." % string)

        def translate(self, string, escape=None):
            value = types.value("%s(context, view, request, '%s')" % \
                                (self.symbol, string))
            value.symbol_mapping[self.symbol] = get_macro_template
            return value

    z3cpt_macro_expression = Z3CPTMacroExpression()
    
except ImportError:
    pass
