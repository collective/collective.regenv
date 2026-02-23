"""Init and utils."""

import logging


__version__ = "2.0.0a0"

PACKAGE_NAME = "collective.regenv"

logger = logging.getLogger(PACKAGE_NAME)


def main():
    """Initialize monkey patches."""
    from collective.regenv.monkey import initialize

    initialize()


main()
