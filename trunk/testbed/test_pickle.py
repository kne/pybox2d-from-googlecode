#!/usr/bin/python
#
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlecode.com)
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from test_main import *
import cPickle as pickle

class Pickle(Framework):
    name = "Pickle" # Name of the class to display
    firstStep = True
    def __init__(self):
        super(Pickle, self).__init__()

        # load the example
        self.pickle_load('pickle_example_web')

        # for more info, see the pickle_load and pickle_save functions.

        # For using pickling in your own applications, there are several things
        # you have to be aware of:
        #  1. Saving the whole world is necessary. Shapes mean nothing without
        #     bodies, which mean nothing without a world to put them in. You
        #     can save your definitions, but that's additional overhead.
        #  2. Save the state of your application also. Saving the world won't 
        #     keep anything in relation to your game world. You can get 
        #     the index of the bodies you're tracking by doing:
        #      world.bodyList.index(myBody)
        #     and then work from there. Joints work the same.
        #  3. ...
        #
        #  XX. Bodies that left the world AABB aren't taken care of yet; this is a TODO

    def Keyboard(self, key):
        # F5/F7 taken care of by the main testbed.
        # F5 saves to 'pickle_output', F7 loads the same file
        pass

    def Step(self, settings):
        super(Pickle, self).Step(settings)
        self.DrawStringCR("So, does Pickling work?")

if __name__=="__main__":
    main(Pickle)


