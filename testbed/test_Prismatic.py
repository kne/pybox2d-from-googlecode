#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
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

from pygame.locals import *
import test_main
from test_main import box2d
class Prismatic (test_main.Framework):
    name="Prismatic"
    def __init__(self):
        super(Prismatic, self).__init__()
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        ground.CreateShape(sd)
    
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(2.0, 0.5)
        sd.density = 5.0
        sd.friction = 0.05
        
        bd=box2d.b2BodyDef()
        bd.position.Set(-10.0, 10.0)
        bd.angle = 0.5 * box2d.b2_pi
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetMassFromShapes()
        
        pjd=box2d.b2PrismaticJointDef()
        
        # Bouncy limit
        pjd.Initialize(ground, body, box2d.b2Vec2(0.0, 0.0), box2d.b2Vec2(1.0, 0.0))
        
        # Non-bouncy limit
        #pjd.Initialize(ground, body, box2d.b2Vec2(-10.0, 10.0), box2d.b2Vec2(1.0, 0.0))
        
        pjd.motorSpeed = 10.0
        pjd.maxMotorForce = 1000.0
        pjd.enableMotor = True
        pjd.lowerTranslation = 0.0
        pjd.upperTranslation = 20.0
        pjd.enableLimit = True
        
        self.m_joint = self.world.CreateJoint(pjd).getAsType()
    
    def Keyboard(self, key):
        if key==K_l:
            self.m_joint.EnableLimit(not self.m_joint.IsLimitEnabled())
        elif key==K_m:
            self.m_joint.EnableMotor(not self.m_joint.IsMotorEnabled())
        elif key==K_p:
            self.m_joint.SetMotorSpeed(-self.m_joint.GetMotorSpeed())
    
    def Step(self, settings):
        self.DrawString(5, self.textLine, "Keys: (l) limits, (m) motors, (p) speed")
        self.textLine += 15
        
        force = self.m_joint.GetMotorForce()
        self.DrawString(5, self.textLine, "Motor Force = %f.0" % force)
        self.textLine += 15
        super(Prismatic, self).Step(settings)
    
if __name__=="__main__":
    test_main.main(Prismatic)
