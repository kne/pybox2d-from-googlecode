#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2010 kne / sirkne at gmail dot com
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

from pygame_main import *
from math import cos, sin

class CharacterCollision (Framework):
    name="CharacterCollision"
    description='This is a test of typical character collision scenarios. This does not\n show how you should implement a character in your application.'
    def __init__(self):
        super(CharacterCollision, self).__init__()

        ground = self.world.CreateStaticBody(
                    position=(0,0),
                    shapes=b2PolygonShape(edge=[(-20,0), (20,0)])
                )
        
        # Collinear edges
        self.world.CreateStaticBody(
                    shapes=[b2PolygonShape(edge=[(-8,1), (-6,1)]),
                            b2PolygonShape(edge=[(-6,1), (-4,1)]),
                            b2PolygonShape(edge=[(-4,1), (-2,1)]),
                            ]
                )
        
        # Square tiles
        self.world.CreateStaticBody(
                    shapes=[b2PolygonShape(box=[1, 1, (4,3), 0]),
                            b2PolygonShape(box=[1, 1, (6,3), 0]),
                            b2PolygonShape(box=[1, 1, (8,3), 0]),
                            ]
                )

        # Square made from edges. Notice how the edges are shrunk to account
        # for the polygon radius. This makes it so the square character does
        # not get snagged. However, ray casts can now go through the cracks.
        self.world.CreateStaticBody(
                    shapes=[ b2PolygonShape(vertices=[(-1,3), (1,3), (1,5), (-1,5)]) ]
                )


        # Square character
        self.world.CreateDynamicBody(
                    position=(-3, 5),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)), density=20.0),
                    linearVelocity=(0,-50)
                )
        
        # Hexagon character
        a=b2_pi/3.0
        self.world.CreateDynamicBody(
                    position=(-5, 5),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(
                            shape=b2PolygonShape(vertices=[(0.5*cos(i*a), 0.5*sin(i*a)) for i in range(6)]),
                            density=20.0
                            ),
                )
        
        # Circle character
        self.world.CreateDynamicBody(
                    position=(3, 5),
                    fixedRotation=True,
                    allowSleep=False,
                    fixtures=b2FixtureDef(
                            shape=b2CircleShape(radius=0.5),
                            density=20.0
                            ),
                )


    def Step(self, settings):
        super(CharacterCollision, self).Step(settings)
        pass

if __name__=="__main__":
     main(CharacterCollision)
