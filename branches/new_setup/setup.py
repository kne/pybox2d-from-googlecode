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

# release version number
box2d_version = "2.0.2"
release_number = 0

# Create the version string
version_str = "%sb%s" % (box2d_version, str(release_number))

box2d_source_files = [
    'Box2D/Dynamics/b2Body.cpp',
    'Box2D/Dynamics/b2Island.cpp',
    'Box2D/Dynamics/b2World.cpp',
    'Box2D/Dynamics/b2ContactManager.cpp',
    'Box2D/Dynamics/Contacts/b2Contact.cpp',
    'Box2D/Dynamics/Contacts/b2PolyContact.cpp',
    'Box2D/Dynamics/Contacts/b2CircleContact.cpp',
    'Box2D/Dynamics/Contacts/b2PolyAndCircleContact.cpp',
    'Box2D/Dynamics/Contacts/b2EdgeAndCircleContact.cpp',
    'Box2D/Dynamics/Contacts/b2PolyAndEdgeContact.cpp',
    'Box2D/Dynamics/Contacts/b2ContactSolver.cpp',
    'Box2D/Dynamics/Controllers/b2BuoyancyController.cpp',
    'Box2D/Dynamics/Controllers/b2ConstantAccelController.cpp',
    'Box2D/Dynamics/Controllers/b2ConstantForceController.cpp',
    'Box2D/Dynamics/Controllers/b2Controller.cpp',
    'Box2D/Dynamics/Controllers/b2GravityController.cpp',
    'Box2D/Dynamics/Controllers/b2TensorDampingController.cpp',
    'Box2D/Dynamics/b2WorldCallbacks.cpp',
    'Box2D/Dynamics/Joints/b2MouseJoint.cpp',
    'Box2D/Dynamics/Joints/b2PulleyJoint.cpp',
    'Box2D/Dynamics/Joints/b2Joint.cpp',
    'Box2D/Dynamics/Joints/b2RevoluteJoint.cpp',
    'Box2D/Dynamics/Joints/b2PrismaticJoint.cpp',
    'Box2D/Dynamics/Joints/b2DistanceJoint.cpp',
    'Box2D/Dynamics/Joints/b2GearJoint.cpp',
    'Box2D/Dynamics/Joints/b2LineJoint.cpp',
    'Box2D/Common/b2StackAllocator.cpp',
    'Box2D/Common/b2Math.cpp',
    'Box2D/Common/b2BlockAllocator.cpp',
    'Box2D/Common/b2Settings.cpp',
    'Box2D/Collision/b2Collision.cpp',
    'Box2D/Collision/b2Distance.cpp',
    'Box2D/Collision/Shapes/b2Shape.cpp',
    'Box2D/Collision/Shapes/b2CircleShape.cpp',
    'Box2D/Collision/Shapes/b2PolygonShape.cpp',
    'Box2D/Collision/Shapes/b2EdgeShape.cpp',
    'Box2D/Collision/b2TimeOfImpact.cpp',
    'Box2D/Collision/b2PairManager.cpp',
    'Box2D/Collision/b2CollidePoly.cpp',
    'Box2D/Collision/b2CollideCircle.cpp',
    'Box2D/Collision/b2BroadPhase.cpp']

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
       
    packages = ['Box2D'],
    package_dir = {'Box2D': 'Box2D'},
    py_modules = ['Box2D2'],
    options={'build_ext':{'swig_opts':swig_arguments}},
    ext_modules = [Extension('_Box2D', ['Box2D/Box2D.i'] + box2d_source_files,
                    language="c++"),]
    )

