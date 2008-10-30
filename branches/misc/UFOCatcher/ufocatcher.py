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
import rabbyt

from math import sqrt, sin, cos,atan

class UFOContactListener(box2d.b2ContactListener):
    """
    Handles all of the contact states passed in from Box2D.
    """
    ufomain = None
    def __init__(self, ufomain):
        super(UFOContactListener, self).__init__()
        self.ufomain = ufomain

    def getOtherBody(self, point, one):
        bodies = [point.shape1.GetBody(), point.shape2.GetBody()]

        if one in bodies:
            bodies.remove(one)
            return bodies[0]

        return None

    def Add(self, point):
        body = self.getOtherBody(point, self.ufomain.goal)
        if body:
            self.ufomain.ReachedGoal(body)

    def Persist(self, point):
        pass

    def Remove(self, point):
        pass

class UFOControls(object):
    gearw = None # wheel to control the gear joint for horizontal movement
    open  = None # open/close button
    world = None
    renderer = None
    grip  = None
    def __init__(self, ufogrip):
        self.world = ufogrip.world
        self.renderer = ufogrip.renderer
        self.grip = ufogrip

        ground = self.world.GetGroundBody()

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

        # gear joint -> gear wheel - horiz movement
        jd=box2d.b2GearJointDef() 
        jd.body1  = gearw
        jd.body2  = ufogrip.topc
        jd.joint1 = gearw_rj
        jd.joint2 = ufogrip.gearw_pj
        jd.ratio  = 10.0
        jd.maxMotorTorque = 0.0
        jd.motorSpeed = 0.0
        jd.enableMotor = True
        self.world.CreateJoint(jd).getAsType()

        # open/close button
        sd=box2d.b2PolygonDef() 
        sd.SetAsBox(2.5, 1.0)
        
        bd=box2d.b2BodyDef()
        bd.position.Set(-25.0, 10.0)
        self.open = open = self.world.CreateBody(bd)
        open.CreateShape(sd)

        Sprites(gearw, "Rollcats_bottom.png", 1.0, 1.0, 0.0, 0.0, self.renderer.toScreen)

    def move(self, amount):
        self.gearw.ApplyForce( box2d.b2Vec2(amount,0.0), box2d.b2Vec2(0.0,0.0))

    def draw(self):
        renderer = self.grip.renderer
        x, y = renderer.toScreen_v( self.open.GetWorldPoint( box2d.b2Vec2(-2.0,0.0) ) )
        renderer.DrawString( x,y, "Close" )

    def getBodyAtPoint(self, p, staticCheck=False):
        # Make a small box.
        aabb = box2d.b2AABB()
        d = box2d.b2Vec2(0.001, 0.001)
        aabb.lowerBound = p - d
        aabb.upperBound = p + d

        # Query the world for overlapping shapes.
        body = None
        k_maxCount = 10 # maximum amount of shapes to return

        (count, shapes) = self.world.Query(aabb, k_maxCount)
        for shape in shapes:
            shapeBody = shape.GetBody()
            if not staticCheck or (shapeBody.IsStatic() == False and shapeBody.GetMass() > 0.0):
                if shape.TestPoint(shapeBody.GetXForm(), p): # is it inside?
                    body = shapeBody
                    break
        
        return body

    def MouseDown(self, p):
        body = self.getBodyAtPoint(p)

        if not body:
            return

        if body == self.open:
            self.grip.toggleClosed()
        elif body == self.gearw:
            self.move(100.0)

