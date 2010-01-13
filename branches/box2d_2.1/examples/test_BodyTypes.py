#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2010 Ken Lauer / sirkne at gmail dot com
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

class BodyTypes (Framework):
    name="Body Types"
    description="Change body type keys: (d) dynamic, (s) static, (k) kinematic"
    speed = 3 # platform speed
    def __init__(self):
        super(BodyTypes, self).__init__()


        # The ground
        ground = self.world.CreateBody(
                b2BodyDef(
                    fixtures=[ 
                        b2PolygonShape(edge=[(-20,0),(20,0)]) 
                        ]
                    )
                )

        # The attachment
        fixture=(b2PolygonShape(box=(0.5,2)), 2.0) # (shape, density)
        self.attachment=self.world.CreateBody(
                b2BodyDef(
                    type=b2_dynamicBody,
                    position=(0,3), 
                    fixtures=[fixture],
                    )
                )
    
        # The platform
        fixture=b2FixtureDef(
                    shape=b2PolygonShape(box=(4,0.5)),
                    friction=0.6,
                    density=2,
                )
               
        self.platform=self.world.CreateBody(
                b2BodyDef(
                    type=b2_dynamicBody,
                    position=(0,3), 
                    fixtures=[fixture],
                    )
                )
        
        # The joints joining the attachment/platform and ground/platform
        self.world.CreateJoint(
                b2RevoluteJointDef(
                    bodyA=self.attachment,
                    bodyB=self.platform,
                    anchor=(0,5),
                    maxMotorTorque=50,
                    enableMotor=True
                    )
                )

        self.world.CreateJoint(
                b2PrismaticJointDef(
                        bodyA=ground,
                        bodyB=self.platform,
                        anchor=(0,5),
                        axis=(1,0),
                        maxMotorForce = 1000,
                        enableMotor = True,
                        lowerTranslation = -10,
                        upperTranslation = 10,
                        enableLimit = True 
                    )
                )

        # And the payload that initially sits upon the platform
        # Reusing the fixture we previously defined above
        fixture.shape.box = (0.75, 0.75)
        self.payload=self.world.CreateBody(
                b2BodyDef(
                    type=b2_dynamicBody,
                    position=(0,8), 
                    fixtures=[fixture],
                    )
                )


    def Keyboard(self, key):
        if key==K_d:
            self.platform.type=b2_dynamicBody
        elif key==K_s:
            self.platform.type=b2_staticBody
        elif key==K_k:
            self.platform.type=b2_kinematicBody
            self.platform.linearVelocity=(-self.speed, 0)
            self.platform.angularVelocity=0

    def Step(self, settings):
        super(BodyTypes, self).Step(settings)

        if self.platform.type==b2_kinematicBody:
            p = self.platform.transform.position
            v = self.platform.linearVelocity
            if ((p.x < -10 and v.x < 0) or (p.x > 10 and v.x > 0)):
                v.x = -v.x
                self.platform.linearVelocity = v

if __name__=="__main__":
     main(BodyTypes)
