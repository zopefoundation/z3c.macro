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
"""ZCML Meta-Directives
"""
import os

import zope.interface
import zope.schema
import zope.configuration.fields
from zope.configuration.exceptions import ConfigurationError
from zope.component import zcml
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.macro import interfaces


class IMacroDirective(zope.interface.Interface):
    """Parameters for the template directive."""

    template = zope.configuration.fields.Path(
        title=u'Template defining a named macro.',
        description=u"""Refers to a file containing a page template
            (should end in extension ``.pt`` or ``.html``).
            """,
        required=True,
        )

    name = zope.schema.TextLine(
        title=u'Name',
        description=u"""
            The macro name which this macro is registered for. The macro
            name can be the same defined in metal:define-macro but does
            not have to be the same. If no macro attribute is given the
            name is used as the name defined in metal:define-macro. If you
            need to register a macro under a different name as the defined
            one, you can use the macro attribute which have to reference
            the metal.define-macro name. The TALES expression calls macros
            by this name and returns the macro within the same name or with
            the name defined in the macro attribute.
            """,
        required=True,
        default=u'',
        )

    macro = zope.schema.TextLine(
        title=u'Macro',
        description=u"""
            The name of the macro to be used. This allows us to reference
            the named  macro defined with metal:define-macro if we use a
            different IMacroDirective name.
            """,
        required=False,
        default=u'',
        )

    for_ = zope.configuration.fields.GlobalObject(
        title=u'Context',
        description=u'The context for which the macro should be used',
        required=False,
        default=zope.interface.Interface,
        )

    view = zope.configuration.fields.GlobalObject(
        title=u'View',
        description=u'The view for which the macro should be used',
        required=False,
        default=IBrowserView)

    layer = zope.configuration.fields.GlobalObject(
        title=u'Layer',
        description=u'The layer for which the macro should be used',
        required=False,
        default=IDefaultBrowserLayer,
        )

    contentType = zope.schema.ASCIILine(
        title=u'Content Type',
        description=u'The content type identifies the type of data.',
        default='text/html',
        required=False,
        )


class MacroFactory(object):
    """Macro factory."""

    def __init__(self, path, macro, contentType):
        self.path = path
        self.macro = macro
        self.contentType = contentType

    def __call__(self, context, view, request):
        template = ViewPageTemplateFile(self.path,
                                        content_type=self.contentType)
        return template.macros[self.macro]


def registerMacroFactory(_context, path, name, macro, for_, view, layer,
                         contentType):
    """Register a named macro factory adapter."""

    factory = MacroFactory(path, macro, contentType)

    # register the macro
    zcml.adapter(_context, (factory,), interfaces.IMacroTemplate,
                 (for_, view, layer), name=name)


def macroDirective(_context, template, name, macro=u'',
                   for_=zope.interface.Interface, view=IBrowserView,
                   layer=IDefaultBrowserLayer, contentType='text/html'):

    # Make sure that the template exists
    path = os.path.abspath(str(_context.path(template)))
    if not os.path.isfile(path):
        raise ConfigurationError("No such file", template)

    if not macro:
        macro = name

    registerMacroFactory(_context, path, name, macro, for_, view, layer,
                         contentType)
