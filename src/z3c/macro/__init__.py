##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""
z3c.macro package.

Importing this package has the side-effect of registering the 'macro'
expression type in Chameleon (if z3c.pt is installed)
"""

try:
    # register chameleon ``macro`` tales expression for BaseTemplate
    # there is not adapter or other registration support built in in
    # z3c.pt and apply our tales expression to any page template or
    # offer a custom PageTemplate is no option
    from z3c.macro import tales
    import z3c.pt.pagetemplate
    z3c.pt.pagetemplate.BaseTemplate.expression_types[
        'macro'] = tales.MacroExpr
except ImportError:  # pragma: no cover
    # we do not support z3c.pt
    pass