class UFOGrip(object):
    extents = box2d.b2Vec2(3.0, 1.0) # size of grip pieces
    overlap = 0.125 # overlap for grip pieces
    lgrips, rgrips = [], [] # grip (grabber) bodies
    ljoints, rjoints=[], [] # grip joints
    force = 150.0    # closing/opening force
    isClosed = False # closing or not
    mainc = None # main control circle (at top of grabber)
    world = None
    renderer = None
    gearw_pj = None
    topcstartpos = box2d.b2Vec2(0.0, 30.0)
    def __init__(self, world, renderer):
        self.world = world
        self.renderer = renderer
        extents = self.extents
        overlap = self.overlap

        ground = self.world.GetGroundBody()
        # top control circle (topc)
        sd=box2d.b2CircleDef() 
        sd.radius = 0.5
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        bd.position = self.topcstartpos
        self.topc = topc = self.world.CreateBody(bd)
        topc.CreateShape(sd)
        topc.SetMassFromShapes()

        # main control circle (mainc)
        sd=box2d.b2CircleDef() 
        sd.radius = 0.5
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        bd.fixedRotation = True
        bd.position = topc.GetWorldCenter() - box2d.b2Vec2(0,10.0)
        self.mainc = mainc = self.world.CreateBody(bd)
        mainc.CreateShape(sd)
        mainc.SetMassFromShapes()

        Sprites(topc, "chain.png", 1.0, 10.0, 0.0, 0.0, self.renderer.toScreen, 0, mainc) # link
        Sprites(topc, "Rollcats_bottom.png", 1.0, 1.0, 0.0, 0.0, self.renderer.toScreen)
        Sprites(mainc, "Rollcats_bottom.png", 1.0, 1.0, 0.0, 0.0, self.renderer.toScreen)

        # prismatic joint for horizontal movement of control circle
        jd=box2d.b2PrismaticJointDef() 
        jd.Initialize(ground, topc, topc.GetWorldCenter(), box2d.b2Vec2(1.0, 0.0))
        jd.lowerTranslation = -18.0
        jd.upperTranslation = 25.0
        jd.enableLimit = True

        self.gearw_pj = self.world.CreateJoint(jd).getAsType()

        # left side stopper
        sd=box2d.b2CircleDef() 
        sd.radius = 0.5
        sd.density = 0.0

        bd=box2d.b2BodyDef()
        bd.position = self.topcstartpos + box2d.b2Vec2(-18.0,0.0)
        leftstopper = self.world.CreateBody(bd)
        leftstopper.CreateShape(sd)

        bd=box2d.b2BodyDef()
        bd.position = self.topcstartpos + box2d.b2Vec2(25.0,0.0)
        rightstopper = self.world.CreateBody(bd)
        rightstopper.CreateShape(sd)

        Sprites(leftstopper, "topbar.png", 10.0, 1.0, 0.0, 0.0, self.renderer.toScreen, 0, rightstopper) # link

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

        # create the grip itself
        tipsd=box2d.b2PolygonDef()
        tipsd.setVertices_tuple( [
                    (extents.x/2, extents.y/2), 
                    (-extents.x/2, 0.0),
                    (extents.x/2, -extents.y/2) ] )
        tipsd.density = 1.1

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(extents.x/2, extents.y/2) # SetAsBox takes half-width/height
        sd.density = 1.1

        start = mainc.GetWorldPoint(box2d.b2Vec2_zero)
        self.lgrips, self.ljoints=self.CreateGrips(True , sd, tipsd, extents, overlap, start, 3)
        self.rgrips, self.rjoints=self.CreateGrips(False, sd, tipsd, extents, overlap, start, 3)

    def CreateGrips(self, left, sd, tipsd, extents, overlap, startpos, count):
        grips  = []
        joints = []            
        
        step = -extents.x + overlap

        jd=box2d.b2RevoluteJointDef() 
        jd.enableLimit  = True

        ###test###
        jd.maxMotorTorque = 800.0
        jd.motorSpeed = 0.0
        jd.enableMotor = True
        ###test###

        jd.lowerAngle   = 0.2 * box2d.b2_pi  #36 degrees (left)
        jd.upperAngle   = 0.4 * box2d.b2_pi  #72 degrees (down)

        if left:
            jd.localAnchor1 = box2d.b2Vec2(-extents.x/2, 0)
            jd.localAnchor2 = box2d.b2Vec2( extents.x/2, 0)
        else: 
            jd.localAnchor1 = box2d.b2Vec2( extents.x/2, 0)
            jd.localAnchor2 = box2d.b2Vec2(-extents.x/2, 0)
            jd.lowerAngle, jd.upperAngle=-jd.upperAngle, -jd.lowerAngle #swap, negative
            step = -step

            for i in xrange(tipsd.vertexCount):
                v = -tipsd.getVertex(i)
                tipsd.setVertex(i,v.x,v.y)

        bd=box2d.b2BodyDef()
        bd.position = startpos
        bd.angularDamping = 0.0
        bd.linearDamping = 0.0

        for i in xrange(count):
            grips.append(self.world.CreateBody(bd))
            grip = grips[-1]

            if i==count-1:
                grip.CreateShape(tipsd)
                if left:
                    Sprites(grip, "grip-tip.png", extents.x, extents.y, 0.0, 0.0, self.renderer.toScreen, 180)
                else:
                    Sprites(grip, "grip-tip.png", extents.x, extents.y, 0.0, 0.0, self.renderer.toScreen)
            else:
                grip.CreateShape(sd)
                Sprites(grip, "grip-piece.png", extents.x, extents.y, 0.0, 0.0, self.renderer.toScreen)

            grip.SetMassFromShapes()

            # left grip 1-2 revolute joint
            if i==0:
                jd.localAnchor1 = box2d.b2Vec2(-overlap, 0)
                jd.body1 = self.mainc
                Sprites(grip, "grip-piece.png", extents.x, extents.y, 0.0, 0.0, self.renderer.toScreen)
            else:
                jd.localAnchor1 = box2d.b2Vec2(-extents.x/2, 0)
                jd.body1 = grips[-2]

            if not left:
                jd.localAnchor1.x = -jd.localAnchor1.x

            jd.body2 = grip
            joints.append( self.world.CreateJoint(jd).getAsType() )
            
            bd.position.x += step

        return grips, joints

    def moveToward(self, joint, angle):
        #print "Current angle: %f Desired angle: %f"%(joint.GetJointAngle() * 180.0/box2d.b2_pi, angle * 180.0/box2d.b2_pi)
        angleError = joint.GetJointAngle() - angle
        gain = 1.0
        joint.SetMotorSpeed(-gain * angleError)

    def Step(self):
        # big problem with the grip is that eventually the torque causes
        # a rotation at the base (top) of the grip itself, which makes it
        # flip around itself! all the things below are tests to see if there's
        # a way around it...
        if self.isClosed:
            closing_speed=1.0
            speed=closing_speed
            for joint in self.ljoints[1:]:
                joint.SetMotorSpeed(speed)
            for joint in self.rjoints[1:]:
                joint.SetMotorSpeed(-speed)
        else:
            for joint in self.ljoints[1:]:
                self.moveToward(joint, -0.4 * box2d.b2_pi)
            for joint in self.rjoints[1:]:
                self.moveToward(joint,  0.4 * box2d.b2_pi)

    def toggleClosed(self):
        self.isClosed = not self.isClosed
     
    def draw(self):
        return

        renderer = self.renderer

        # draw the top track
        tc = self.topcstartpos
        color=(255,0,127)
        self.drawLinks(p1, p2, color) 

        # draw a chain from the top control circle to the grip
        p3 = renderer.toScreen_v( self.topc.GetWorldPoint(box2d.b2Vec2_zero) )
        p4 = renderer.toScreen_v( self.mainc.GetWorldPoint(box2d.b2Vec2_zero) )
        color=(255,255,255)
        self.drawLinks(p1, p2, color)

    def disassembleJohnnyFive(self):
        for joint in self.ljoints+self.rjoints:
            self.world.DestroyJoint(joint)
        self.ljoints, self.rjoints = [], []

    def ropeExtend(self, amount=0.1):
        self.ropejd.length += amount

        if self.ropejd.length < 1.0:
            self.ropejd.length = 1.0

        self.world.DestroyJoint(self.ropej)
        self.ropej  = self.world.CreateJoint(self.ropejd).getAsType() 

