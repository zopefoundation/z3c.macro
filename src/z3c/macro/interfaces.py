##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
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
Interfaces for z3c.macro.
"""

from zope.tales import interfaces
from zope.pagetemplate.interfaces import IPageTemplate


class IMacroTemplate(IPageTemplate):
    """A macro template."""


class IMacroExpression(interfaces.ITALESExpression):
    """Return the HTML content of the named provider.

    To call a macro from a page template use the the following syntax::

      <metal:block use-macro="macro:macroname">
        <metal:block fill-slot="slotname">
          this content get rendered in the defined slot of the macro
        </metal:block>
      </metal:block>

      or

      <metal:block use-macro="macro:macroname">
        this content get replaced by the defined macro
      </metal:block>

    The ``macro:`` TALES expression calles a named adapter adapting
    (context, request) or (context, request, view), depending on the usage
    of the view attribute in the macro directive. A macro provides the
    interface IMacroTemplate.
    """
