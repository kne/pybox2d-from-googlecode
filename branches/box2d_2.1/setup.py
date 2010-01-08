#!/usr/bin/env python
"""
Setup script for pybox2d.

For installation instructions, see INSTALL.

Basic install steps:
 setup.py build

If that worked, then:
 setup.py install
"""

from __future__ import print_function
import os
import sys
from glob import glob

setuptools_version=None
try:
    import setuptools
    from setuptools import (setup, Extension)
    setuptools_version=setuptools.__version__
    print('Using setuptools (version %s).' % setuptools_version)
except:
    from distutils.core import (setup, Extension)
    print('Setuptools not found; falling back on distutils.')

if setuptools_version:
    if (setuptools_version in ["0.6c%d"%i for i in range(1,9)] # old versions
        or setuptools_version=="0.7a1"): # 0.7a1 py 3k alpha version based on old version
            print('Patching setuptools.build_ext.get_ext_filename')
            from setuptools.command import build_ext
            def get_ext_filename(self, fullname):
                from setuptools.command.build_ext import (_build_ext, Library, use_stubs)
                filename = _build_ext.get_ext_filename(self,fullname)
                if fullname in self.ext_map:
                    ext = self.ext_map[fullname]
                    if isinstance(ext,Library):
                        fn, ext = os.path.splitext(filename)
                        return self.shlib_compiler.library_filename(fn,libtype)
                    elif use_stubs and ext._links_to_dynamic:
                        d,fn = os.path.split(filename)
                        return os.path.join(d,'dl-'+fn)
                return filename
            build_ext.build_ext.get_ext_filename = get_ext_filename

# release version number
box2d_version  = '2.1'
release_number = 0

# create the version string
version_str = "%sb%s" % (box2d_version, str(release_number))

def write_init(): 
    # read in the license header
    license_header = open(os.path.join('Box2D', 'pybox2d_license_header.txt')).read()

    # create the source code for the file
    if sys.version_info >= (2, 5):
        import_string = "from .Box2D import *"
    else:
        import_string = "from Box2D import *"

    init_source = [
        import_string,
        "__version__      = '%s'"    % version_str,
        "__version_info__ = (%s,%d)" % (box2d_version.replace('.', ','), release_number), ]

    # and create the __init__ file with the appropriate version string
    f=open('__init__.py', 'w')
    f.write(license_header)
    f.write( '\n'.join(init_source) )
    f.close()
    
source_paths = [
    os.path.join('Box2D', 'Dynamics'),
    os.path.join('Box2D', 'Dynamics', 'Contacts'),
    os.path.join('Box2D', 'Dynamics', 'Joints'),
    os.path.join('Box2D', 'Common'),
    os.path.join('Box2D', 'Collision'),
    os.path.join('Box2D', 'Collision', 'Shapes'),
    ]

# glob all of the paths and then flatten the list into one
box2d_source_files = [os.path.join('Box2D', 'Box2D.i')] + \
    sum( [glob(os.path.join(path, "*.cpp")) for path in source_paths], [])

# arguments to pass to SWIG. for old versions of SWIG, -O (optimize) might not be present.
swig_arguments = '-c++ -IBox2D -O -includeall -ignoremissing -w201 -globals b2Globals -outdir .'

pybox2d_extension = \
    Extension('Box2D._Box2D', box2d_source_files, extra_compile_args=['-I.'], language='c++')

LONG_DESCRIPTION = \
""" 2D physics library Box2D %s for usage in Python.

    After installing please be sure to try out the testbed demos.
    They require either pygame or pyglet and are available on the
    homepage.

    pybox2d homepage: http://pybox2d.googlecode.com
    Box2D's homepage: http://www.box2d.org
    """ % (box2d_version,)

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: zlib/libpng License",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: POSIX",
    "Programming Language :: Python",
    "Games :: Physics Libraries"
    ]

write_init()

setup_dict = dict(
    name             = "Box2D",
    version          = version_str,
    author           = "Ken Lauer",
    author_email     = "sirkne at gmail dot com",
    description      = "Python Box2D",
    license          = "zlib",
    url              ="http://pybox2d.googlecode.com/",
    long_description = LONG_DESCRIPTION,
    classifiers      = CLASSIFIERS,
    packages         = ['Box2D'],
    package_dir      = {'Box2D': '.'},
    test_suite       = "tests",
    options          = { 'build_ext': { 'swig_opts' : swig_arguments } },
    ext_modules      = [ pybox2d_extension ]
    )

# run the actual setup from distutils
setup( **setup_dict )
