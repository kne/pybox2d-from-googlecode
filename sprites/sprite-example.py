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
"""
9/15/2008
Just a basic example of how to use pybox2d with pygame and rabbyt for sprites.
Obviously derived from the main testbed, but does not require the GUI.

Todo: fix object picking. Why's it not working now?

-kne
"""

import pygame
import rabbyt
import Box2D2 as box2d
import rabbyt
import os.path

from pygame.locals import *
from math import sqrt, sin, cos, atan

rabbyt.data_directory = os.path.dirname(__file__)

class fwSettings(object):
    hz=60.0
    velocityIterations=10
    positionIterations=8
    enableWarmStarting=True
    enableTOI=True
    pause=False
    singleStep=False
    pointSize=2.5 # pixel radius for drawing points

class fwDestructionListener(box2d.b2DestructionListener):
    """
    The destruction listener callback:
    "SayGoodbye" is called when a joint is deleted.
    """
    test = None
    def __init__(self):
        super(fwDestructionListener, self).__init__()

    def SayGoodbye(self, joint):
        if self.test.mouseJoint:
            self.test.mouseJoint=None
        else:
            self.test.JointDestroyed(joint)

class fwBoundaryListener(box2d.b2BoundaryListener):
    """
    The boundary listener callback:
    Violation is called when the specified body leaves the world AABB.
    """
    test = None
    def __init__(self):
        super(fwBoundaryListener, self).__init__()

    def Violation(self, body):
        # So long as it's not the user-created bomb, let the test know that
        # the specific body has left the world AABB
        if self.test.bomb != body:
            self.test.BoundaryViolated(body)

class fwContactTypes:
    """
    Acts as an enum, holding the types necessary for contacts:
    Added, persisted, and removed
    """
    contactUnknown = 0
    contactAdded = 1
    contactPersisted = 2
    contactRemoved = 3

class fwContactPoint:
    """
    Structure holding the necessary information for a contact point.
    All of the information is copied from the contact listener callbacks.
    """
    shape1 = None
    shape2 = None
    normal = None
    position = None
    velocity = None
    id  = None
    state = 0

class fwContactListener(box2d.b2ContactListener):
    """
    Handles all of the contact states passed in from Box2D.
    """
    def __init__(self):
        super(fwContactListener, self).__init__()

    def Add(self, point):
        pass

    def Persist(self, point):
        pass

    def Remove(self, point):
        pass

