#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pygooglecode.com)
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
Keys:
    F1     - toggle menu (can greatly improve fps)
    F5     - save state
    F7     - load state

    Space  - shoot projectile
    Z/X    - zoom
    Escape - quit

Other keys can be set by the individual test

Mouse:
    Left click  - select/drag body (creates mouse joint)
    Right click - pan
    Shift+Left  - drag to create a directional projectile
    Scroll      - zoom

You can easily add your own tests based on test_empty.
"""
import pygame
from Box2D import *
from pygame.locals import *
from settings import fwSettings
from pgu import gui

# Use psyco if available
try:
    import psyco
    psyco.full()
except ImportError:
    pass

class fwDestructionListener(b2DestructionListener):
    """
    The destruction listener callback:
    "SayGoodbye" is called when a joint or shape is deleted.
    """
    test = None
    def __init__(self):
        super(fwDestructionListener, self).__init__()

    def SayGoodbye(self, object):
        if isinstance(object, b2Joint):
            if self.test.mouseJoint==object:
                self.test.mouseJoint=None
            else:
                self.test.JointDestroyed(object)
        elif isinstance(object, b2Shape):
            self.test.ShapeDestroyed(object)

class fwContactTypes:
    """
    Acts as an enum, holding the types necessary for contacts:
    Added, persisted, and removed
    """
    contactUnknown   = 0
    contactAdded     = 1
    contactPersisted = 2
    contactRemoved   = 3

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

class fwContactListener(b2ContactListener):
    """
    Handles all of the contact states passed in from 

    """
    test = None
    def __init__(self):
        super(fwContactListener, self).__init__()

    def handleCall(self, state, point):
        if not self.test: return

        cp          = fwContactPoint()
        cp.shape1   = point.shape1
        cp.shape2   = point.shape2
        cp.position = point.position.copy()
        cp.normal   = point.normal.copy()
        cp.id       = point.id
        cp.state    = state
        self.test.points.append(cp)

    def Add(self, point):
        self.handleCall(fwContactTypes.contactAdded, point)

    def Persist(self, point):
        self.handleCall(fwContactTypes.contactPersisted, point)

    def Remove(self, point):
        self.handleCall(fwContactTypes.contactRemoved, point)

    def PreSolve(self, point, old_manifold):
        pass # TODO
        #self.handleCall(fwContactTypes.contactPreSolve, point)
        #print point

class fwDebugDraw(b2DebugDraw):
    """
    This debug draw class accepts callbacks from Box2D (which specifies what to draw)
    and handles all of the rendering.

    If you are writing your own game, you likely will not want to use debug drawing.
    Debug drawing, as its name implies, is for debugging.
    """
    circle_segments = 16
    surface = None
    viewZoom = 1.0
    viewCenter = None
    viewOffset = None
    width, height = 0, 0
    def __init__(self): super(fwDebugDraw, self).__init__()
    def _setValues(self, viewZoom, viewCenter, viewOffset, width, height):
        """
        Sets the view zoom, center, offset, and width and height of the screen such that access 
        to the main window is unnecessary.
        """
        self.viewZoom=viewZoom
        self.viewCenter=viewCenter
        self.viewOffset=viewOffset
        self.width = width 
        self.height = height

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size/self.viewZoom, color, drawwidth=0)
        
    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        points = [self.to_screen(p) for p in [
                    (aabb.lowerBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.lowerBound.y ),
                    (aabb.upperBound.x, aabb.upperBound.y ),
                    (aabb.lowerBound.x, aabb.upperBound.y ),
                    ] ]
        
        pygame.draw.aalines(self.surface, color, True, points)

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        pygame.draw.aaline(self.surface, color.bytes, self.to_screen(p1), self.to_screen(p2))

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        k_axisScale = 0.4
        p2 = self.to_screen(p1 + k_axisScale * xf.R.col1)
        p3 = self.to_screen(p1 + k_axisScale * xf.R.col2)
        p1 = self.to_screen(p1)

        pygame.draw.aaline(self.surface, (255,0,0), p1, p2)
        pygame.draw.aaline(self.surface, (0,255,0), p1, p3)

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        radius *= self.viewZoom
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.to_screen(center)
        pygame.draw.circle(self.surface, color.bytes, center, radius, drawwidth)

    def DrawSolidCircle(self, center_v, radius, axis, color):
        """
        Draw a solid circle given the b2Vec2 center_v, radius, axis of orientation and color.
        """
        radius *= self.viewZoom
        if radius < 1: radius = 1
        else: radius = int(radius)

        center = self.to_screen(center_v)
        pygame.draw.circle(self.surface, (color/2).bytes+[127], center, radius, 0)

        pygame.draw.circle(self.surface, color.bytes, center, radius, 1)

        p = radius * axis
        pygame.draw.aaline(self.surface, (255,0,0), center, (center[0] - p.x, center[1] + p.y)) 

    def DrawPolygon(self, in_vertices, vertexCount, color):
        """
        Draw a wireframe polygon given the world vertices in_vertices (tuples) with the specified color.
        """
        if len(in_vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes, self.to_screen(in_vertices[0]), self.to_screen(in_vertices[1]))
        else:
            pygame.draw.polygon(self.surface, color.bytes, [self.to_screen(v) for v in in_vertices], 1)
        
    def DrawSolidPolygon(self, in_vertices, vertexCount, color):
        """
        Draw a filled polygon given the world vertices in_vertices (tuples) with the specified color.
        """
        if len(in_vertices) == 2:
            pygame.draw.aaline(self.surface, color.bytes, self.to_screen(in_vertices[0]), self.to_screen(in_vertices[1]))
        else:
            vertices = [self.to_screen(v) for v in in_vertices]
            pygame.draw.polygon(self.surface, (color/2).bytes+[127], vertices, 0)
            pygame.draw.polygon(self.surface, color.bytes, vertices, 1)

    def to_screen(self, pt):
        """
        Input:  (x, y) - a tuple in world coordinates
        Output: (x, y) - a tuple in screen coordinates
        """
        return ((pt[0] * self.viewZoom) - self.viewOffset.x, self.height - ((pt[1] * self.viewZoom) - self.viewOffset.y))
    def scaleValue(self, value):
        """
        Input: value - unscaled value
        Output: scaled value according to the view zoom ratio
        """
        return value/self.viewZoom

class fwGUI(gui.Table):
    """
    Deals with the initialization and changing the settings based on the GUI 
    controls. Callbacks are not used, but the checkboxes and sliders are polled
    by the main loop.
    """
    checkboxes =( ("Warm Starting", "enableWarmStarting"), 
                  ("Time of Impact", "enableContinuous"), 
                  ("Draw", None),
                  ("Shapes", "drawShapes"), 
                  ("Joints", "drawJoints"), 
                  ("AABBs", "drawAABBs"), 
                  ("Pairs", "drawPairs"), 
                  ("Contact Points", "drawContactPoints"), 
                  ("Contact Normals", "drawContactNormals"), 
                  ("Center of Masses", "drawCOMs"), 
                  ("Statistics", "drawStats"),
                  ("FPS", "drawFPS"),
                  ("Control", None),
                  ("Pause", "pause"),
                  ("Single Step", "singleStep") )
    form = None

    def __init__(self,settings, **params):
        # The framework GUI is just basically a HTML-like table.
        # There are 2 columns, and basically everything is right-aligned.
        gui.Table.__init__(self,**params)
        self.form=gui.Form()

        fg = (255,255,255)

        # "Hertz"
        self.tr()
        self.td(gui.Label("F1: Toggle Menu",color=(255,0,0)),align=1,colspan=2)

        self.tr()
        self.td(gui.Label("Hertz",color=fg),align=1,colspan=2)

        # Hertz slider
        self.tr()
        e = gui.HSlider(settings.hz,5,200,size=20,width=100,height=16,name='hz')
        self.td(e,colspan=2,align=1)

        # "Vel Iters"
        self.tr()
        self.td(gui.Label("Vel Iters",color=fg),align=1,colspan=2)

        # Velocity Iterations slider (min 1, max 500)
        self.tr()
        e = gui.HSlider(settings.velocityIterations,1,500,size=20,width=100,height=16,name='velIters')
        self.td(e,colspan=2,align=1)

        # "Pos Iters"
        self.tr()
        self.td(gui.Label("Pos Iters",color=fg),align=1,colspan=2)

        # Position Iterations slider (min 0, max 100)
        self.tr()
        e = gui.HSlider(settings.positionIterations,0,100,size=20,width=100,height=16,name='posIters')
        self.td(e,colspan=2,align=1)

        # Add each of the checkboxes.
        for text, variable in self.checkboxes:
            self.tr()
            if variable == None:
                # Checkboxes that have no variable (i.e., None) are just labels.
                self.td(gui.Label(text, color=fg), align=1, colspan=2)
            else:
                # Add the label and then the switch/checkbox
                self.td(gui.Label(text, color=fg), align=1)
                self.td(gui.Switch(value=getattr(settings, variable),name=variable))

    def updateGUI(self, settings):
        """
        Change all of the GUI elements based on the current settings
        """
        for text, variable in self.checkboxes:
            if not variable: continue
            if hasattr(settings, variable):
                self.form[variable].value = getattr(settings, variable)

        # Now do the sliders
        self.form['hz'].value       = settings.hz
        self.form['posIters'].value = settings.positionIterations
        self.form['velIters'].value = settings.velocityIterations

    def updateSettings(self, settings):
        """
        Change all of the settings based on the current state of the GUI.
        """
        for text, variable in self.checkboxes:
            if variable == None: continue
            setattr(settings, variable, self.form[variable].value)

        # Now do the sliders
        settings.hz = int(self.form['hz'].value)
        settings.positionIterations = int(self.form['posIters'].value)
        settings.velocityIterations = int(self.form['velIters'].value)

        # If we're in single-step mode, update the GUI to reflect that.
        if settings.singleStep:
            settings.pause=True
            self.form['pause'].value = True
            self.form['singleStep'].value = False

class QueryCallback(b2QueryCallback):
    def __init__(self): 
        super(QueryCallback, self).__init__()
        self.point = None
        self.fixture = None

    def ReportFixture(self, fixture):
        body = fixture.body
        if body.type == b2_dynamicBody:
            inside=fixture.TestPoint(self.point)
            if inside:
                self.fixture=fixture
                # We found the object, sto stop the query
                return False
        # Continue the query
        return True

class Framework(object):
    """
    The main testbed framework.
    It handles basically everything:
    * The initialization of pygame, Box2D
    * Contains the main loop
    * Handles all user input.

    You should derive your class from this one to implement your own tests.
    See test_Empty.py or any of the other tests for more information.
    """
    name = "None"

    # Box2D-related
    points             = []
    world              = None
    bomb               = None
    mouseJoint         = None
    settings           = fwSettings
    bombSpawning       = False
    bombSpawnPoint     = None
    mouseWorld         = None
    destroyList        = []

    # Box2D-callbacks
    destructionListener= None
    contactListener    = None
    debugDraw          = None

    # Screen/rendering-related
    _viewZoom          = 10.0
    _viewCenter        = None
    _viewOffset        = None
    screenSize         = None
    rMouseDown         = False
    textLine           = 30
    font               = None
    fps                = 0

    # GUI-related (PGU)
    gui_app   = None
    gui_table = None

    def __init__(self):
        # Box2D Initialization
        gravity = (0.0, -10.0)
        doSleep = True
        self.world = b2World(gravity, doSleep)

        self.destructionListener = fwDestructionListener()
        self.contactListener = fwContactListener()
        self.debugDraw = fwDebugDraw()

        self.destructionListener.test = self
        self.contactListener.test = self
        
        self.world.destructionListener=self.destructionListener
        self.world.contactListener=self.contactListener
        self.world.debugDraw=self.debugDraw

        # Pygame Initialization
        if fwSettings.onlyInit: # testing mode doesn't initialize pygame
            return

        pygame.init()

        caption= "Python Box2D Testbed - " + self.name
        pygame.display.set_caption(caption)

        self.screen = pygame.display.set_mode( (640,480) )
        self.debugDraw.surface = self.screen

        self.screenSize = b2Vec2(*self.screen.get_size())
        
        try:
            self.font = pygame.font.Font(None, 15)
        except IOError:
            try:
                self.font = pygame.font.Font("freesansbold.ttf", 15)
            except IOError:
                print "Unable to load default font or 'freesansbold.ttf'"
                print "Disabling text drawing."
                self.DrawString = lambda x,y,z: 0

        # GUI Initialization
        self.gui_app = gui.App()
        self.gui_table=fwGUI(self.settings)
        container = gui.Container(align=1,valign=-1)
        container.add(self.gui_table,0,0)
        self.gui_app.init(container)

        self.viewCenter = (0,10.0*20.0)

    def setCenter(self, value):
        """
        Updates the view offset based on the center of the screen.
        
        Tells the debug draw to update its values also.
        """
        if isinstance(value, b2Vec2):
            self._viewCenter = value.copy()
        elif isinstance(value, (list, tuple)):
            self._viewCenter = b2Vec2( *value )
        else:
            raise ValueError, 'Expected b2Vec2 or sequence'

        self._viewOffset = self._viewCenter - self.screenSize/2

        self.debugDraw._setValues(self.viewZoom, self.viewCenter, self.viewOffset, self.screenSize.x, self.screenSize.y)
    
    def setZoom(self, zoom):
        self._viewZoom = zoom
        self.debugDraw.viewZoom = zoom

    viewZoom   = property(lambda self: self._viewZoom, setZoom,
                           doc='Zoom factor for the display')
    viewCenter = property(lambda self: self._viewCenter, setCenter, 
                           doc='Screen center in camera coordinates')
    viewOffset = property(lambda self: self._viewOffset,
                           doc='The offset of the top-left corner of the screen')
        
    def checkEvents(self):
        """
        Check for pygame events (mainly keyboard/mouse events).
        Passes the events onto the GUI also.
        """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key)
            elif event.type == MOUSEBUTTONDOWN:
                p = self.ConvertScreenToWorld(*event.pos)
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
                elif event.button == 5:
                    self.viewZoom /= 1.1
            elif event.type == MOUSEBUTTONUP:
                p = self.ConvertScreenToWorld(*event.pos)
                if event.button == 3: #right
                    self.rMouseDown = False
                else:
                    self.MouseUp(p)
            elif event.type == MOUSEMOTION:
                p = self.ConvertScreenToWorld(*event.pos)

                self.MouseMove(p)

                if self.rMouseDown:
                    self.viewCenter -= (event.rel[0], -event.rel[1])

            self.gui_app.event(event) #Pass the event to the GUI

        return True

    def run(self):
        """
        Main loop.

        Continues to run while checkEvents indicates the user has 
        requested to quit.

        Updates the screen and tells the GUI to paint itself.
        """
        running = True
        clock = pygame.time.Clock()

        while running:
            running = self.checkEvents()
            self.screen.fill( (0,0,0) )

            # Check keys that should be checked every loop (not only on initial keydown)
            self.CheckKeys()

            # Run the simulation loop 
            self.SimulationLoop()

            if self.settings.drawMenu:
                self.gui_app.paint(self.screen)

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

            self.DrawStringCR("****PAUSED****", (200,0,0))

        # Set the flags based on what the settings show (uses a bitwise or mask)
        flag_info = [
            (settings.drawShapes,     b2DebugDraw.e_shapeBit),
            (settings.drawJoints,     b2DebugDraw.e_jointBit),
            (settings.drawAABBs,      b2DebugDraw.e_aabbBit),
            (settings.drawPairs,      b2DebugDraw.e_pairBit),
            (settings.drawCOMs,       b2DebugDraw.e_centerOfMassBit),
            ]

        flags = 0
        for setting, flag in flag_info:
            if setting:
                flags |= flag

        self.debugDraw.SetFlags(flags)

        # Set the other settings that aren't contained in the flags
        self.world.warmStarting=settings.enableWarmStarting
    	self.world.continuousPhysics=settings.enableContinuous

        # Reset the collision points
        self.points = []

        # Tell Box2D to step
        self.world.Step(timeStep, settings.velocityIterations, settings.positionIterations)
        self.world.ClearForces()
        self.world.DrawDebugData()

        # Destroy bodies that have left the world AABB (can be removed if not using pickling)
        for obj in self.destroyList:
            self.world.DestroyBody(obj)
        self.destroyList = []

        # If the bomb is frozen, get rid of it.
        if self.bomb and self.bomb.IsFrozen():
            self.world.DestroyBody(self.bomb)
            self.bomb = None

        # Take care of additional drawing (stats, fps, mouse joint, slingshot bomb, contact points)
        if settings.drawStats:
            self.DrawStringCR("proxies(max) = %d(%d), pairs(max) = %d(%d)" % (
                self.world.GetProxyCount(), b2_maxProxies, self.world.GetPairCount(), b2_maxPairs) )

            self.DrawStringCR("bodies/contacts/joints = %d/%d/%d" %
                (self.world.GetBodyCount(), self.world.GetContactCount(), self.world.GetJointCount()))

            self.DrawStringCR("hz %d vel/pos iterations %d/%d" %
                (settings.hz, settings.velocityIterations, settings.positionIterations))

            self.DrawStringCR("heap bytes = %d" % cvar.b2_byteCount)

        if settings.drawFPS:
            self.DrawStringCR("FPS %d" % self.fps)
        
        # If there's a mouse joint, draw the connection between the object and the current pointer position.
        if self.mouseJoint:
            body = self.mouseJoint.GetBody2()
            p1 = body.GetWorldPoint(self.mouseJoint.localAnchor)
            p2 = self.mouseJoint.target

            self.debugDraw.DrawPoint(p1, settings.pointSize, (0,1.0,0))
            self.debugDraw.DrawPoint(p2, settings.pointSize, (0,1.0,0))
            self.debugDraw.DrawSegment(p1, p2, (0.8,0.8,0.8))

        # Draw the slingshot bomb
        if self.bombSpawning:
            self.debugDraw.DrawPoint(self.bombSpawnPoint, settings.pointSize, (0,0,1.0))
            self.debugDraw.DrawSegment(self.bombSpawnPoint, self.mouseWorld, (0.8,0.8,0.8))

        # Draw each of the contact points in different colors.
        if self.settings.drawContactPoints:
            #k_impulseScale = 0.1
            k_axisScale = 0.3

            for point in self.points:
                if point.state == fwContactTypes.contactAdded:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, (0.3, 0.95, 0.3))
                elif point.state == fwContactTypes.contactPersisted:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, (0.3, 0.3, 0.95))
                elif point.state == fwContactTypes.contactRemoved:
                    self.debugDraw.DrawPoint(point.position, settings.pointSize, (0.95, 0.3, 0.3))
                #else: # elif point.state == fwContactTypes.contactPreSolve:
                #    pass

                if settings.drawContactNormals:
                    p1 = point.position
                    p2 = p1 + k_axisScale * point.normal
                    self.debugDraw.DrawSegment(p1, p2, (0.4, 0.9, 0.4))

    def _Keyboard_Event(self, key):
        """
        Internal keyboard event, don't override this.

        Checks for the initial keydown of the basic testbed keys. Passes the unused
        ones onto the test via the Keyboard() function.
        """
        if key==K_z:       # Zoom in
            self.viewZoom = min(1.1 * self.viewZoom, 20.0)
        elif key==K_x:     # Zoom out
            self.viewZoom = max(0.9 * self.viewZoom, 0.02)
        elif key==K_SPACE: # Launch a bomb
            self.LaunchRandomBomb()
        elif key==K_F1:    # Toggle drawing the menu
            self.settings.drawMenu = not self.settings.drawMenu
        else:              # Inform the test of the key press
            self.Keyboard(key)
        
    def ShiftMouseDown(self, p):
        """
        Indicates that there was a left click at point p (world coordinates) with the
        left shift key being held down.
        """
        self.mouseWorld = p

        if not self.mouseJoint:
            self.SpawnBomb(p)

    def MouseDown(self, p):
        """
        Indicates that there was a left click at point p (world coordinates)
        """

        if self.mouseJoint != None:
            return

        # Create a mouse joint on the selected body (assuming it's dynamic)

        # Make a small box.
        aabb = b2AABB(lowerBound=p-(0.001, 0.001), upperBound=p+(0.001, 0.001))

        # Query the world for overlapping shapes.
        body = None

        query = QueryCallback()
        self.world.QueryAABB(query, aabb)
        
        if query.fixture:
            body = query.fixture.body
            # A body was selected, create the mouse joint
            md = b2MouseJointDef()
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
        position and velocity must be b2Vec2's.
        """
        if self.bomb:
            self.world.DestroyBody(self.bomb)
            self.bomb = None

        bd = b2BodyDef()
        bd.allowSleep = True
        bd.position = position
        bd.isBullet = True
        self.bomb = self.world.CreateBody(bd)
        self.bomb.SetLinearVelocity(velocity)

        sd = b2CircleDef()
        sd.radius = 0.3
        sd.density = 20.0
        sd.restitution = 0.1

        minV = position - (0.3,0.3)
        maxV = position + (0.3,0.3)

        aabb = b2AABB()
        aabb.lowerBound = minV
        aabb.upperBound = maxV

        if self.world.InRange(aabb):
            self.bomb.CreateFixture(sd)
            self.bomb.SetMassFromShapes()

    def LaunchRandomBomb(self):
        """
        Create a new bomb and launch it at the testbed.
        """
        p = b2Vec2( b2Random(-15.0, 15.0), 30.0 )
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
            self.viewCenter -= (0.5, 0)
        elif keys[K_RIGHT]:
            self.viewCenter += (0.5, 0)

        if keys[K_UP]:
            self.viewCenter += (0, 0.5)
        elif keys[K_DOWN]:
            self.viewCenter -= (0, 0.5)

        if keys[K_HOME]:
            self.viewZoom = 1.0
            self.viewCenter = (0.0, 20.0)

    def SimulationLoop(self):
        """
        The main simulation loop. Don't override this, override Step instead.
        """

        # Reset the text line to start the text from the top
        self.textLine = 15

        # Draw the name of the test running
        self.DrawStringCR(self.name, (127,127,255))

        # Update the settings based on the GUI
        self.gui_table.updateSettings(self.settings)

        # Do the main physics step
        self.Step(self.settings)

        # In case during the step the settings changed, update the GUI reflecting
        # those settings.
        self.gui_table.updateGUI(self.settings)

    def ConvertScreenToWorld(self, x, y):
        """
        Return a b2Vec2 in world coordinates of the passed in screen coordinates x, y
        """
        return b2Vec2((x + self.viewOffset.x) / self.viewZoom, 
                           ((self.screenSize.y - y + self.viewOffset.y) / self.viewZoom))

    def DrawString(self, x, y, str, color=(229,153,153,255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        text = self.font.render(str, True, color)
        self.screen.blit(text, (x,y))

    def DrawStringCR(self, str, color=(229,153,153,255)):
        """
        Draw some text at the top status lines
        and advance to the next line.
        """
        text = self.font.render(str, True, color)
        self.screen.blit(text, (5,self.textLine))
        self.textLine += 15

    def __del__(self):
        pass

    # These can/should be implemented in the subclass: (Step() also if necessary)
    # See test_Empty.py for a simple example.

    def ShapeDestroyed(self, shape):
        """
        Callback indicating 'shape' has been destroyed.
        """
        pass

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

def main(test_class):
    """
    Loads the test class and executes it.
    """
    print "Loading %s..." % test_class.name
    test = test_class()
    if fwSettings.onlyInit:
        return
    test.run()

if __name__=="__main__":
    from test_empty import Empty
    main(Empty)
