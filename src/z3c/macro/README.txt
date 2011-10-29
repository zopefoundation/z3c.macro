=====
Macro
=====

This package provides a adapter and a TALES expression for a expliciter and
flexibler macro handling using the adapter registry for macros.

We start with creating a content object that is used as a view context later:

  >>> import zope.interface
  >>> import zope.component
  >>> from zope.publisher.interfaces.browser import IBrowserView
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> class Content(object):
  ...     zope.interface.implements(zope.interface.Interface)

  >>> content = Content()

We also create a temp dir for sample templates which we define later for
testing:

  >>> import os, tempfile
  >>> temp_dir = tempfile.mkdtemp()


Macro Template
--------------

We define a macro template as a adapter providing IMacroTemplate:

  >>> path = os.path.join(temp_dir, 'navigation.pt')
  >>> open(path, 'w').write('''
  ... <metal:block define-macro="navigation">
  ...   <div tal:content="title">---</div>
  ... </metal:block>
  ... ''')

Let's define the macro factory

  >>> from z3c.macro import interfaces
  >>> from z3c.macro import zcml
  >>> navigationMacro = zcml.MacroFactory(path, 'navigation', 'text/html')

and register them as adapter:

  >>> zope.component.provideAdapter(
  ...     navigationMacro,
  ...     (zope.interface.Interface, IBrowserView, IDefaultBrowserLayer),
  ...     interfaces.IMacroTemplate,
  ...     name='navigation')


The TALES ``macro`` Expression
------------------------------

The ``macro`` expression will look up the name of the macro, call a adapter
providing IMacroTemplate and uses them or fills a slot if defined in the
``macro`` expression.

Let's create a page template using the ``navigation`` macros:

  >>> path = os.path.join(temp_dir, 'first.pt')
  >>> open(path, 'w').write('''
  ... <html>
  ...   <body>
  ...     <h1>First Page</h1>
  ...     <div class="navi">
  ...       <tal:block define="title string:My Navigation">
  ...         <metal:block use-macro="macro:navigation" />
  ...       </tal:block>
  ...     </div>
  ...     <div class="content">
  ...       Content here
  ...     </div>
  ...   </body>
  ... </html>
  ... ''')

As you can see, we used the ``macro`` expression to simply look up a macro
called navigation whihc get inserted and replaces the HTML content at this
place.

Let's now create a view using this page template:

  >>> from zope.publisher.browser import BrowserView
  >>> class simple(BrowserView):
  ...     def __getitem__(self, name):
  ...         return self.index.macros[name]
  ...
  ...     def __call__(self, **kwargs):
  ...         return self.index(**kwargs)

  >>> from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile  
  >>> def SimpleViewClass(path, name=u''):
  ...     return type(
  ...         "SimpleViewClass", (simple,),
  ...         {'index': ViewPageTemplateFile(path), '__name__': name})
  
  >>> FirstPage = SimpleViewClass(path, name='first.html')

  >>> zope.component.provideAdapter(
  ...     FirstPage,
  ...     (zope.interface.Interface, IDefaultBrowserLayer),
  ...     zope.interface.Interface,
  ...     name='first.html')

Finally we look up the view and render it:

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> view = zope.component.getMultiAdapter((content, request),
  ...                                       name='first.html')
  >>> print view().strip()
  <html>
    <body>
      <h1>First Page</h1>
      <div class="navi">
        <div>My Navigation</div>
      </div>
      <div class="content">
        Content here
      </div>
    </body>
  </html>


Slot
----

We can also define a macro slot and fill it with given content:

  >>> path = os.path.join(temp_dir, 'addons.pt')
  >>> open(path, 'w').write('''
  ... <metal:block define-macro="addons">
  ...   Content before header
  ...   <metal:block define-slot="header">
  ...     <div>My Header</div>
  ...   </metal:block>
  ...   Content after header
  ... </metal:block>
  ... ''')

Let's define the macro factory

  >>> addonsMacro = zcml.MacroFactory(path, 'addons', 'text/html')

and register them as adapter:

  >>> zope.component.provideAdapter(
  ...     addonsMacro,
  ...     (zope.interface.Interface, IBrowserView, IDefaultBrowserLayer),
  ...     interfaces.IMacroTemplate,
  ...     name='addons')

Let's create a page template using the ``addons`` macros:

  >>> path = os.path.join(temp_dir, 'second.pt')
  >>> open(path, 'w').write('''
  ... <html>
  ...   <body>
  ...     <h1>Second Page</h1>
  ...     <div class="header">
  ...       <metal:block use-macro="macro:addons">
  ...         This line get ignored
  ...         <metal:block fill-slot="header">
  ...           Header comes from here
  ...         </metal:block>
  ...         This line get ignored
  ...       </metal:block>
  ...     </div>
  ...   </body>
  ... </html>
  ... ''')

Let's now create a view using this page template:

  >>> SecondPage = SimpleViewClass(path, name='second.html')

  >>> zope.component.provideAdapter(
  ...     SecondPage,
  ...     (zope.interface.Interface, IDefaultBrowserLayer),
  ...     zope.interface.Interface,
  ...     name='second.html')

Finally we look up the view and render it:

  >>> view = zope.component.getMultiAdapter((content, request),
  ...                                       name='second.html')
  >>> print view().strip()
  <html>
    <body>
      <h1>Second Page</h1>
      <div class="header">
  <BLANKLINE>
    Content before header
  <BLANKLINE>
            Header comes from here
  <BLANKLINE>
    Content after header
      </div>
    </body>
  </html>


Cleanup
-------

  >>> import shutil
  >>> shutil.rmtree(temp_dir)

