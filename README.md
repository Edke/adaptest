Adaptest - a lightweight YAML wrapper for httest
================================================

## Overview

There are many powerful tools for automated HTTP-based tests, and and even in Python:

- [httest](http://htt.sourceforge.net/), HTTP Test tool
- [pyresttest](https://github.com/svanoort/pyresttest), Python REST Test tool
- [gabbi](https://github.com/cdent/gabbi), Declarative HTTP Testing tool

But key features for me were:

- powerful
- easily maintenable config, ideally using YAML or something similar
- Cookies support
- CSRF support

Some of them were HTTP REST and JSON specific. `httest` was best option but not
very confortable .htt files especially for Testers with little knowledge of HTTP
protocol and programming.

Therefore I wrote `Adaptest` which is basically a `httest` YAML wrapper.
 
## Features
 
As `httest` is really powerful tool, `Adaptest` does not support everything at this stage. But
even while in alpha stage it supports:

- Sequence HTTP testing
- Cookies support
- CSRF support
- Any request headers
- Multiple `expect`'s, status, response header tests, body tests
- Capturing response headers or body using regex to variables and use in later testes
- POST (application/x-www-form-urlencoded)
- Auto referer from previous test 

## Examples

`Adaptest` turns yaml config of test:

```yml
---

config:
 auto_cookie: on

tests:
  - name: user profile without auth
    url: /en/account/
    method: get
    headers:
      - Connection: keep-alive
    expect:
      - scope: .
        value: "302 Found"
      - scope: headers
        value: "Location: /en/account/log-in/"

  - name: login page to get cookie
    url: /en/account/log-in/
    method: get
    expect:
      - scope: .
        value: 200 OK
    match:
      - scope: headers
        pattern: "csrftoken=([^;]+)"
        variable: csrf

  - name: login page
    url: /en/account/log-in/
    method: post
    referer: auto
    headers:
      - Content-Type: application/x-www-form-urlencoded
    data:
      - csrfmiddlewaretoken: $csrf
      - username: eduard@adaptiware.com
      - password: Mys3cr3tp455
    expect:
      - scope: .
        value: "302 Found"

  - name: user profile after auth
    url: /en/account/
    method: get
    headers:
      - Connection: keep-alive
    expect:
      - scope: .
        value: 200 OK
```

into this:

```
CLIENT
_AUTO_COOKIE on

_REQ example.com SSL:443
_DEBUG user profile without auth
__GET /en/account/ HTTP/1.1
__Host: example.com
__Cookie: AUTO
__Connection: keep-alive
__
_EXPECT . "302 Found"
_EXPECT headers "Location: /en/account/log-in/"
_WAIT
_CLOSE

_REQ example.com SSL:443
_DEBUG login page to get cookie
__GET /en/account/log-in/ HTTP/1.1
__Host: example.com
__Cookie: AUTO
__
_EXPECT . "200 OK"
_MATCH headers "csrftoken=([^;]+)" csrf
_WAIT
_CLOSE

_REQ example.com SSL:443
_DEBUG login page
__POST /en/account/log-in/ HTTP/1.1
__Host: example.com
__Cookie: AUTO
__Content-Length: AUTO
__Content-Type: application/x-www-form-urlencoded
__Referer: https://example.com/en/account/log-in/
__
__csrfmiddlewaretoken=$csrf&username=eduard@adaptiware.com&password=Mys3cr3tp455&
_EXPECT . "302 Found"
_WAIT
_CLOSE

_REQ example.com SSL:443
_DEBUG user profile after auth
__GET /en/account/ HTTP/1.1
__Host: example.com
__Cookie: AUTO
__Connection: keep-alive
__
_EXPECT . "200 OK"
_WAIT
_CLOSE

END

```

## Installation

### From source

```bash
git clone git@github.com:Edke/adaptest.git
cd adaptest
sudo python setup.py install
```

### From PyPI

```bash
pip install adaptest
```

## Testing

```bash
cd tests
pytest
```

## Status

Please consider this tool as early alpha, not ready for production. Testing is more than welcome.

## Contributing

For bugs, feature requests or code contributing please use [Github project page](https://github.com/Edke/adaptest).
