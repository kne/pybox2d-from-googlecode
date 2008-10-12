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
E_TYPE    ="type"
E_CIRCLE  ="circle"

