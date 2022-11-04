.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.regenv.svg?branch=master
    :target: https://travis-ci.org/collective/collective.regenv

.. image:: https://coveralls.io/repos/github/collective/collective.regenv/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.regenv?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.regenv.svg
    :target: https://pypi.python.org/pypi/collective.regenv/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.regenv.svg
    :target: https://pypi.python.org/pypi/collective.regenv
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.regenv.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.regenv.svg
    :target: https://pypi.python.org/pypi/collective.regenv/
    :alt: License


===================
collective.regenv
===================

Tell me what your product does

Features
--------

- Can be bullet points


Documentation
-------------

Registry overrides should be in a YAML file::

    % cat sample.yaml

    defaults: &defaults
        plone.cachepurging.interfaces.ICachePurgingSettings.cachingProxies:
            - http://localhost:8000
            - http://localhost:8001
        plone.app.theming.interfaces.IThemeSettings.hostnameBlacklist:
            - 127.0.0.1
            - localhost

    /Plone/portal_registry:
        <<: *defaults

    /Plone2/portal_registry:
        <<: *defaults
        plone.cachepurging.interfaces.ICachePurgingSettings.cachingProxies:
            - http://localhost:9000

Run zope instance with environment pointing to the YAML file, for example::

    PLONE_REGISTRY_YAML=$(pwd)/sample.yaml bin/instance fg


Installation
------------

Install collective.regenv by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.regenv


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.regenv/issues
- Source Code: https://github.com/collective/collective.regenv
- Documentation: https://docs.plone.org/foo/bar


License
-------

The project is licensed under the GPLv2.
