#!/usr/bin/env python

"""
Test
"""

from distutils.core import setup, Extension
import glob

package_dir ="bin"
package_type="float"

import os
#init = open(os.path.join(package_dir, "__init__.py"), "w")
#init.write("from Box2D2 import *")
#init.close()

box2d_version = "2.0.1"
release_number = 2
version_str = box2d_version + 'b' + str(release_number)

all_data = []

for walkdir in ('.\\testbed', '.\\interface'):
    for root, dirs, files in os.walk(walkdir):
        if ".svn" in root: continue
        file_list=[]
        for filename in files:
            if ".swp" in filename: continue # vim
            if filename[0]=='.': continue  
            file_list.append(os.path.join(root, filename))
        if file_list:
            all_data.append( ("box2d_" + root[2:], file_list) )

setup (name = 'Box2D',
        version = version_str,
        packages=["Box2D2"],
        package_dir = {"Box2D2": package_dir},
        package_data={"Box2D2" : ["_Box2D2.pyd"],  },
        data_files=all_data,
        author      = "kne",
        author_email = "sirkne at gmail dot com",
        description = "Box2D Python Wrapper",
        license="zlib",
        url="http://code.google.com/p/pybox2d/",
        long_description = """Wraps Box2D (currently version %s) for usage in Python.
        For more information, see the homepage or Box2D's homepage at http://www.box2d.org .

        After installing, please be sure to try out the testbed demos (requires pygame).
        See testbed/demos.py .

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

