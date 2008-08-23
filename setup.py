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

Linux:
 python setup.py build
 sudo python setup.py install 

OS X:
 See: http://code.google.com/p/pybox2d/wiki/OSXInstallation
 Assuming you have the dependencies, it should be as simple 
 as the Linux install.

General notes:
 * You can add data files to the release by modifying the directories.
 * These files will be assumed to be in the (release_dir)/[data_subdirs]
 * Set do_file_copy = True to package them 


TODO:

This script is really difficult to understand. Needs to be improved for
non-win32 installations and such.
"""

import distutils
from distutils.core import setup, Extension
from distutils.command import build_ext

import glob
import os

#-----------------------------------------------------------------
# config variables

# include release_dir/data_subdirs in the distribution (win32 only)
do_copy_data = True  

# do_copy_data uses this path:
release_dir = os.path.join("..", "Python") # "d:/dev/pybox2d/"

# copy files from this directory (e.g., setup.py) to the release dir
# copies: the interfaces, __init__.py, and setup.py to the appropriate release dirs
# -> see copy_files()
do_file_copy = True 

# subdirectories from release_dir
data_subdirs = ["testbed", "interface", "docs"]

# interface files to copy (and compile with)
interface_file = "Box2D.i"
fixed_interface_file = "Box2D_fixed.i"
build_type="float" #or 'fixed'

# release version number
box2d_version = "2.0.1"
release_number = 5

# all_data holds the filenames to include in the distribution
# -> shouldn't be used on linux, as it'll copy to '/' for some reason.
all_data = []

# ----------------------------------------------------------------
# support functions

def add_data(path, subdirs, ignore_extensions = (".pyo", ".pyc")):
    # Adds all valid files from path\[subdirs] to the list all_data
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
        return []
    build_ext.build_ext.get_export_symbols = patch_get_export_symbols
    print "[setup.py] Patched get_export_symbols for win32 build"

def distutils_fix():
    # okay, I really am not too fond of distutils now. someone please tell me I'm misinterpreting the code.
    # the default name would be Box2D2 for the py and the pyd, but the pyd needs to be _Box2D2, so correct that
    # here. (no way to change it with parameters?!)
    def patch_get_ext_filename(self, ext_name):
        return shared_lib_name
        
    real_get_ext_filename = build_ext.build_ext.get_ext_filename
    build_ext.build_ext.get_ext_filename=patch_get_ext_filename
    print "[setup.py] Patched get_ext_filename"

def copy_files():
    # Copies files to the release dir for packaging
    print "Copying files to the release directory..."

    from shutil import copy
    copy(interface_file, os.path.join(release_dir, "interface"))
    copy(fixed_interface_file, os.path.join(release_dir, "interface"))
    copy("__init__.py", release_dir) 
    copy("setup.py", release_dir)

#-----------------------------------------------------------------

# Create a simple __init__.py for the package
open("__init__.py","w").write("from Box2D2 import *")

if do_file_copy:
    copy_files()

# Create the version string
version_str = "%sb%s" % (box2d_version, str(release_number))

# Set the SWIG options
# [If you get -O unrecognized parameter for SWIG, your version is too old.]
build_ext_options = {'swig_opts':"-c++ -O -includeall -ignoremissing -w201", 'inplace':True}

# The shared lib name is _Box2D.so (linux), _Box2D.pyd (windows), etc.
shared_lib_name = "_Box2D2" + distutils.sysconfig.get_config_var('SO')

# Link to the appropriate build (fixed/float)
link_to = os.path.join("Gen", build_type, "libbox2d.a")

if distutils.util.get_platform() == "win32":
    if do_copy_data:
        add_data(release_dir, data_subdirs)

    distutils_win32_fix()

    print "Win32 detected. Attempting to use MinGW."
    build_ext_options['compiler']='mingw32'

# Fix the library name
distutils_fix()

try:
    compile_flags=os.environ["CXXFLAGS"].split(" ")
except KeyError:
    compile_flags="-O3".split(" ")

print "Compile flags:", compile_flags

setup (name = 'Box2D',
    version = version_str,
    packages=["Box2D2"],
    package_dir = {"Box2D2": "."},
    package_data={"Box2D2" : [shared_lib_name],  },
    options={'build_ext':build_ext_options}, 
    ext_modules = [Extension('Box2D2', [interface_file],
        extra_compile_args=compile_flags, extra_link_args=[link_to], language="c++")],
    data_files=all_data,
    author      = "kne",
    author_email = "sirkne at gmail dot com",
    description = "Box2D Python Wrapper",
    license="zlib",
    url="http://pybox2d.googlecode.com/",
    long_description = """Wraps Box2D (version %s) for usage in Python.
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

