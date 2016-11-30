#!/usr/bin/env python
import io
import sys
from setuptools import find_packages, setup
import adaptest


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name="adaptest",
    version=adaptest.__version__,
    author="Eduard Kracmar",
    author_email="eduard@adaptiware.com",
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url="https://github.com/Edke/adaptest",
    description="Adaptest - a lightweight YAML wrapper for httest",
    long_description=read('README.md', ),
    # long_description=read('README.md', 'CHANGES.rst'),
    entry_points={
        'console_scripts': [
            'adaptest = adaptest.__main__:main',
        ]
    },
    zip_safe=False,
    install_requires=[
        'Jinja2>=2.8',
        'PyYAML>=3.12'
    ],
)
