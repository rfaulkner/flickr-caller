#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Author:             Ryan Faulkner
    Date:               August 23rd, 2013
    Email:              bobs.ur.uncle@gmail.com

Flickr API call wrapper.

"""

from flickr_caller import config

import urllib2
import flickrapi
import argparse
import logging
import sys

# Logging INIT
# ============

# NullHandler was added in Python 3.1.
try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Add a do-nothing NullHandler to the module logger to prevent "No handlers
# could be found" errors. The calling code can still add other, more useful
# handlers, or otherwise configure logging.
log = logging.getLogger(__name__)
#null_logger = NullHandler()
#log.addHandler(null_logger)


class PythonFlickrAPIError(Exception):
    """ Basic exception class for UserMetric types """
    def __init__(self, message="Git deploy error.", exit_code=1):
        Exception.__init__(self, message)
        self._exit_code = int(exit_code)

    @property
    def exit_code(self):
        return self._exit_code


def parseargs():
    """Parse command line arguments.

    Returns *args*, the list of arguments left over after processing.

    """
    parser = argparse.ArgumentParser(
        description="This script performs ",
        epilog="",
        conflict_handler="resolve",
        usage="sartoris [-q --quiet] [-s --silent] [-v --verbose] [method]"
    )

    parser.allow_interspersed_args = False

    defaults = {
        "quiet": 0,
        "silent": False,
        "verbose": 0,
    }

    # Global options.
    parser.add_argument("method")
    parser.add_argument("-q", "--quiet",
                        default=defaults["quiet"], action="count",
                        help="decrease the logging verbosity")
    parser.add_argument("-s", "--silent",
                        default=defaults["silent"], action="store_true",
                        help="silence the logger")
    parser.add_argument("-v", "--verbose",
                        default=defaults["verbose"], action="count",
                        help="increase the logging verbosity")

    args = parser.parse_args()
    return args


def set_logger(args, out=None, err=None):
    """
    Configures the script level logger
    """

    if out is None:  # pragma: nocover
        out = sys.stdout
    if err is None:  # pragma: nocover
        err = sys.stderr
    args = parseargs()
    level = logging.WARNING - ((args.verbose - args.quiet) * 10)
    if args.silent:
        level = logging.CRITICAL + 1

    log_format = "%(asctime)s %(levelname)-8s %(message)s"
    handler = logging.StreamHandler(err)
    handler.setFormatter(logging.Formatter(fmt=log_format,
                         datefmt='%b-%d %H:%M:%S'))

    # log.removeHandler(null_logger)
    log.addHandler(handler)
    log.setLevel(level)

    log.debug("Logger configured.")


def _call_api(args, params=None):
    """
    Invokes the API method
    """

    log.debug('API KEY = {0}, SECRET = {1}'.format(
        config.API_KEY,
        config.API_SECRET
    ))
    flickr = flickrapi.FlickrAPI(config.API_KEY, secret=config.API_SECRET)

    try:
        # Extract the api method
        log.debug('Calling method - ' + args.method)
        method = getattr(flickr, args.method)
    except Exception:
        log.error('No such API method.')
        return

    try:
        if params:
            return method(format='json')
        else:
            return method(params)
    except urllib2.HTTPError as e:
        log.error('Could not reach service.')
    except Exception as e:
        log.error(e.message())
        return None


def main():
    args = parseargs()
    set_logger(args)
    _call_api(args)

def cli():
    exit(main())

if __name__ == '__main__':
    cli()