class Sprites(object):
    # A bit of inspiration from the RollCats code :) Thanks!
    sprites = []
    instances = []
    sprite = None
    isLink = False
    def __init__(self, body, imageName, imageWidthMeters, imageHeightMeters, imageOffsetXMeters, imageOffsetYMeters, worldToScreenFunction, baseangle=0.0, body2=None):
        super(Sprites, self).__init__()

        # Save a copy of the screen's rectangle
        self.w2s = worldToScreenFunction
        self.body = body
        if body2:
            self.body2 = body2
            self.isLink = True
        self.imageName      =imageName
        self.imageDimensions= (imageWidthMeters, imageHeightMeters)
        self.offsetX        = imageOffsetXMeters
        self.offsetY        = imageOffsetYMeters
        self.baseAngle = baseangle
        self.reload()

        # get the dimensions of the image on the screen
        newWidth = abs( self.w2s( self.imageDimensions )[0] - self.w2s( (0,0) )[0])
        newHeight =abs( self.w2s( self.imageDimensions )[1] - self.w2s( (0,0) )[1])
        
        xy = self.w2s( (self.offsetX, self.offsetY) )
        self.sprite = rabbyt.Sprite(texture=imageName, shape=(-newWidth/2,newHeight/2,newWidth/2,-newHeight/2), xy=xy)
        Sprites.instances.append(self)
        Sprites.sprites.append(self.sprite)

    def reload(self):
        if not self.sprite: return
        if self.isLink: 
            self.updateLink()
            return
        newWidth = abs( self.w2s( self.imageDimensions )[0] - self.w2s( (0,0) )[0])
        newHeight =abs( self.w2s( self.imageDimensions )[1] - self.w2s( (0,0) )[1])
        self.sprite.shape=(-newWidth/2,newHeight/2,newWidth/2,-newHeight/2)

    def update(self):
        if not self.body: return
        if self.isLink: 
            self.updateLink()
            return
        angle = self.body.GetAngle()*180.0/box2d.b2_pi + self.baseAngle
        pos = self.body.GetWorldPoint( box2d.b2Vec2_zero )
        xy = self.w2s( (pos.x+self.offsetX, pos.y+self.offsetY) )
        self.sprite.x, self.sprite.y = xy
        self.sprite.rot = angle

    def updateLink(self):
        self.isLink = True
        p1 = self.body.GetWorldCenter()
        p2 = self.body2.GetWorldCenter()
        line = p2 - p1
        dist = line.Normalize()
        midpoint = p1 + 0.5*dist*line

        if p1.y - p2.y > box2d.FLT_EPSILON:
            self.sprite.rot = atan( (p2.x-p1.x) / (p1.y-p2.y))*180.0/box2d.b2_pi
        else:
            self.sprite.rot = 0

        if self.sprite.rot == 0:
            # okay, this is only a temporary fix
            newWidth = abs( self.w2s( (dist, self.imageDimensions[1]) )[0] - self.w2s( (0,0) )[0])
            newHeight =abs( self.w2s( (dist, self.imageDimensions[1]) )[1] - self.w2s( (0,0) )[1])
        else:
            newWidth = abs( self.w2s( (self.imageDimensions[0], dist) )[0] - self.w2s( (0,0) )[0])
            newHeight =abs( self.w2s( (self.imageDimensions[0], dist) )[1] - self.w2s( (0,0) )[1])
        self.sprite.shape=(-newWidth/2,newHeight/2,newWidth/2,-newHeight/2)
        self.sprite.x, self.sprite.y = self.w2s( (midpoint.x, midpoint.y) )

