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

import test_main
from test_main import box2d
from pygame.locals import *

# Inspired by a contribution by roman_m (C++ version)
# Dimensions scooped from APE (http://www.cove.org/ape/index.htm)

class TheoJansen (test_main.Framework):
    name="TheoJansen"
    m_offset=box2d.b2Vec2() 
    m_chassis=box2d.b2Vec2()
    m_wheel=None
    m_motorJoint=None
    m_motorOn = False
    m_motorSpeed = 0

    def CreateLeg(self, s, wheelAnchor) :
        p1=box2d.b2Vec2(5.4 * s, -6.1)
        p2=box2d.b2Vec2(7.2 * s, -1.2)
        p3=box2d.b2Vec2(4.3 * s, -1.9)
        p4=box2d.b2Vec2(3.1 * s, 0.8)
        p5=box2d.b2Vec2(6.0 * s, 1.5)
        p6=box2d.b2Vec2(2.5 * s, 3.7)
        
        sd1=box2d.b2PolygonDef()
        sd2=box2d.b2PolygonDef()
        sd1.vertexCount = 3
        sd2.vertexCount = 3
        sd1.filter.groupIndex = -1
        sd2.filter.groupIndex = -1
        sd1.density = 1.0
        sd2.density = 1.0
        
        if s > 0.0:
            sd1.setVertex(0, p1)
            sd1.setVertex(1, p2)
            sd1.setVertex(2, p3)
            
            sd2.setVertex(0, box2d.b2Vec2_zero)
            sd2.setVertex(1, p5 - p4)
            sd2.setVertex(2, p6 - p4)
        else:
            sd1.setVertex(0, p1)
            sd1.setVertex(1, p3)
            sd1.setVertex(2, p2)
            
            sd2.setVertex(0, box2d.b2Vec2_zero)
            sd2.setVertex(1, p6 - p4)
            sd2.setVertex(2, p5 - p4)

        bd1=box2d.b2BodyDef()
        bd2=box2d.b2BodyDef()
        bd1.position = self.m_offset
        bd2.position = p4 + self.m_offset
        
        bd1.angularDamping = 10.0
        bd2.angularDamping = 10.0
        
        body1 = self.world.CreateBody(bd1) 
        body2 = self.world.CreateBody(bd2) 
        
        body1.CreateShape(sd1)
        body2.CreateShape(sd2)
        
        body1.SetMassFromShapes()
        body2.SetMassFromShapes()
        
        djd=box2d.b2DistanceJointDef()
        
        # Using a soft distance constraint can reduce some jitter.
        # It also makes the structure seem a bit more fluid by
        # acting like a suspension system.
        #djd.dampingRatio = 0.5
        #djd.frequencyHz = 10.0
        # usable, but doesn't act like it seems it should?
        
        djd.Initialize(body1, body2, p2 + self.m_offset, p5 + self.m_offset)
        self.world.CreateJoint(djd).getAsType() 
        
        djd.Initialize(body1, body2, p3 + self.m_offset, p4 + self.m_offset)
        self.world.CreateJoint(djd).getAsType() 
        
        djd.Initialize(body1, self.m_wheel, p3 + self.m_offset, wheelAnchor + self.m_offset)
        self.world.CreateJoint(djd).getAsType() 
        
        djd.Initialize(body2, self.m_wheel, p6 + self.m_offset, wheelAnchor + self.m_offset)
        self.world.CreateJoint(djd).getAsType() 
        
        rjd=box2d.b2RevoluteJointDef() 
        
        rjd.Initialize(body2, self.m_chassis, p4 + self.m_offset)
        self.world.CreateJoint(rjd).getAsType() 
    
    def __init__(self):
        super(TheoJansen, self).__init__()
        self.m_offset.Set(0.0, 8.0)
        self.m_motorSpeed = 2.0
        self.m_motorOn = True
        pivot=box2d.b2Vec2(0.0, 0.8)
        
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(50.0, 10.0)
        
        bd=box2d.b2BodyDef() 
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd) 
        ground.CreateShape(sd)
        
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(-50.0, 15.0), 0.0)
        ground.CreateShape(sd)
        
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(50.0, 15.0), 0.0)
        ground.CreateShape(sd)
        
        for i in range(40):
            sd = box2d.b2CircleDef()
            sd.density = 1.0
            sd.radius = 0.25
            
            bd=box2d.b2BodyDef() 
            bd.position.Set(-40.0 + 2.0 * i, 0.5)
            
            body = self.world.CreateBody(bd) 
            body.CreateShape(sd)
            body.SetMassFromShapes()
        
        sd=box2d.b2PolygonDef() 
        sd.density = 1.0
        sd.SetAsBox(2.5, 1.0)
        sd.filter.groupIndex = -1
        bd=box2d.b2BodyDef() 
        bd.position = pivot + self.m_offset
        self.m_chassis = self.world.CreateBody(bd)
        self.m_chassis.CreateShape(sd)
        self.m_chassis.SetMassFromShapes()
        
        sd = box2d.b2CircleDef()
        sd.density = 1.0
        sd.radius = 1.6
        sd.filter.groupIndex = -1
        bd=box2d.b2BodyDef() 
        bd.position = pivot + self.m_offset
        self.m_wheel = self.world.CreateBody(bd)
        self.m_wheel.CreateShape(sd)
        self.m_wheel.SetMassFromShapes()
    
        jd=box2d.b2RevoluteJointDef() 
        jd.Initialize(self.m_wheel, self.m_chassis, pivot + self.m_offset)
        jd.collideConnected = False
        jd.motorSpeed = self.m_motorSpeed
        jd.maxMotorTorque = 400.0
        jd.enableMotor = self.m_motorOn
        self.m_motorJoint = self.world.CreateJoint(jd).getAsType()
    
        wheelAnchor = pivot + box2d.b2Vec2(0.0, -0.8)
        
        self.CreateLeg(-1.0, wheelAnchor)
        self.CreateLeg(1.0, wheelAnchor)
        
        self.m_wheel.SetXForm(self.m_wheel.GetPosition(), 120.0 * box2d.b2_pi / 180.0)
        self.CreateLeg(-1.0, wheelAnchor)
        self.CreateLeg(1.0, wheelAnchor)
        
        self.m_wheel.SetXForm(self.m_wheel.GetPosition(), -120.0 * box2d.b2_pi / 180.0)
        self.CreateLeg(-1.0, wheelAnchor)
        self.CreateLeg(1.0, wheelAnchor)
    
    def Step(self, settings):
        self.DrawString(5, self.textLine, "Keys: left = a, brake = s, right = d, toggle motor = m")
        self.textLine += 15
        
        super(TheoJansen, self).Step(settings)
    
    def Keyboard(self, key):
        if key==K_a:
            self.m_chassis.WakeUp()
            self.m_motorJoint.SetMotorSpeed(-self.m_motorSpeed)
            
        elif key==K_s:
            self.m_chassis.WakeUp()
            self.m_motorJoint.SetMotorSpeed(0.0)
            
        elif key==K_d:
            self.m_chassis.WakeUp()
            self.m_motorJoint.SetMotorSpeed(self.m_motorSpeed)
            
        elif key==K_m:
            self.m_chassis.WakeUp()
            self.m_motorJoint.EnableMotor(not self.m_motorJoint.IsMotorEnabled())
    
if __name__=="__main__":
    test_main.main(TheoJansen)
