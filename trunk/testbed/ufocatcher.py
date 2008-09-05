#!/usr/bin/python
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

from test_main import *

class UFOContactListener(box2d.b2ContactListener):
    """
    Handles all of the contact states passed in from Box2D.
    """
    ufomain = None
    def __init__(self, ufomain):
        super(UFOContactListener, self).__init__()
        self.ufomain = ufomain

    def handleCall(self, state, point):
        return

        k_maxContactPoints = 2048
        if len(self.test.points) == k_maxContactPoints: return

        self.test.points.append( fwContactPoint() )
        cp = self.test.points[-1]
        cp.shape1 = point.shape1
        cp.shape2 = point.shape2
        cp.position = point.position.copy()
        cp.normal = point.normal.copy()
        cp.id = point.id
        cp.state = state

    def Add(self, point):
        bodies = [point.shape1.GetBody(), point.shape2.GetBody()]
        
        if self.ufomain.goal in bodies:
            bodies.remove(self.ufomain.goal)
            self.ufomain.ReachedGoal(bodies[0])

    def Persist(self, point):
        pass

    def Remove(self, point):
        pass

class UFOCatcher (Framework):
    name="UFOCatcher"
    gearw = None # wheel to control the gear joint for horizontal movement
    mainc = None # main control circle (at top of grabber)
    lgrips, rgrips = [], [] # grip (grabber) bodies
    ljoints, rjoints=[], [] # grip joints
    gripClose = False
    gripforce = 150.0
    stackheight = 5
    objects = []
    contactListener = None
    goal = None
    removeList = []
    def CreateGrips(self, left, sd, tipsd, gripextents, gripoverlap, startpos, count):
        grips  = []
        joints = []            
        
        jd=box2d.b2RevoluteJointDef() 
        jd.enableLimit  = True

        step = -gripextents.x + gripoverlap

        if left:
            jd.localAnchor1 = box2d.b2Vec2(-gripextents.x/2, 0)
            jd.localAnchor2 = box2d.b2Vec2( gripextents.x/2, 0)
            jd.lowerAngle   = 0.2 * box2d.b2_pi  # 0 degrees (left)
            jd.upperAngle   = 0.5 * box2d.b2_pi  #90 degrees (down)
        else:
            jd.localAnchor1 = box2d.b2Vec2( gripextents.x/2, 0)
            jd.localAnchor2 = box2d.b2Vec2(-gripextents.x/2, 0)
            jd.lowerAngle   =-0.5 * box2d.b2_pi  # 0 degrees (right)
            jd.upperAngle   =-0.2 * box2d.b2_pi  #90 degrees (down)
            step = -step

            for i in xrange(tipsd.vertexCount):
                v = -tipsd.getVertex(i)
                tipsd.setVertex(i,v.x,v.y)

        bd=box2d.b2BodyDef()
        bd.position = startpos
        bd.angularDamping = 500.0

        for i in xrange(count):
            grips.append(self.world.CreateBody(bd))
            grip = grips[-1]

            if i==count-1:
                grip.CreateShape(tipsd)
            else:
                grip.CreateShape(sd)

            grip.SetMassFromShapes()

            # left grip 1-2 revolute joint
            if i==0:
                jd.localAnchor1 = box2d.b2Vec2(-gripoverlap, 0)
                jd.body1 = self.mainc
            else:
                jd.localAnchor1 = box2d.b2Vec2(-gripextents.x/2, 0)
                jd.body1 = grips[-2]

            if not left:
                jd.localAnchor1.x = -jd.localAnchor1.x

            jd.body2 = grip
            joints.append( self.world.CreateJoint(jd).getAsType() )
            
            bd.position.x += step

        return grips, joints

    def ReachedGoal(self, body):
        if body not in self.removeList:
            print "Reached goal!", type(body)
            self.removeList.append(body)

    def __init__(self):
        super(UFOCatcher, self).__init__()
    
        self.contactListener = UFOContactListener(self)
        self.world.SetContactListener(self.contactListener)

        # ground
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)

        # side walls
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(-15.0, 15.0), 0)
        ground.CreateShape(sd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(15.0, 15.0), 0)
        ground.CreateShape(sd)

        # goal (base)
        bd=box2d.b2BodyDef()
        bd.position.Set(22.0, 0.0)
        self.goal = goal = self.world.CreateBody(bd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(5.0, 1.0)
        goal.CreateShape(sd)

        # goal walls
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.25, 1.5, box2d.b2Vec2(-5.0, 2.0), 0)
        goal.CreateShape(sd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.25, 1.5, box2d.b2Vec2(5.0, 2.0), 0)
        goal.CreateShape(sd)

        # gear wheel
        sd=box2d.b2CircleDef() 
        sd.radius = 2.0
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        bd.position.Set(-25.0, 20.0)
        bd.angularDamping = 2.0
        self.gearw = gearw = self.world.CreateBody(bd)
        gearw.CreateShape(sd)
        gearw.SetMassFromShapes()

        # connect gear wheel to ground by revolute joint
        jd=box2d.b2RevoluteJointDef() 
        jd.Initialize(ground, gearw, gearw.GetWorldCenter())
        gearw_rj = self.world.CreateJoint(jd).getAsType()

        # top control circle (topc)
        sd=box2d.b2CircleDef() 
        sd.radius = 0.5
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 30.0)
        self.topc = topc = self.world.CreateBody(bd)
        topc.CreateShape(sd)
        topc.SetMassFromShapes()

        # main control circle (mainc)
        sd=box2d.b2CircleDef() 
        sd.radius = 0.5
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        bd.position = topc.GetWorldCenter() - box2d.b2Vec2(0,10.0)
        self.mainc = mainc = self.world.CreateBody(bd)
        mainc.CreateShape(sd)
        mainc.SetMassFromShapes()

        # prismatic joint for horizontal movement of control circle
        jd=box2d.b2PrismaticJointDef() 
        jd.Initialize(ground, topc, topc.GetWorldCenter(), box2d.b2Vec2(1.0, 0.0))
        jd.lowerTranslation = -18.0
        jd.upperTranslation = 40.0
        jd.enableLimit = True

        gearw_pj = self.world.CreateJoint(jd).getAsType()

        # gear joint -> gear wheel - horiz movement
        jd=box2d.b2GearJointDef() 
        jd.body1  = gearw
        jd.body2  = topc
        jd.joint1 = gearw_rj
        jd.joint2 = gearw_pj
        jd.ratio  = 10.0
        jd.maxMotorTorque = 0.0
        jd.motorSpeed = 0.0
        jd.enableMotor = True
        self.world.CreateJoint(jd).getAsType()

        # vertical distance joint to main control circle
        jd=box2d.b2DistanceJointDef() 
        jd.body1 = topc
        jd.body2 = mainc
        jd.localAnchor1.Set(0.0, 0.0)
        jd.localAnchor2.Set(0.0, 0.0)
        d = jd.body2.GetWorldPoint(jd.localAnchor2) - jd.body1.GetWorldPoint(jd.localAnchor1)
        jd.length = d.Length()
        self.ropejd = jd
        self.ropej  = self.world.CreateJoint(jd).getAsType() 

        gripextents = box2d.b2Vec2(3.0, 1.0) 
        gripstart   = mainc.GetWorldPoint(box2d.b2Vec2_zero)
        gripoverlap = 0.125

        self.gripextents = gripextents

        tipsd=box2d.b2PolygonDef()
        tipsd.setVertices_tuple( [
                    (gripextents.x/2, gripextents.y/2), 
                    (-gripextents.x/2, 0.0),
                    (gripextents.x/2, -gripextents.y/2) ] )
        tipsd.density = 1.8

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(gripextents.x/2, gripextents.y/2) # SetAsBox takes half-width/height
        sd.density = 1.8

        self.lgrips, self.ljoints=self.CreateGrips(True , sd, tipsd, gripextents, gripoverlap, gripstart, 3)
        self.rgrips, self.rjoints=self.CreateGrips(False, sd, tipsd, gripextents, gripoverlap, gripstart, 3)

        # make a few stacks to grab from
        sd=box2d.b2CircleDef()
        sd.radius = 1.0
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        
        for y in xrange(self.stackheight):
            bd.position.Set(0.0, 2.0 + 3.0 * y)
            
            self.objects.append( self.world.CreateBody(bd) )
            self.objects[-1].CreateShape(sd)
            self.objects[-1].SetMassFromShapes()



    def Step(self, settings):
        self.DrawString(5, self.textLine, "Let's ufo catch!")
        self.textLine += 15

        for body in self.removeList:
            self.world.DestroyBody(body)

        self.removeList = []

        if self.gripClose:
            force = box2d.b2Vec2(self.gripforce, 0.0)
        else:
            force = box2d.b2Vec2(-self.gripforce, 0.0)

        # keep the grip open
        # left side
        grip = self.lgrips[-1]
        point = grip.GetWorldPoint(box2d.b2Vec2(-self.gripextents.x/2,0.0))
        grip.ApplyForce(force, point)

        # right side
        grip = self.rgrips[-1]
        point = grip.GetWorldPoint(box2d.b2Vec2(self.gripextents.x/2,0.0))
        force = -force
        grip.ApplyForce(force, point)

        #self.debugDraw.DrawPoint(point, settings.pointSize, box2d.b2Color(1.0,0.0,1.0))
        #self.debugDraw.DrawPoint(point, settings.pointSize, box2d.b2Color(1.0,1.0,0.0))

        super(UFOCatcher, self).Step(settings)

    def Keyboard(self, key):
        if key == K_w:
            if self.ropejd.length > 1.0:
                self.world.DestroyJoint(self.ropej)
                self.ropejd.length -= 0.1
                self.ropej  = self.world.CreateJoint(self.ropejd).getAsType() 
        elif key == K_s:
            self.world.DestroyJoint(self.ropej)
            self.ropejd.length += 0.1
            self.ropej  = self.world.CreateJoint(self.ropejd).getAsType() 
        elif key == K_a:
            self.gearw.ApplyForce( box2d.b2Vec2(100.0,0.0), box2d.b2Vec2(0.0,0.0))
        elif key == K_d:
            self.gearw.ApplyForce( box2d.b2Vec2(-100.0,0.0), box2d.b2Vec2(0.0,0.0))
        elif key == K_c:
            self.gripClose = not self.gripClose
        elif key == K_q:
            for joint in self.ljoints+self.rjoints:
                self.world.DestroyJoint(joint)

if __name__=="__main__":
    main(UFOCatcher)
