#!/usr/bin/env python
#
# Copyright (c) 2008 kne / sirkne at gmail dot com
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

import easyPhysics as ep
from easyPhysics.locals import * # includes box2d locals

# modifies some box2d functions to include pythonic usage
# stores created bodies/shapes for pickling
# xml saving/loading
# 
# 
# 
# 

class genericCollisionHandler (ep.CollisionClass):
    def add(self, info): #todo: change to appropriate args
        # delete object -> check at end of step() fcn to remove them
        pass
    def persist(self, info):
        pass
    def delete(self, info):
        pass

class collisionClass1 (ep.CollisionClass):
    def add(self, info):
        print "collided"

class Renderer (ep.Renderer):
    # world_center, screen_center
    # world_aabb, screen_aabb

    def render_object(self, **kw):
        first, last = kw["first_object"], kw["last_object"]
        if first:
            # clear screen
            pass

        print kw
        # body/shape/x/y/rot -> for polygons, modified vertices

        if last:
            # flip if necessary
            pass

    def world_to_screen(self, world):
        # tell ep the screen location of world position
        # use zoom, screen center
        screen = world
        return screen

    def screen_to_world(self, screen):
        # tell ep the world location of screen position
        world = screen
        return world

ep.init(frequency=60)
#ep.set_scale_function(world_to_screen, screen_to_world) # screen to world optional (both optional if display callback not enabled)
#new idea:
myRenderer = Renderer()
ep.set_renderer( myRenderer )
# warn if scale functions not symmetric
# warn if scale is small (<= world 1:screen 2 ?)
# have basic w2s/s2w functions setup for common libraries, given scale
#  -- updatable by functions or camera tracking
#ep.set_display_callback(display_fcn) # raise error if scale function not set

shape1  = { 
            E_TYPE    : E_CIRCLE,
            "radius"  : 1.0,
            "position": (0.0, 0.0),
            "collisionGroup" : collisionClass1,
          }
bodyDef = { 
            "density"  : 1.0,
            "position" : (0.0, 0.0),
            "userdata" : "",
            "shapes"   : [shape1],
          }

ep.create_body(bodyDef)

ep.save_world("world.xml")
ep.load_world("world2.xml")

# initialize pygame/etc

running = True
while running:
    # display function called here
    ep.step()
    # callbacks for rendering called as necessary

    gotClick = False #
    # check if events...
    if gotClick: # clicked
        pos = event.pos
        shapes = ep.pick(pos)

    # do something each call
    for body in ep.get_bodies():
        for shape in body.get_shapes():
            if shape.type == e_circleShape:
                print shape.radius
    for shape in ep.get_all_shapes():
        print shape.radius
    exit(0)
