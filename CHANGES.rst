=======
CHANGES
=======

2.2.1 (unreleased)
------------------

- Fix list of supported Python versions in Trove classifiers.


2.2.0 (2018-11-13)
------------------

- Removed Python 3.5 support, added Python 3.7.

- Fixed up tests.

- Fix docstring that caused DeprecationWarning.


2.1.0 (2017-10-17)
------------------

- Drop support for Python 2.6 and 3.3.

- Add support for Python 3.4, 3.5 and 3.6.

- Add support for PyPy.


2.0.0 (2015-11-09)
------------------

- Standardize namespace ``__init__``.


2.0.0a1 (2013-02-25)
--------------------

- Added support for Python 3.3.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.4 and 2.5.


1.4.2 (2012-02-15)
------------------

- Remove hooks to use ViewPageTemplateFile from z3c.pt because this breaks when
  z3c.pt is available, but z3c.ptcompat is not included. As recommended by notes
  in 1.4.0 release.


1.4.1 (2011-11-15)
------------------

- bugfix, missing comma in setup install_requires list


1.4.0 (2011-10-29)
------------------

- Moved z3c.pt include to extras_require chameleon. This makes the package
  independent from chameleon and friends and allows to include this
  dependencies in your own project.

- Upgrade to chameleon 2.0 template engine and use the newest z3c.pt and
  z3c.ptcompat packages adjusted to work with chameleon 2.0.

  See the notes from the z3c.ptcompat package:

  Update z3c.ptcompat implementation to use component-based template engine
  configuration, plugging directly into the Zope Toolkit framework.

  The z3c.ptcompat package no longer provides template classes, or ZCML
  directives; you should import directly from the ZTK codebase.

  Note that the ``PREFER_Z3C_PT`` environment option has been
  rendered obsolete; instead, this is now managed via component
  configuration.

  Also note that the chameleon CHAMELEON_CACHE environment value changed from
  True/False to a path. Skip this property if you don't like to use a cache.
  None or False defined in buildout environment section doesn't work. At least
  with chameleon <= 2.5.4

  Attention: You need to include the configure.zcml file from z3c.ptcompat
  for enable the z3c.pt template engine. The configure.zcml will plugin the
  template engine. Also remove any custom built hooks which will import
  z3c.ptcompat in your tests or other places.


1.3.0 (2010-07-05)
------------------

- Tests now require ``zope.browserpage >= 3.12`` instead of
  ``zope.app.pagetemplate`` as the expression type registration has
  been moved there recently.

- No longer using deprecated ``zope.testing.doctestunit`` but built-in
  ``doctest`` instead.


1.2.1 (2009-03-07)
------------------

- Presence of ``z3c.pt`` is not sufficient to register macro-utility,
  ``chameleon.zpt`` is required otherwise the factory for the utility
  is not defined.


1.2.0 (2009-03-07)
------------------

- Allow use of ``z3c.pt`` using ``z3c.ptcompat`` compatibility layer.

- Change package's mailing list address to zope-dev at zope.org.


1.1.0 (2007-11-01)
------------------

- Update package info data.

- Add z3c namespace package declaration.


1.0.0 (2007-09-30)
------------------

- Initial release.
