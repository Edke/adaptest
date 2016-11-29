Adaptest - a lightweight yaml wrapper for httest
================================================

# Overview

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

Therefore I wrote `Adaptest`, which is basically a `httest` YAML wrapper.
 
# Features
 
As `httest` is really powerful tool, not everything is currently supported. But
even in this alpha stage it supports:

- Sequence HTTP testing
- Cookies support
- CSRF support
- Any request headers
- Multiple `expect`'s, status, response header tests, body tests
- Capturing response headers or body using regex to variables and use in later testes
- POST (application/x-www-form-urlencoded)
- Auto referer from previous test 

# Installation

## From source

```bash
git clone 
cd adaptest
sudo python setup.py install
```

## From PyPI

```bash
pip install adaptest
```

# Testing

```bash
cd tests
pytest
```

# Status

Please consider this tool as early alpha, not ready for production. Testing is more than welcome.

# Contributing

For bugs, feature requests or code contributing please use [Github project page](xs).

