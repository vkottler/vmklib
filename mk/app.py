
"""
mk - This package's command-line entry-point application.
"""

# built-in
import argparse
import logging

LOG = logging.getLogger(__name__)


def entry(args: argparse.Namespace) -> int:
    """ TODO """

    LOG.info(args)
    return 0


def add_app_args(_: argparse.ArgumentParser) -> None:
    """ Add application-specific arguments to the command-line parser. """
