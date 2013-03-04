# oauth\_get\_credential.py

## What's This?

This small script gets a token credential for [OAuth 1.0/a] from servers.

Use this script to test your code using OAuth 1.0/a authentication.

[OAuth 1.0/a]: http://tools.ietf.org/html/rfc5849

## Installation and Usage

oauth\_get\_credential.py requires [rauth].

Before installing rauth, installing the older version of 
[Requests] may make you happier:

    pip install requests==0.14.2

Then, you simply clone this repository and run:

    python oauth_get_credential.py
    
or run with `-h` for full details of options.

[rauth]: https://github.com/litl/rauth
[Requests]: https://github.com/kennethreitz/requests

## Copyright and License

Copyright (c) 2013 Naoto Yokoyama

Distributed under the MIT license.
See the LICENSE file for full details.
