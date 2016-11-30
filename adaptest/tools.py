# coding: utf-8
import re
import os
import yaml
from jinja2 import Environment, FileSystemLoader
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse


def render(context):
    fn = os.path.join(os.path.dirname(__file__), 'templates')

    loader = FileSystemLoader(searchpath=fn)
    env = Environment(loader=loader)
    env.trim_blocks = True
    env.lstrip_blocks = True

    t = env.get_template('sequence.htt')
    return t.render(context)


def get_context(path, url, defaults=None):
    # context from yaml
    ctx = yaml.load(open(path, 'r').read())

    # split url
    u = urlparse.urlparse(url)
    host_with_port = u.netloc.split(':')
    if host_with_port.__len__() == 2:
        host = host_with_port[0]
        port = host_with_port[1]
    else:
        host = u.netloc
        port = '443' if u.scheme == 'https' else '80'

    ssl = u.scheme == 'https'

    ctx['request'] = u'{} {}{}'.format(
        host,
        'SSL:' if ssl else '',
        port
    )
    ctx['host_with_port'] = u'{}:{}'.format(host, port)
    ctx['ssl'] = ssl
    ctx['host'] = host
    ctx['port'] = port

    # default config
    if defaults is None:
        defaults_fn = os.path.join(os.path.dirname(__file__), 'defaults.yml')
        defaults = yaml.load(open(defaults_fn, 'r').read())

    if 'config' in ctx:
        # config = {**defaults, **ctx['config']}
        defaults.update(ctx['config'])
        config = defaults

    else:
        config = defaults

    # tests
    if 'tests' not in ctx:
        print(u'No tests in yaml, nothing to do')
        exit(1)

    # tests data tweaks
    for test in ctx['tests']:
        if 'headers' in test:
            test['headers_tuple'] = [(x.popitem()) for x in test['headers']]
            test['headers'] = [{x[0].lower().replace('-', '_'): x[1]} for x in test['headers_tuple']]

    # iteration tweaks
    uri = None
    for test in ctx['tests']:
        if 'referer' in test and test['referer'].lower() == 'auto':
            if 'headers_tuple' not in test:
                test['headers_tuple'] = []
            if 'headers' not in test:
                test['headers'] = []

            test['headers_tuple'].append(('Referer', '{}{}'.format(url, uri)))
            test['headers'].append({'referer': uri})

        if 'headers_tuple' in test and \
           'application/x-www-form-urlencoded' in [x[1] for x in test['headers_tuple'] if x[0] == 'Content-Type']:
            test['post'] = True

        if 'data' in test:
            data = [(x.popitem()) for x in test['data']]
            test['data'] = '&'.join([u'{}={}'.format(k, v) for k, v in data]) + '&'

        uri = test['url']

    ctx['config'] = config
    return ctx


def process_httest_output(output, err=None):
    chunks = []
    last = None
    buff = []
    caption = None
    for line in output.splitlines(False):
        _type = None
        if re.match(r'^<', line):
            _type = 'response'
        elif re.match(r'^>', line):
            _type = 'request'
        elif re.match(r'^_', line):
            _type = 'definition'

        # caption
        match = re.match(r'^_DEBUG (.*)', line)
        if match and _type == 'definition':
            caption = match.group(1)

        if last != _type and last is not None:
            chunks.append({
                'type': last,
                'buffer': buff,
                'lines': len(buff),
                'caption': caption if _type == 'definition' else None
            })
            buff = []
            last = _type

        last = _type
        buff.append(line)

        # print(line)
    chunks.append({
        'type': _type,
        'buffer': buff,
        'lines': len(buff),
        'caption': caption if _type == 'definition' else None
    })

    for chunk in chunks:
        if chunk['type'] == 'response':
            print("\n".join(chunk['buffer'][:20]))
        else:
            print("\n".join(chunk['buffer']))

    if err:
        print(err)


