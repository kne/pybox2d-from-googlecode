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


import box2d
from locals import *

class Config:
    frequency = 60.0
    renderer = None
    velocity_iter = 10
    position_iter = 8

class CollisionClass:
    def add(self, info): #todo: change to appropriate args
        pass
    def persist(self, info):
        pass
    def delete(self, info):
        pass

class Renderer:
    world_center=None
    screen_center=None

    world_aabb=None
    screen_aabb=None

    def render_object(self, **kw):
        pass

    def world_to_screen(self, world):
        pass

    def screen_to_world(self, screen):
        pass


def init(**kw):
    #    if kw["frequency"]:
    # frequency, (renderer, vel/pos iterations, )
    pass

def set_renderer( myRenderer ):
    pass

# get/set -- use property

def create_body(bodyDef):
    pass

def save_world(file, format="xml"): # xml/pickle
    pass

def load_world(file, format="xml"):
    pass

def step():
    # skip render, pause physics step, ...
    pass

def get_bodies():
    for i in []:
        yield i 

def get_shapes(body):
    for i in []:
        yield i 

def get_all_shapes():
    for i in []:
        yield i 

def pick(pos):
    pass

