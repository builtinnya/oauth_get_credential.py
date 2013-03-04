# -*- coding: utf-8 -*-
"""
Gets a token credential for OAuth 1.0/a from servers.

This script gets an OAuth 1.0/a credential from servers.
Use this script to test your code using OAuth 1.0/a authentication.

Requirements:
  - rauth [https://github.com/litl/rauth]

  NOTE:
    `pip install requests==0.14.2` before `pip install rauth`
    will make you happier.

For usage, type:
  python oauth_get_credential.py -h

Author:
   Naoto Yokoyama <builtinnya@gmail.com>
"""

import sys
import argparse
import urlparse
import urllib
import webbrowser
from rauth.service import OAuth1Service

import logging
logger = logging.getLogger('oauth_get_credential')

def _input(prompt):
    """Input non-empty string from user."""

    s = raw_input(prompt).strip()
    while not s:
        print 'Something not empty is required'
        s = raw_input(prompt).strip()

    return s

def fill_args(args):
    """Show prompts to user to fill the required arguments."""

    import readline

    if not args.request_token_url:
        args.request_token_url = _input('Temporary credential endpoint: ')

    if not args.authorize_url:
        args.authorize_url = _input('Authorize endpoint: ')

    if not args.access_token_url:
        args.access_token_url = _input('Token credential endpoint: ')

    if not args.consumer_key:
        args.consumer_key = _input('Client credential key: ')

    if not args.consumer_secret:
        args.consumer_secret = _input('Client credential secret: ')

def load_config(args):
    """Load a configuration file and override specified arguments."""

    if not args.config_file:
        return

    import csv

    with open(args.config_file, 'rb') as f:
        reader = csv.reader(f, delimiter='=')
        for row in reader:
            if len(row) > 1:
                arg_name = row[0].lower()
                arg_value = row[1]
                setattr(args, arg_name, arg_value)

def yes(text):
    """True only if the given text expresses affirmative."""

    import re

    return re.match('yes|true|ok', text, re.IGNORECASE)

def config_logger(args):
    """Configure the logger."""

    handler = logging.StreamHandler()

    if args.verbose and yes(args.verbose):
        logger.setLevel('DEBUG')
        handler.setLevel('DEBUG')

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main(args):
    """Application entry point."""

    # Load the configuration file if specified
    load_config(args)

    config_logger(args)

    # Fill unspecified required arguments interactively
    fill_args(args)

    service = OAuth1Service(
        request_token_url=args.request_token_url,
        authorize_url=args.authorize_url,
        access_token_url=args.access_token_url,
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret
    )

    params = {}
    if args.params:
        params.update(urlparse.parse_qs(args.params))

    logger.debug('Attempting to request a temporal credential...')
    temporal_credential = service.get_request_token(method='GET', params=params)

    request_token, request_token_secret = temporal_credential
    logger.debug('request_token="{}", request_token_secret="{}"'.format(
        request_token, request_token_secret
    ))

    authorize_url = urllib.unquote(service.get_authorize_url(request_token))
    logger.debug('authorize_url="{}"'.format(authorize_url))

    webbrowser.open(authorize_url)
    verifier = _input("Enter code from your browser: ")

    logger.debug('Attempting to request a token credential...')
    response = service.get_access_token(
        method='GET',
        request_token=request_token,
        request_token_secret=request_token_secret,
        params={'oauth_verifier': verifier}
    )

    data = response.content
    access_token = data['oauth_token']
    access_token_secret = data['oauth_token_secret']

    print 'oauth_token={}'.format(access_token)
    print 'oauth_token_secret={}'.format(access_token_secret)

if __name__ == '__main__':

    description = (
        'This script gets an OAuth 1.0/a credential from servers. '
        'Requires `rauth` package [https://github.com/litl/rauth].'
    )

    epilog = ('Authored by Naoto Yokoyama <builtinnya@gmail.com>')

    parser = argparse.ArgumentParser(
        prog='python oauth_get_credential.py',
        usage='%(prog)s [options]',
        description=description,
        epilog=epilog
    )

    parser.add_argument(
        '-r', '--request-token-url',
        help='Temporary credential endpoint'
    )
    parser.add_argument(
        '-a', '--authorize-url',
        help='Authorize endpoint'
    )
    parser.add_argument(
        '-t', '--access-token-url',
        help='Token credential endpoint'
    )
    parser.add_argument(
        '-k', '--consumer-key',
        help='Client credential key'
    )
    parser.add_argument(
        '-s', '--consumer-secret',
        help='Client credential secret'
    )
    parser.add_argument(
        '-p', '--params',
        metavar='KEY1=VALUE1&KEY2=VALUE2...',
        help='Extra parameters to pass'
    )
    parser.add_argument(
        '-f', '--config-file',
        help=(
            'Configuration file for specifying arguments, '
            'which contains ARGUMENT_NAME="VALUE" in each line.'
        )
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    main(args)