class UFOCatcher (Framework):
    name="UFOCatcher"
    stackheight = 5
    objects = []
    contactListener = None
    goal = None
    removeList = []
    grip = None
    drawList = []
    imageZoom=0.0 #cached image zoom
    image = None
    def ReachedGoal(self, body):
        if body not in self.removeList:
            print "Reached goal!"
            self.objects.remove(body)
            self.removeList.append(body)

    def __init__(self):
        self.viewCenter = 10.0 * box2d.b2Vec2(30.0, 40.0)
        self.viewZoom = 10.0

        super(UFOCatcher, self).__init__()
    
        self.renderer = self.debugDraw
        self.lastZoom = self.renderer.viewZoom
        self.lastCenter=self.renderer.viewCenter.tuple()
        self.lastCenter_s=self.renderer.toScreen( self.lastCenter )
        self.contactListener = UFOContactListener(self)
        self.world.SetContactListener(self.contactListener)

        # ground
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        Sprites(ground, "ground.png", 100.0, 20.0, 0.0, 0.0, self.renderer.toScreen)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)

        # left side wall
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 0.0)
        wall = self.world.CreateBody(bd)
        Sprites(wall, "wall.png", 1.0, 10.0, -15.0, 5.0, self.renderer.toScreen)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(-15.0, 5.0), 0)
        wall.CreateShape(sd)

        # right side wall
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 0.0)
        wall = self.world.CreateBody(bd)
        Sprites(wall, "wall.png", 1.0, 10.0, 15.0, 5.0, self.renderer.toScreen)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 5.0, box2d.b2Vec2(15.0, 5.0), 0)
        wall.CreateShape(sd)

        # goal (base)
        bd=box2d.b2BodyDef()
        bd.position.Set(22.0, 0.0)
        self.goal = goal = self.world.CreateBody(bd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(5.0, 1.0)
        goal.CreateShape(sd)
        Sprites(goal, "goal.png", 10.6, 5.0, 0.0, 1.0, self.renderer.toScreen)

        # goal walls
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.25, 1.5, box2d.b2Vec2(-5.0, 2.0), 0)
        goal.CreateShape(sd)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(0.25, 1.5, box2d.b2Vec2(5.0, 2.0), 0)
        goal.CreateShape(sd)

        # create the grip
        self.grip = UFOGrip(self.world, self.renderer)

        # create the controls
        self.controls = UFOControls(self.grip)

        # list the objects to draw
        self.drawList.append(self.grip)
        self.drawList.append(self.controls)

        # make a stack to grab from
        sd=box2d.b2CircleDef()
        sd.radius = 1.0
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        
        self.debugDraw.DrawSolidCircle = lambda a,b,c,d: False #DrawSolidCircle(self, center_v, radius, axis, color): 
        self.debugDraw.DrawSolidPolygon = lambda a,b,c: False #DrawSolidPolygon(self, in_vertices, vertexCount, color):

        for y in xrange(self.stackheight):
            bd.position.Set(0.0, 2.0 + 3.0 * y)
            body = self.world.CreateBody(bd)

            Sprites(body, "rollcat_assembly_required.png", 2.0, 2.0, 0.0, 0.0, self.renderer.toScreen)

            self.objects.append( body )
            self.objects[-1].CreateShape(sd)
            self.objects[-1].SetMassFromShapes()

    def Step(self, settings):
        rabbyt.clear()

        for sprite in Sprites.instances:
            sprite.update()

        rnd = self.renderer

        rabbyt.render_unsorted(Sprites.sprites)

        if rnd.viewZoom != self.lastZoom:
            for sprite in Sprites.instances:
                sprite.reload()
            self.lastZoom=rnd.viewZoom

        rnd.DrawString(5, rnd.textLine, "Let's ufo catch!")
        rnd.textLine += 15

        for body in self.removeList:
            self.world.DestroyBody(body)
        self.removeList = []

        # draw the sprites
        screen = rnd.surface

        self.grip.Step()

        displayList = []

        for object in self.drawList:
            object.draw()

        super(UFOCatcher, self).Step(settings)
        
    def MouseDown(self, p):
        self.controls.MouseDown(p)

    def Keyboard(self, key):
        if key == K_w:
            self.grip.ropeExtend(-0.2)
        elif key == K_s:
            self.grip.ropeExtend( 0.2)
        elif key == K_a:
            self.controls.move( 100.0 )
        elif key == K_d:
            self.controls.move(-100.0 )
        elif key == K_c:
            self.grip.toggleClosed()
        elif key == K_q:
            self.grip.disassembleJohnnyFive()

if __name__=="__main__":
    main(UFOCatcher)
