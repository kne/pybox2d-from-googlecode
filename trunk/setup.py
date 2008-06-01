#!/usr/bin/env python

"""
pyBox2D setup script
--------------------

Basic Instructions
 1. Put this script in Box2D/Source
 2. Run: make
 3. Run: setup.py install

This script assumes Box2D has already been built via the Makefile, 
with the output in Gen/[float,fixed]/libbox2d.a depending on the build

Windows (MinGW)
    * Create Python\Lib\distutils\distutils.cfg if it doesn't exist and add:
        [build]
        compiler=mingw32
        [build_ext]
        compiler=mingw32
    * setup.py install somehow doesn't work without the above 
     (even if you specify -c mingw32 on the cmd line)
    * Then you can 
      setup.py [build/install]

Others (Linux and hopefully OS X):
 python setup.py install 

General notes:
 * You can add data files to the release by modifying the directories.
 * These files will be assumed to be in the (release_dir)/[data_subdirs]
 * Set do_file_copy = True to package them 

"""

import distutils
from distutils.core import setup, Extension
from distutils.command import build_ext

import glob
import os

# paths
release_dir = "C:\\dev\\pybox2d\\"
data_subdirs = ["testbed", "interface", "docs"]
interface_file = "Box2D.i"
fixed_interface_file = "Box2D_fixed.i"
build_type="float" #or 'fixed'

# release version number
box2d_version = "2.0.1"
release_number = 4

# other settings
do_file_copy = False
# ----------------------
def add_data(path, subdirs, ignore_extensions = (".pyo", ".pyc")):
    for walkdir in [os.path.join(path, subdir) for subdir in subdirs]:
        for root, dirs, files in os.walk(walkdir):
            if ".svn" in root: continue
            file_list=[]
            for filename in files:
                if ".swp" in filename: continue # vim
                elif os.path.splitext(filename)[1] in ignore_extensions: continue
                elif filename[0]=='.': continue
                file_list.append(os.path.join(root, filename))
            if file_list:
                all_data.append( (os.path.join("box2d", root[len(path):]), file_list) )

def distutils_win32_fix():
    # okay, so the problem is that there seems to be no actual way to remove the initBox2D2 from
    # the exported symbols, so we need to patch that from here.
    def patch_get_export_symbols(self,ext):
        # print "Hello! Patched get_export_symbols called."
        return []
    build_ext.build_ext.get_export_symbols = patch_get_export_symbols
    print "[setup.py] Patched get_export_symbols for win32 build"

def distutils_fix():
    # okay, I really am not too fond of distutils now. someone please tell me I'm misinterpreting the code.
    # the default name would be Box2D2 for the py and the pyd, but the pyd needs to be _Box2D2, so correct that
    # here. (no way to change it with parameters?!)
    def patch_get_ext_filename(self, ext_name):
        #print "Hello! Patched get_ext_filename called."
        #return "_" + real_get_ext_filename(self, ext_name)
        return shared_lib_name
        
    real_get_ext_filename = build_ext.build_ext.get_ext_filename
    build_ext.build_ext.get_ext_filename=patch_get_ext_filename


def copy_files():
    from shutil import copy
    copy(interface_file, os.path.join(release_dir, "interface"))
    copy(fixed_interface_file, os.path.join(release_dir, "interface"))
    copy("__init__.py", release_dir) 
    copy("setup.py", release_dir)

open("__init__.py","w").write("from Box2D2 import *")

if do_file_copy:
    copy_files()

build_ext_options = {'swig_opts':"-c++ -O -includeall -ignoremissing -w201", 'inplace':True}

shared_lib_name = "_Box2D2" + distutils.sysconfig.get_config_var('SO')
link_to = os.path.join("Gen", build_type)
link_to = os.path.join(link_to, "libbox2d.a")

version_str = box2d_version + 'b' + str(release_number)

all_data = []
add_data(release_dir, data_subdirs)

if distutils.util.get_platform() == "win32":
    win32 = True
    distutils_win32_fix()
    print "Attempting to use MinGW."
    build_ext_options['compiler']='mingw32'

distutils_fix()

setup (name = 'Box2D',
    version = version_str,
    packages=["Box2D2"],
    package_dir = {"Box2D2": "."},
    package_data={"Box2D2" : [shared_lib_name],  },
    options={'build_ext':build_ext_options}, 
        # ^^ these don't work if in Extension()
    ext_modules = [Extension('Box2D2', [interface_file],
        extra_compile_args=["-O3"], extra_link_args=[link_to], language="c++")],
    data_files=all_data,
    author      = "kne",
    author_email = "sirkne at gmail dot com",
    description = "Box2D Python Wrapper",
    license="zlib",
    url="http://code.google.com/p/pybox2d/",
    long_description = """Wraps Box2D (currently version %s) for usage in Python.
    For more information, see the homepage or Box2D's homepage at http://www.box2d.org .

    After installing, please be sure to try out the testbed demos (requires pygame).
    See <python directory>box2d/testbed/demos.py .

    Wiki: http://www.box2d.org/wiki/index.php?title=Box2D_with_Python
    Ports forum: http://www.box2d.org/forum/viewforum.php?f=5
    """ % (box2d_version),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Games :: Physics Libraries"
    ]
    )

