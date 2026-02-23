<div align="center">
    <h1 align="center">collective.regenv</h1>
</div>
<div align="center">
[![PyPI](https://img.shields.io/pypi/v/collective.regenv)](https://pypi.org/project/collective.regenv/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.regenv)](https://pypi.org/project/collective.regenv/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.regenv)](https://pypi.org/project/collective.regenv/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.regenv)](https://pypi.org/project/collective.regenv/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.regenv)](https://pypi.org/project/collective.regenv/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.regenv)](https://pypi.org/project/collective.regenv/)

[![CI](https://github.com/collective/collective.regenv/actions/workflows/main.yml/badge.svg)](https://github.com/collective/collective.regenv/actions/workflows/main.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.regenv)](https://github.com/collective/collective.regenv)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.regenv?style=social)](https://github.com/collective/collective.regenv)

</div>

Override Plone registry settings with environment variables.

## Features

Using this product you can:

1. have different values for development and production environments
   (think about the ``MailHost`` settings,
   connection parameters to external services,
   etc.)

2. have different values for different instances in the same buildout,
   allowing for example to toggle features on and off for A/B testing.

## Installation

Install collective.regenv with `pip`:

```shell
pip install collective.regenv
```

And to create the Plone site:

```shell
make create-site
```

## Usage

Registry overrides should be in a YAML file:

```yaml
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

/Plone/acl_users/oidc:
    issuer:
        http://localhost:1234/realms/plone/
    client_id:
        plone
```

Run zope instance with environment pointing to the YAML file, for example

```shell
PLONE_REGISTRY_YAML=$(pwd)/sample.yaml bin/instance fg
```

Or using the docker image, for example::

```shell
docker run -p 8080:8080 \
    -e ADDONS=collective.regenv \
    -e PLONE_REGISTRY_YAML=/app/registry.yaml \
    -v$(pwd)/sample.yaml:/app/registry.yaml \
    plone/plone-backend:latest
```

Alternatively you can add the contents of the YAML file in an environment variable called `PLONE_REGISTRY_YAML_CONTENT` and pass the values directly.
This way you do not need to mount a volume with the configuration file.

For example:

```shell
export PLONE_REGISTRY_YAML_CONTENT=$(cat sample.yaml)
docker run -p 8080:8080 \
    -e ADDONS=collective.regenv \
    -e PLONE_REGISTRY_YAML_CONTENT
    plone/plone-backend:latest
```


## Contribute

- [Issue tracker](https://github.com/collective/collective.regenv/issues)
- [Source code](https://github.com/collective/collective.regenv/)

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Installation 🔧

1.  Clone this repository, then change your working directory.

    ```shell
    git clone git@github.com:collective/collective.regenv.git
    cd collective.regenv
    ```

2.  Install this code base.

    ```shell
    make install
    ```


### Add features using `plonecli` or `bobtemplates.plone`

This package provides markers as strings (`<!-- extra stuff goes here -->`) that are compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
These markers act as hooks to add all kinds of subtemplates, including behaviors, control panels, upgrade steps, or other subtemplates from `plonecli`.

To run `plonecli` with configuration to target this package, run the following command.

```shell
make add <template_name>
```

For example, you can add a content type to your package with the following command.

```shell
make add content_type
```

You can add a behavior with the following command.

```shell
make add behavior
```

```{seealso}
You can check the list of available subtemplates in the [`bobtemplates.plone` `README.md` file](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates).
See also the documentation of [Mockup and Patternslib](https://6.docs.plone.org/classic-ui/mockup.html) for how to build the UI toolkit for Classic UI.
```

## License

The project is licensed under GPLv2.

## Credits and acknowledgements 🙏

Generated using [Cookieplone (0.9.10)](https://github.com/plone/cookieplone) and [cookieplone-templates (44f4a49)](https://github.com/plone/cookieplone-templates/commit/44f4a492fdf40acb385227b0564b7c62d22bd8d9) on 2026-02-20 17:38:38.334208. A special thanks to all contributors and supporters!
