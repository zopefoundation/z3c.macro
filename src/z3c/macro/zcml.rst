=================
 macro directive
=================

A macro directive can be used for register macros. Take a look at the
README.txt which explains the macro TALES expression.

  >>> import sys
  >>> from zope.configuration import xmlconfig
  >>> import z3c.template
  >>> context = xmlconfig.file('meta.zcml', z3c.macro)

First define a template which defines a macro:

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()
  >>> file_path = os.path.join(temp_dir, 'file.pt')
  >>> with open(file_path, 'w') as file:
  ...     _ = file.write('''
  ... <html>
  ...   <head>
  ...     <metal:block define-macro="title">
  ...        <title>Pagelet skin</title>
  ...     </metal:block>
  ...   </head>
  ...   <body>
  ...     <div>content</div>
  ...   </body>
  ... </html>
  ... ''')

and register the macro provider within the ``z3c:macroProvider`` directive:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:macro
  ...       template="%s"
  ...       name="title"
  ...       />
  ... </configure>
  ... """ % file_path, context=context)

We need a content object...

  >>> import zope.interface
  >>> @zope.interface.implementer(zope.interface.Interface)
  ... class Content(object):
  ...     pass
  >>> content = Content()

and we need a view...

  >>> import zope.interface
  >>> import zope.component
  >>> from zope.publisher.browser import BrowserPage
  >>> class View(BrowserPage):
  ...     def __init__(self, context, request):
  ...         self.context = context
  ...         self.request = request

and we need a request:
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

Check if we get the macro template:

  >>> from z3c.macro import interfaces
  >>> view = View(content, request)

  >>> macro = zope.component.queryMultiAdapter((content, view, request),
  ...     interface=interfaces.IMacroTemplate, name='title')

  >>> macro is not None
  True

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()
  >>> test_path = os.path.join(temp_dir, 'test.pt')
  >>> with open(test_path, 'w') as file:
  ...     _ = file.write('''
  ... <html>
  ...   <body>
  ...     <metal:macro use-macro="options/macro" />
  ...   </body>
  ... </html>
  ... ''')

  >>> from zope.browserpage.viewpagetemplatefile import BoundPageTemplate
  >>> from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
  >>> template = ViewPageTemplateFile(test_path)
  >>> print(BoundPageTemplate(template, view)(macro=macro))
  <html>
    <body>
      <title>Pagelet skin</title>
    </body>
  </html>

Error Conditions
================

If the file is not available, the directive fails:

  >>> context = xmlconfig.string("""
  ... <configure
  ...     xmlns:z3c="http://namespaces.zope.org/z3c">
  ...   <z3c:macro
  ...       template="this_file_does_not_exist"
  ...       name="title"
  ...       />
  ... </configure>
  ... """, context=context)
  Traceback (most recent call last):
  ...
  zope.configuration.exceptions.ConfigurationError: ...
