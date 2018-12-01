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

"""
import zope.component
import zope.interface
from zope.tales import expressions

from z3c.macro import interfaces


def get_macro_template(context, view, request, name):
    return zope.component.getMultiAdapter(
        (context, view, request),
        interface=interfaces.IMacroTemplate,
        name=name)


@zope.interface.implementer(interfaces.IMacroExpression)
class MacroExpression(expressions.StringExpr):
    """Collect named IMacroTemplate via a TAL namespace called ``macro``."""

    def __call__(self, econtext):
        name = super(MacroExpression, self).__call__(econtext)
        context = econtext.vars['context']
        request = econtext.vars['request']
        view = econtext.vars['view']
        return get_macro_template(context, view, request, name)


try:
    # define chameleon  ``macro`` expression

    from chameleon.tales import StringExpr
    from chameleon.astutil import Static
    from chameleon.astutil import Symbol
    from chameleon.codegen import template

    class MacroGetter(object):
        """Collect named IMacroTemplate via TAL namespace called ``macro``."""

        def __call__(self, context, request, view, name):
            return zope.component.getMultiAdapter(
                (context, view, request), interface=interfaces.IMacroTemplate,
                name=name)

    class MacroExpr(StringExpr):
        traverser = Static(
            template("cls()", cls=Symbol(MacroGetter), mode="eval")
        )

        def __call__(self, target, engine):
            assignment = super(MacroExpr, self).__call__(target, engine)

            return assignment + template(
                "target = traverse(context, request, view, target.strip())",
                target=target,
                traverse=self.traverser,
            )

except ImportError:  # pragma: no cover
    pass
