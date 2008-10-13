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


# All easyPhysics stuff that should be in the local namespace
# Use 
#  from easyPhysics.locals import * 
# in your code


# Box2D locals:
import box2d

# a few variables that should be in the global scope from Box2D
__box2d_variables=[
    "B2_FLT_EPSILON",
    "B2_FLT_MAX",
    "FLT_EPSILON",
    "RAND_LIMIT",
    ]

# prefixes such as b2_ and e_ indicate enums, constants, etc.
__box2d_prefixes=(
    "b2",
    "e",
    )

__prefixed_vars = [varname for varname in dir(box2d)
                    if varname.split("_")[0] in __box2d_prefixes]

for __varname in __box2d_variables+__prefixed_vars:
    globals()[__varname]=getattr(box2d, __varname)

# easyPhysics locals:
ep_type    ="type"

# types:
# - shapes
ep_circle  ="circle"
ep_polygon ="polygon"
ep_edge    ="edge"
# - joints
ep_distance ="distance"
ep_gear     ="gear"
ep_line     ="line"
ep_mouse    ="mouse"
ep_prismatic="prismatic"
ep_pulley   ="pulley"
ep_revolute ="revolute"

# body creation
ep_shapes   ="shapes"
######### others


# (Note that not all are shown for each type, since
#  names overlap between the joints. See main.py
#  for specifics, or the documentation)
#
# shape creation
# - all shapes
ep_type         ="type"
ep_body         ="body"
ep_density      ="density"
ep_filter       ="filter"
ep_friction     ="friction"
ep_isSensor     ="isSensor"
ep_localPosition="localPosition"
ep_restitution  ="restitution"
ep_userData     ="userData"
# - circles
ep_radius       ="radius"
# - polygons
ep_vertices     ="vertices"
# - edges
ep_isALoop      ="isALoop"

# joint creation
# - all joints
ep_body1            ="body1"
ep_body2            ="body2"
ep_collideConnected ="collideConnected"
ep_type             ="type"
#ep_userData 
# - distance joint
ep_localAnchor1    ="localAnchor1"
ep_localAnchor2    ="localAnchor2"
ep_length          ="length"
# - gear joint
ep_joint1          ="joint1"
ep_joint2          ="joint2"
ep_ratio           ="ratio"
# - line joint
ep_enableLimit     ="enableLimit"
ep_enableMotor     ="enableMotor"
ep_localAxis1      ="localAxis1"
ep_maxMotorForce   ="maxMotorForce"
ep_motorSpeed      ="motorSpeed"
ep_lowerTranslation="lowerTranslation"
ep_upperTranslation="upperTranslation"
# - mouse joint
ep_target          ="target"
ep_maxForce        ="maxForce"
ep_frequencyHz     ="frequencyHz"
ep_dampingRatio    ="dampingRatio"
ep_timeStep        ="timeStep"
# - prismatic joint
ep_referenceAngle  ="referenceAngle"
# - pulley joint
ep_groundAnchor1   ="groundAnchor1"
ep_groundAnchor2   ="groundAnchor2"
ep_length1         ="length1"
ep_maxLength1      ="maxLength1"
ep_length2         ="length2"
ep_maxLength2      ="maxLength2"
# - revolute joint
ep_lowerAngle      ="lowerAngle"
ep_upperAngle      ="upperAngle"
ep_maxMotorTorque  ="maxMotorTorque"

ep_shape_types=(ep_circle,ep_polygon,ep_edge)
ep_joint_types=(ep_distance,ep_gear,ep_line,ep_mouse,ep_prismatic,ep_pulley,ep_revolute)

# easyPhysics exceptions:
class ep_Exception (Exception): pass
class ep_ArgumentRequired (ep_Exception): pass
class ep_InvalidParameter (ep_Exception): pass
class ep_InvalidScalingFunction (ep_Exception): pass
class ep_InvalidDefinition (ep_Exception): pass

