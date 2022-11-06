.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/collective.regenv.svg
    :target: https://pypi.org/project/collective.regenv/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/collective.regenv.svg?style=plastic
    :target: https://pypi.org/project/collective.regenv/
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/dm/collective.regenv.svg
    :target: https://pypi.org/project/collective.regenv/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/l/collective.regenv.svg
    :target: https://pypi.org/project/collective.regenv/
    :alt: License

.. image:: https://github.com/collective/collective.regenv/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/collective/collective.regenv/actions
    :alt: Tests

.. image:: https://coveralls.io/repos/github/collective/collective.regenv/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.regenv?branch=main
    :alt: Coverage


=================
collective.regenv
=================

This product allows to override the values stored in the portal registry
with values defined on a local file
defined in an environment variable called ``PLONE_REGISTRY_YAML``.


Features
--------

Using this product you can:

1. have different values for development and production environments
   (think about the ``MailHost`` settings,
   connection parameters to external services,
   etc.)

2. have different values for different instances in the same buildout,
   allowing for example to toggle features on and off for A/B testing.


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
- Documentation: https://pypi.org/project/collective.regenv/


License
-------

The project is licensed under the GPLv2.
