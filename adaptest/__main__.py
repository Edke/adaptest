# coding: utf-8
import os
import argparse
import subprocess
import tempfile
from .tools import render, get_context, process_httest_output


def main():
    parser = argparse.ArgumentParser(
        prog='adaptest',
        description=u'Adaptest, lightweight httest yaml wrapper',
    )

    parser.add_argument('--uri-prefix', type=str, help=u'Uri prefix that will be applied to all tests, e.g. /en/')
    parser.add_argument('--verbose', '-v', action='store_true', help=u'More verbose output')
    parser.add_argument('url', type=str, help=u'URL all tests will be tested to, e.g. https://google.com')
    parser.add_argument('file', type=str, nargs="+", help=u'YAML config file(s) for Adaptest')

    args = parser.parse_args()

    for _file in args.file:
        if not os.path.exists(_file):
            print(u'file {} does not exists'.format(_file))
            exit(1)

        fd = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        print(u"Building htt file {} for {} ... ".format(fd.name, _file), end='')
        ctx = get_context(_file, args.url)
        htt_file = render(context=ctx)
        fd.write(htt_file)
        fd.close()
        print(u"done")
        if args.verbose:
            print(htt_file)

        print(u"Running httest ... ", end='')
        p = subprocess.Popen(['httest', fd.name], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, err = p.communicate()
        if p.returncode != 0:
            process_httest_output(output.decode('utf-8'), err.decode('utf-8'))
            exit(1)

        process_httest_output(output.decode('utf-8'))

        os.unlink(fd.name)

    print(u"ALL DONE, woila")

if __name__ == '__main__':
    main()
