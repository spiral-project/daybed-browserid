# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid >= 1.3',
    'PyBrowserID',
    'webtest'
]

setup(
    name='daybed-browserid',
    version='0.1.0.dev',
    description='Grab a daybed token from a browserid assertion',
    long_description=README + '\n\n' + CHANGES,
    license='BSD',
    classifiers=[
        "Programming Language :: Python",
        'License :: OSI Approved :: BSD License',
    ],
    author='Spiral Project',
    author_email='spiral-project@lolnet.org',
    url='https://github.com/spiral-project/daybed-browserid',
    keywords='authentication token hawk browserid daybed',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="daybed_browserid.tests"
)
