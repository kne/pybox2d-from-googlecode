#!/usr/bin/env python
"""
Setup script for pyBox2D distribution.

For installation instructions, see INSTALL.

Basic install steps:
 setup.py build

If that worked, then:
 setup.py install
"""

import os
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_inc
from glob import glob

# release version number
box2d_version = "2.0.2"
release_number = 0

# Create the version string
version_str = "%sb%s" % (box2d_version, str(release_number))

source_paths = [
    'Box2D/Dynamics/',
    'Box2D/Dynamics/Contacts/',
    'Box2D/Dynamics/Controllers/',
    'Box2D/Dynamics/Joints/',
    'Box2D/Common/',
    'Box2D/Collision/',
    ]

# glob all of the paths and then flatten the list into one
box2d_source_files = sum( [glob(os.path.join(path, "*.cpp")) for path in source_paths], [])

swig_arguments = '-c++ -O -includeall -ignoremissing -w201'

setup (name = "Box2D",
    version = version_str,
    author      = "kne",
    author_email = "sirkne at gmail dot com",
    description = "Python Box2D",
    license="zlib",
    url="http://pybox2d.googlecode.com/",
    long_description = """Box2D (version %s) for usage in Python.

After installing, please be sure to try out the testbed demos (requires pygame).
See <python directory>box2d/testbed/demos.py .

For more information, see:

pybox2d homepage: http://pybox2d.googlecode.com
Box2D's homepage: http://www.box2d.org
    """ % (box2d_version),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Games :: Physics Libraries"
    ],
       
#    packages = ['Box2D'],
#    package_dir = {'Box2D': 'Box2D'},
    py_modules = ['Box2D'],
    options={'build_ext':{'swig_opts':swig_arguments}},
    ext_modules = [Extension('_Box2D', ['Box2D/Box2D.i'] + box2d_source_files,
                    extra_compile_args=["-I."], language="c++"),]
    )

