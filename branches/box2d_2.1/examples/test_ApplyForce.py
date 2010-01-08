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
from math import sqrt

class ApplyForce (Framework):
    name="ApplyForce"
    def __init__(self):
        super(ApplyForce, self).__init__()
        self.world.gravity = (0.0, 0.0)

        k_restitution = 0.4
        angle=0.5*b2_pi

        # The boundaries
        ground = self.world.CreateBody(
                b2BodyDef(
                    position=(0, 20), 
                    fixtures=[
                        b2PolygonShape(edge=[(-20,-20),(-20, 20)]),
                        b2PolygonShape(edge=[( 20,-20),( 20, 20)]),
                        b2PolygonShape(edge=[(-20, 20),( 20, 20)]),
                        b2PolygonShape(edge=[(-20,-20),( 20,-20)]),
                        ]) )

        xf1 = b2Transform()
        xf1.R.set(0.3524 * b2_pi)
        xf1.position = b2Mul(xf1.R, (1.0, 0.0))

        xf2 = b2Transform()
        xf2.R.set(-0.3524 * b2_pi)
        xf2.position = b2Mul(xf2.R, (-1.0, 0.0))

        self.body = self.world.CreateBody(
                b2BodyDef(
                    position=(0, 2), 
                    angle=b2_pi,
                    angularDamping=5,
                    linearDamping=0.1,
                    type=b2_dynamicBody,
                    fixtures=[ 
                        (b2PolygonShape(vertices=[xf1*(-1,0), xf1*(1,0), xf1*(0,.5)]), 2.0),
                        (b2PolygonShape(vertices=[xf2*(-1,0), xf2*(1,0), xf2*(0,.5)]), 2.0) ]
                    )
                )
     
        gravity = 10.0
        fixtures = [ b2FixtureDef(shape=b2PolygonShape(box=(0.5, 0.5)), density=1, friction=0.3) ]
        for i in range(10):
            body=self.world.CreateBody(b2BodyDef(type=b2_dynamicBody, position=(0,5+1.54*i), fixtures=fixtures))

            # For a circle: I = 0.5 * m * r * r ==> r = sqrt(2 * I / m)
            r = sqrt(2.0 * body.inertia / body.mass)

            self.world.CreateJoint(
                    b2FrictionJointDef(
                        localAnchorA=(0,0), 
                        localAnchorB=(0,0), 
                        bodyA = ground,
                        bodyB = body,
                        collideConnected=True,
                        maxForce = body.mass * gravity,
                        maxTorque = body.mass * r * gravity)
                    )

    def Keyboard(self, key):
        if not self.body:
            return

        if key==K_w:
            f = self.body.GetWorldVector((0.0, -200.0))
            p = self.body.GetWorldPoint((0.0, 2.0))
            self.body.ApplyForce(f, p)
        elif key==K_a:
            self.body.ApplyTorque(50.0)
        elif key==K_d:
            self.body.ApplyTorque(-50.0)

if __name__=="__main__":
     main(ApplyForce)
