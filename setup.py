#!/usr/bin/env python
# vim:set fileencoding=utf8 ts=4 sw=4 et:

import io
import os
import re

name = 'characterentities'
_github_path = 'romain-dartigues/python-' + name

try:
    from setuptools import setup
except ImportError:
    import warnings
    from distutils.core import setup
    warnings.warn('unable to import setuptools, all options will not be available')

PWD = os.path.dirname(os.path.abspath(__file__))


with io.open(os.path.join(PWD, name, '__init__.py'), 'rt', encoding='utf8') as fobj:
    version = re.search(
        r'''^__version__\s*=\s*(?P<q>["'])(.*)(?P=q)''',
        fobj.read(),
        re.M,
    ).group(2)

with io.open('README.rst', 'rt', encoding='utf8') as fobj:
    README = fobj.read()


setup(
    name=name,
    version=version,
    description='HTML Entities for Python',
    long_description=README,
    author='Romain Dartigues',
    author_email='romain.dartigues@gmail.com',
    license='BSD 3-Clause License',
    keywords=[
        'SGML', 'HTML',
        'charater-entity', 'entities',
        'encode', 'decode',
        'escape', 'unescape',
    ],
    url='https://github.com/{}'.format(_github_path),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: SGML',
        'Topic :: Text Processing :: Markup :: XML',
    ],
    packages=[name],
    extras_require={
        'dev': (
            'pytest>=3',
            'coverage',
        ),
    },
)
