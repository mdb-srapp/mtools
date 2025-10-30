#!/usr/bin/env python3
"""Setup file for mlaunch."""

import platform
import re
import sys

# try importing from setuptools, if unavailable use distutils.core
try:
    from setuptools import setup, find_packages

    python_requires='>=3.8'

    # Additional dependencies from requirements.txt that should be installed
    # for full mlaunch feature support. These are optional dependencies to
    # simplify the default install experience, particularly where a build
    # toolchain is required.
    base_extras_requires = ['python-dateutil>=2.8.2,<3.0.0']
    extras_requires = {
        "all": ['pymongo>=4.3.2,<5.0.0', 'psutil>=5.9.3,<6.0.0', 'packaging>=21.3'] + base_extras_requires,
        "mlaunch": ['pymongo>=4.3.2,<5.0.0', 'psutil>=5.9.3,<6.0.0', 'packaging>=21.3'] + base_extras_requires,
    }

    install_requires = []
    
    try:
        import argparse
    except ImportError:
        install_requires.append('argparse')

    try:
        from collections import OrderedDict
    except ImportError:
        install_requires.append('ordereddict')

    packages = find_packages()
    kws = {'install_requires': install_requires}

except ImportError:
    from distutils.core import setup

    # find_packages not available in distutils, manually define packaging
    packages = ['mlaunch',
                'mlaunch.test',
                'mlaunch.util']
    kws = {}

# import version from mtools/version.py
with open('util/version.py') as f:
    exec(f.read())

# read README.rst for long_description content
with open('README.rst') as f:
    long_description = f.read()

if sys.platform == 'darwin' and 'clang' in platform.python_compiler().lower():
    from distutils.sysconfig import get_config_vars
    res = get_config_vars()
    for key in ('CFLAGS', 'PY_CFLAGS'):
        if key in res:
            flags = res[key]
            flags = re.sub('-mno-fused-madd', '', flags)
            res[key] = flags

setup(
    name='mlaunch',
    version=__version__,
    packages=packages,
    entry_points={
        "console_scripts": [
            "mlaunch=mlaunch:main",
        ],
    },
    author='Samantha Rapp',
    author_email='samantha.rapp@mongodb.com',
    url='https://github.com/mongodb/mlaunch',
    description=("A utility to quickly set up complex MongoDB test environments"
                "on a local machine "),
    long_description=long_description,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    keywords='MongoDB testing',
    extras_require=extras_requires,
    **kws
)
