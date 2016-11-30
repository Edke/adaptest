# coding: utf-8
import os
from adaptest.tools import render, get_context


def get_result(filename):
    fn = os.path.join(os.path.dirname(__file__), filename)
    return open(fn).read()


def get_rendered(filename, url):
    ctx = get_context(os.path.join(os.path.dirname(__file__), filename),
                      url=url)
    return render(context=ctx)


def test_render1():
    assert get_rendered('render1.yml', 'http://google.com') == get_result('render1.txt')
    assert get_rendered('render2.yml', 'https://google.com') == get_result('render2.txt')
