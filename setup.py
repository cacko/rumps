#!/usr/bin/env python

import errno
import os
import sys
from pathlib import Path
import semver
from rumps import __title__

from setuptools import setup

INFO_PLIST_TEMPLATE = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>%(name)s</string>
</dict>
</plist>
'''


def fix_virtualenv():
    executable_dir = os.path.dirname(sys.executable)

    try:
        os.mkdir(os.path.join(executable_dir, 'Contents'))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with open(os.path.join(executable_dir, 'Contents', 'Info.plist'), 'w') as f:
        f.write(INFO_PLIST_TEMPLATE % {'name': 'rumps'})



def version():
    if len(sys.argv) > 1 and sys.argv[1] == "bdist_wheel":
        init = Path(__file__).parent / __title__ / "version.py"
        _, v = init.read_text().strip().split(" = ")
        cv = semver.VersionInfo.parse(v.strip('"'))
        nv = f"{cv.bump_patch()}"
        init.write_text(f'__version__ = "{nv}"')
        return nv
    from rumps.version import __version__
    return __version__

setup(
    name=__title__,
    version=version(),
    description='Ridiculously Uncomplicated MacOS Python Statusbar apps.',
    author='Jared Suttles',
    url='https://github.com/jaredks/rumps',
    packages=['rumps'],
    package_data={'': ['LICENSE']},
    license='BSD License',
    install_requires=[
        'pyobjc==9.2.1',
    ],
    extras_require={
        'dev': [
            'pytest>=4.3',
            'pytest-mock>=2.0.0',
            'tox>=3.8'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: MacOS X',
        'Environment :: MacOS X :: Cocoa',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Objective C',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