class Game(object):
    """
    The main game framework.
    It handles basically everything:
    * The initialization of pygame, Box2D
    * Contains the main loop
    * Handles all user input.

    You should derive your class from this one to implement your own tests.
    See test_Empty.py or any of the other tests for more information.
    """
    name = "None"

    # Box2D-related
    worldAABB = box2d.b2AABB()
    world = None
    bomb = None
    mouseJoint = None
    settings = fwSettings()
    bombSpawning = False
    bombSpawnPoint = None
    mouseWorld = None

    # Box2D-callbacks
    destructionListener = None
    boundaryListener = None
    contactListener = None

    # Screen-related
    viewCenter = 10.0 * box2d.b2Vec2(30.0, 40.0)
    viewZoom = 10.0
    viewOffset = None
    screenSize = None
    rMouseDown = False
    fps = 0

    def __init__(self):
        # Pygame Initialization
        pygame.init()

        caption= "pyBox2D Sprite Example"
        pygame.display.set_caption(caption)

        windowSize = (640,480)
        self.screen = pygame.display.set_mode( windowSize, pygame.OPENGL | pygame.DOUBLEBUF )
        rabbyt.set_viewport(windowSize)
        rabbyt.set_default_attribs()
        
        self.screenSize = box2d.b2Vec2(*windowSize)

        # Box2D Initialization
        self.worldAABB.lowerBound.Set(-200.0, -100.0)
        self.worldAABB.upperBound.Set( 200.0, 200.0)
        gravity = box2d.b2Vec2(0.0, -10.0)

        doSleep = True
        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)
        self.destructionListener = fwDestructionListener()
        self.boundaryListener = fwBoundaryListener()
        self.contactListener = fwContactListener()

        self.destructionListener.test = self
        self.boundaryListener.test = self
        
        self.world.SetDestructionListener(self.destructionListener)
        self.world.SetBoundaryListener(self.boundaryListener)
        self.world.SetContactListener(self.contactListener)

        self.updateCenter()

    def updateCenter(self):
        """
        Updates the view offset based on the center of the screen.
        """
        self.viewOffset = self.viewCenter - self.screenSize/2
        print self.viewCenter, self.viewOffset

    def toWorld(self, x, y):
        """
        Return a b2Vec2 in world coordinates of the passed in screen coordinates x, y
        """
        print self.viewOffset, self.viewZoom
        return box2d.b2Vec2((x + self.viewOffset.x) / self.viewZoom, ((self.screenSize.y - y + self.viewOffset.y) / self.viewZoom))

    def toScreen_v(self, pt):
        """
        Input:  pt - a b2Vec2 in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """
        return (int((pt.x * self.viewZoom) - self.viewOffset.x), int((pt.y * self.viewZoom) - self.viewOffset.y))
    def toScreen(self, pt):
        """
        Input:  (x, y) - a tuple in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """
        return ((pt[0] * self.viewZoom) - self.viewOffset.x, ((pt[1] * self.viewZoom) - self.viewOffset.y))
    def scaleValue(self, value):
        """
        Input: value - unscaled value
        Output: scaled value according to the view zoom ratio
        """
        return value/self.viewZoom

    def checkEvents(self):
        """
        Check for pygame events (mainly keyboard/mouse events).
        """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                print event.pos
                p = self.toWorld(*event.pos)
                if event.button == 1: # left
                    mods = pygame.key.get_mods()
                    if mods & KMOD_LSHIFT:
                        self.ShiftMouseDown( p )
                    else:
                        self.MouseDown( p )
                elif event.button == 2: #middle
                    pass
                elif event.button == 3: #right
                    self.rMouseDown = True
                elif event.button ==4:
                    self.viewZoom *= 1.1
                    for sprite in Sprites.instances:
                        sprite.reload()
                elif event.button == 5:
                    self.viewZoom /= 1.1
                    for sprite in Sprites.instances:
                        sprite.reload()
            elif event.type == MOUSEBUTTONUP:
                p = self.toWorld(*event.pos)
                if event.button == 3: #right
                    self.rMouseDown = False
                else:
                    self.MouseUp(p)
            elif event.type == MOUSEMOTION:
                p = self.toWorld(*event.pos)

                self.MouseMove(p)

                if self.rMouseDown:
                    self.viewCenter -= box2d.b2Vec2(event.rel[0], -event.rel[1])
                    self.updateCenter()

        return True

    def run(self):
        """
        Main loop.

        Continues to run while checkEvents indicates the user has 
        requested to quit.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.checkEvents()

            rabbyt.set_time(pygame.time.get_ticks())
            rabbyt.scheduler.pump()

            # Check keys that should be checked every loop (not only on initial keydown)
            self.CheckKeys()

            # Run the simulation loop 
            self.Step(self.settings)

            pygame.display.flip()
            clock.tick(self.settings.hz)
            self.fps = clock.get_fps()

    def Step(self, settings):
        """
        The main physics step.

        Takes care of physics drawing (callbacks are executed after the world.Step() )
        and drawing additional information.
        """

        # Don't do anything if the setting's Hz are <= 0
        if settings.hz > 0.0:
            timeStep = 1.0 / settings.hz
        else:
            timeStep = 0.0
        
        # If paused, display so
        if settings.pause:
            if settings.singleStep:
                settings.singleStep=False
            else:
                timeStep = 0.0

        # Set the other settings that aren't contained in the flags
        self.world.SetWarmStarting(settings.enableWarmStarting)
    	self.world.SetContinuousPhysics(settings.enableTOI)

        # Tell Box2D to step
        self.world.Step(timeStep, settings.velocityIterations, settings.positionIterations)
        self.world.Validate()

        # If the bomb is frozen, get rid of it.
        if self.bomb and self.bomb.IsFrozen():
            self.removeSprite(self.bomb)
            self.world.DestroyBody(self.bomb)
            self.bomb = None

    def _Keyboard_Event(self, key):
        """
        Internal keyboard event, don't override this.

        Checks for the initial keydown of the basic testbed keys. Passes the unused
        ones onto the test via the Keyboard() function.
        """
        if key==K_z:
            # Zoom in
            self.viewZoom = min(1.1 * self.viewZoom, 20.0)
            self.updateCenter()
        elif key==K_x:
            # Zoom out
            self.viewZoom = max(0.9 * self.viewZoom, 0.02)
            self.updateCenter()
        elif key==K_SPACE:
            # Launch a bomb
            self.LaunchRandomBomb()
        else:
            # Inform the test of the key press
            self.Keyboard(key)
        
    def ShiftMouseDown(self, p):
        """
        Indicates that there was a left click at point p (world coordinates) with the
        left shift key being held down.
        """
        self.mouseWorld = p

        if self.mouseJoint != None:
            return

        self.SpawnBomb(p)

    def MouseDown(self, p):
        """
        Indicates that there was a left click at point p (world coordinates)
        """
        print p
        if self.mouseJoint != None:
            return

        # Create a mouse joint on the selected body (assuming it's dynamic)

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
            if shapeBody.IsStatic() == False and shapeBody.GetMass() > 0.0:
                if shape.TestPoint(shapeBody.GetXForm(), p): # is it inside?
                    body = shapeBody
                    break
        
        if body:
            md = box2d.b2MouseJointDef()
            md.body1   = self.world.GetGroundBody()
            md.body2   = body
            md.target  = p
            md.maxForce= 1000.0 * body.GetMass()
            self.mouseJoint = self.world.CreateJoint(md).getAsType()
            body.WakeUp()

    def MouseUp(self, p):
        """
        Left mouse button up.
        """     
        if self.mouseJoint:
            self.world.DestroyJoint(self.mouseJoint)
            self.mouseJoint = None

        if self.bombSpawning:
            self.CompleteBombSpawn(p)

    def MouseMove(self, p):
        """
        Mouse moved to point p, in world coordinates.
        """
        self.mouseWorld = p
        if self.mouseJoint:
            self.mouseJoint.SetTarget(p)

    def SpawnBomb(self, worldPt):
        """
        Begins the slingshot bomb by recording the initial position.
        Once the user drags the mouse and releases it, then 
        CompleteBombSpawn will be called and the actual bomb will be
        released.
        """

        self.bombSpawnPoint = worldPt.copy()
        self.bombSpawning = True

    def CompleteBombSpawn(self, p):
        """
        Create the slingshot bomb based on the two points
        (from the worldPt passed to SpawnBomb to p passed in here)
        """
        if not self.bombSpawning: 
            return
        multiplier = 30.0
        vel  = self.bombSpawnPoint - p
        vel *= multiplier
        self.LaunchBomb(self.bombSpawnPoint, vel)
        self.bombSpawning = False

    def LaunchBomb(self, position, velocity):
        """
        A bomb is a simple circle which has the specified position and velocity.
        """
        if self.bomb:
            self.removeSprite(self.bomb)
            self.world.DestroyBody(self.bomb)
            self.bomb = None

        bd = box2d.b2BodyDef()
        bd.allowSleep = True
        bd.position = position
        bd.isBullet = True
        self.bomb = self.world.CreateBody(bd)
        self.bomb.SetLinearVelocity(velocity)

        sd = box2d.b2CircleDef()
        sd.radius = 0.3
        sd.density = 20.0
        sd.restitution = 0.1
        Sprites(self.bomb, "rollcat_assembly_required.png", 0.6, 0.6, 0.0, 0.0, self.toScreen)

        minV = position - box2d.b2Vec2(0.3,0.3)
        maxV = position + box2d.b2Vec2(0.3,0.3)

        aabb = box2d.b2AABB()
        aabb.lowerBound = minV
        aabb.upperBound = maxV

        if self.world.InRange(aabb):
            self.bomb.CreateShape(sd)
            self.bomb.SetMassFromShapes()

    def LaunchRandomBomb(self):
        """
        Create a new bomb and launch it at the testbed.
        """
        p = box2d.b2Vec2( box2d.b2Random(-15.0, 15.0), 30.0 )
        v = -5.0 * p
        self.LaunchBomb(p, v)
     
    def CheckKeys(self):
        """
        Check the keys that are evaluated on every main loop iteration.
        I.e., they aren't just evaluated when first pressed down
        """

        pygame.event.pump()
        self.keys = keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.viewCenter.x -= 0.5
            self.updateCenter()
        elif keys[K_RIGHT]:
            self.viewCenter.x += 0.5
            self.updateCenter()
        if keys[K_UP]:
            self.viewCenter.y += 0.5
            self.updateCenter()
        elif keys[K_DOWN]:
            self.viewCenter.y -= 0.5
            self.updateCenter()

        if keys[K_HOME]:
            self.viewZoom = 1.0
            self.viewCenter.Set(0.0, 20.0)
            self.updateCenter()

    def removeSprite(self, body):
        for instance in Sprites.instances:
            if instance.body == body:
                index = Sprites.instances.index(instance)

                Sprites.instances.remove(instance)
                del Sprites.sprites[index]
                return

    def BoundaryViolated(self, body):
        """
        Callback indicating 'body' has left the world AABB.
        """
        self.removeSprite(body)

    # These should be implemented in the subclass: (Step() also if necessary)
    def JointDestroyed(self, joint):
        """
        Callback indicating 'joint' has been destroyed.
        """
        pass

    def Keyboard(self, key):
        """
        Callback indicating 'key' has been pressed down.
        The key is from pygame.locals.K_*:

         from pygame.locals import *
         ...
         if key == K_z:
             pass
        """
        pass

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

class SimpleExample(Game):
    stackheight = 5
    objects = []
    drawList = []
    def __init__(self):
        super(SimpleExample, self).__init__()
    
        # ground
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        ground = self.world.CreateBody(bd)
        Sprites(ground, "ground.png", 100.0, 20.0, 0.0, 0.0, self.toScreen)

        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)

        # make a stack to grab from
        sd=box2d.b2CircleDef()
        sd.radius = 1.0
        sd.density = 1.0

        bd=box2d.b2BodyDef()
        
        for y in xrange(self.stackheight):
            bd.position.Set(0.0, 2.0 + 3.0 * y)
            print "position", y, bd.position
            body = self.world.CreateBody(bd)

            Sprites(body, "rollcat_assembly_required.png", 2.0, 2.0, 0.0, 0.0, self.toScreen)

            self.objects.append( body )
            self.objects[-1].CreateShape(sd)
            self.objects[-1].SetMassFromShapes()
            
    def Step(self, settings):
        rabbyt.clear()

        for sprite in Sprites.instances:
            sprite.update()

        rabbyt.render_unsorted(Sprites.sprites)

        super(SimpleExample, self).Step(settings)
        
    def Keyboard(self, key):
        pass

if __name__=="__main__":
    game = SimpleExample()
    game.run()
