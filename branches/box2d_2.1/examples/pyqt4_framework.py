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

"""
Global Keys:
    F1     - toggle menu (can greatly improve fps)
    Space  - shoot projectile
    Z/X    - zoom
    Escape - quit

Other keys can be set by the individual test.

Mouse:
    Left click  - select/drag body (creates mouse joint)
    Right click - pan
    Shift+Left  - drag to create a directed projectile
    Scroll      - zoom

"""

from __future__ import print_function
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject, SIGNAL, pyqtSlot
from PyQt4.QtGui import QTreeWidget, QTreeWidgetItem, QColor, QPixmap
from PyQt4.QtCore import Qt, QSettings
from pyqt4_gui import Ui_MainWindow
from framework import *
#from Box2D.b2 import *
from time import time
import sys

class Pyqt4DebugDraw(b2DebugDraw):
    def __init__(self, **kwargs): 
        super(Pyqt4DebugDraw, self).__init__(**kwargs)
        self.test=kwargs['test']
        self.window=self.test.window
        self.scene=self.window.scene
        self.render_times=[]

    def StartDraw(self):
        self.scene.clear()
        self.render_start=time()

    def EndDraw(self):
        render_time=time() - self.render_start
        self.render_times.append(render_time)

        if len(self.render_times) > 10:
            self.render_times.pop(0)
        
        average_time=sum(self.render_times) / len(self.render_times)
        if average_time > 0.00001:
            fps=1.0 / average_time
            print('average fps %.0f' % fps)

    def DrawPoint(self, p, size, color):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size/self.zoom, color, drawwidth=0)
        
    def DrawAABB(self, aabb, color):
        """
        Draw a wireframe around the AABB with the given color.
        """
        self.scene.addLine(aabb.lowerBound.x, aabb.lowerBound.y, aabb.upperBound.x, aabb.lowerBound.y, 
                         pen=QtGui.QPen(QColor(*color.bytes)))
        self.scene.addLine(aabb.upperBound.x, aabb.upperBound.y, aabb.lowerBound.x, aabb.upperBound.y,
                         pen=QtGui.QPen(QColor(*color.bytes)))

    def DrawSegment(self, p1, p2, color):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen=QtGui.QPen(QColor(*color.bytes)))

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        axisScale = 0.4
        p2 = p1 + axisScale * xf.R.col1
        p3 = p1 + axisScale * xf.R.col2

        self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen=QtGui.QPen(QColor(255,0,0)))
        self.scene.addLine(p1[0], p1[1], p3[0], p3[1], pen=QtGui.QPen(QColor(0,255,0)))

    def DrawCircle(self, center, radius, color, drawwidth=1):
        """
        Draw a wireframe circle given the center, radius, axis of orientation and color.
        """
        border_color=[c*255 for c in color] + [255]
        pen  =QtGui.QPen(QtGui.QColor(*border_color))
        self.scene.addEllipse(center[0]-radius, center[1]-radius, radius*2, radius*2, pen=pen)
        self.scene.addLine(center[0], center[1], (center[0]-radius*axis[0]), (center[1]+radius*axis[1]), pen=QtGui.QPen(QColor(255,0,0)))

    def DrawSolidCircle(self, center, radius, axis, color):
        """
        Draw a solid circle given the center, radius, axis of orientation and color.
        """
        border_color=color.bytes + [255]
        inside_color=(color / 2).bytes + [127]
        brush=QtGui.QBrush(QtGui.QColor(*inside_color))
        pen  =QtGui.QPen(QtGui.QColor(*border_color))
        self.scene.addEllipse(center[0]-radius, center[1]-radius, radius*2, radius*2, brush=brush, pen=pen)
        self.scene.addLine(center[0], center[1], (center[0]-radius*axis[0]), (center[1]+radius*axis[1]), pen=QtGui.QPen(QColor(255,0,0)))

    def DrawPolygon(self, vertices, color):
        """
        Draw a wireframe polygon given the world vertices vertices (tuples) with the specified color.
        """
        poly=QtGui.QPolygonF()
        pen=QtGui.QPen(QtGui.QColor(*color.bytes))

        for v in vertices:
            poly+=QtCore.QPointF(*v)

        self.scene.addPolygon(poly, pen=pen)

    def DrawSolidPolygon(self, vertices, color):
        """
        Draw a filled polygon given the world vertices vertices (tuples) with the specified color.
        """

        poly=QtGui.QPolygonF()
        border_color=color.bytes + [255]
        inside_color=(color / 2).bytes + [127]
        brush=QtGui.QBrush(QtGui.QColor(*inside_color))
        pen  =QtGui.QPen(QtGui.QColor(*border_color))

        for v in vertices:
            poly+=QtCore.QPointF(*v)

        self.scene.addPolygon(poly, brush=brush, pen=pen)

    def DrawShape(self, fixture, transform, color):
        """
        Draw any type of shape
        """
        shape=fixture.shape
        if isinstance(shape, b2PolygonShape):
            vertices=[b2Mul(transform, v) for v in shape.vertices]
            self.DrawSolidPolygon(vertices, color)
        elif isinstance(shape, b2EdgeShape):
            v1=b2Mul(transform, shape.vertex1)
            v2=b2Mul(transform, shape.vertex2)
            self.DrawSegment(v1, v2, color)
        elif isinstance(shape, b2CircleShape):
            self.DrawSolidCircle(b2Mul(transform, shape.pos), shape.radius, transform.R.col1, color)
        elif isinstance(shape, b2LoopShape):
            vertices=shape.vertices
            v1=b2Mul(transform, vertices[-1])
            for v2 in vertices:
                v2=b2Mul(transform, v2)
                self.DrawSegment(v1, v2, color)
                v1=v2

    def DrawJoint(self, joint):
        """
        Draw any type of joint
        """
        bodyA, bodyB=joint.bodyA, joint.bodyB
        xf1, xf2=bodyA.transform, bodyB.transform
        x1, x2=xf1.position, xf2.position
        p1, p2=joint.anchorA, joint.anchorB
        color=b2Color(0.5, 0.8, 0.8)
            
        if isinstance(joint, b2DistanceJoint):
            self.DrawSegment(p1, p2, color)
        elif isinstance(joint, b2PulleyJoint):
            s1, s2=joint.groundAnchorA, joint.groundAnchorB
            self.DrawSegment(s1, p1, color)
            self.DrawSegment(s2, p2, color)
            self.DrawSegment(s1, s2, color)

        elif isinstance(joint, b2MouseJoint):
            pass # don't draw it here
        else:
            self.DrawSegment(x1, p1, color)
            self.DrawSegment(p1, p2, color)
            self.DrawSegment(x2, p2, color)

    def ManualDraw(self):
        """
        This implements code normally present in the C++ version,
        which calls the callbacks that you see in this class (DrawSegment,
        DrawSolidCircle, etc.).
        
        This is implemented in Python as an example of how to do it, and also
        a test.
        """
        colors = {
            'active'    : b2Color(0.5, 0.5, 0.3),
            'static'    : b2Color(0.5, 0.9, 0.5), 
            'kinematic' : b2Color(0.5, 0.5, 0.9), 
            'asleep'    : b2Color(0.6, 0.6, 0.6), 
            'default'   : b2Color(0.9, 0.7, 0.7), 
        
        }
        settings=self.test.settings
        world=self.test.world
        if settings.drawShapes:
            for body in world.bodies:
                transform=body.transform
                for fixture in body.fixtures:
                    
                    if not body.active: color=colors['active']
                    elif body.type==b2_staticBody: color=colors['static']
                    elif body.type==b2_kinematicBody: color=colors['kinematic']
                    elif not body.awake: color=colors['asleep']
                    else: color=colors['default']

                    self.DrawShape(fixture, transform, color)

        if settings.drawJoints:
            for joint in world.joints:
                self.DrawJoint(joint)

        # if settings.drawPairs
        #   pass

        # TODO: requires access to proxies and broadphase stuff
        #if settings.drawAABBs:
        #    color=(0.9, 0.3, 0.9)
        #    cm=world.contactManager
        #    for body in world.bodies:
        #        if not b.active:
        #            continue
        #        for fixture in body.fixtures:
        #            pass
        
class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.scene=QtGui.QGraphicsScene()
        self.scene.setBackgroundBrush( QtGui.QBrush(QtGui.QColor(0,0,0)) )
        self.graphicsView.setScene(self.scene)
        self.graphicsView.scale(10.0, -10.0)

app=None
class Pyqt4Framework(FrameworkBase):
    def setup_keys(self):
        pass
        #TODO

    def __reset(self):
        # Screen/rendering-related
        self._viewZoom          = 10.0
        self._viewCenter        = None
        self._viewOffset        = None
        self.screenSize         = None
        self.rMouseDown         = False
        self.textLine           = 30
        self.font               = None
        self.fps                = 0

        # GUI-related
        self.window=None
        self.setup_keys()
        
    def __init__(self):
        super(Pyqt4Framework, self).__init__()
        
        if fwSettings.onlyInit: # testing mode doesn't initialize Pyqt4
            return
            
        global app
        app = QtGui.QApplication(sys.argv)

        self.__reset()
        print('Initializing Pyqt4 framework...')
        # Pyqt4 Initialization
        self.window=MainWindow()
        self.window.show()

        self.window.setWindowTitle( "Python Box2D Testbed - " + self.name)

        # Screen and debug draw
        self.debugDraw = Pyqt4DebugDraw(test=self)
        self.world.debugDraw=self.debugDraw

        # Note that in this framework, we override the draw debug data routine
        # that occurs in Step(), and we implement the normal C++ code in Python.
        self.world.DrawDebugData = lambda: self.debugDraw.ManualDraw()
        self.screenSize = b2Vec2(0,0)
        self.viewCenter = (0,10.0*20.0)
        self.groundbody = self.world.CreateBody()

    def setCenter(self, value):
        """
        Updates the view offset based on the center of the screen.
        
        Tells the debug draw to update its values also.
        """
        self._viewCenter = b2Vec2( *value )
        self._viewOffset = self._viewCenter - self.screenSize/2
    
    def setZoom(self, zoom):
        self._viewZoom = zoom

    viewZoom   = property(lambda self: self._viewZoom, setZoom,
                           doc='Zoom factor for the display')
    viewCenter = property(lambda self: self._viewCenter, setCenter, 
                           doc='Screen center in camera coordinates')
    viewOffset = property(lambda self: self._viewOffset,
                           doc='The offset of the top-left corner of the screen')

    def checkEvents(self):
        """
        Check for Pyqt4 events (mainly keyboard/mouse events).
        Passes the events onto the GUI also.
        """
        for event in Pyqt4.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == Keys.K_ESCAPE):
                return False
            elif event.type == KEYDOWN:
                self._Keyboard_Event(event.key, down=True)
            elif event.type == KEYUP:
                self._Keyboard_Event(event.key, down=False)
            elif event.type == MOUSEBUTTONDOWN:
                p = self.ConvertScreenToWorld(*event.pos)
                if event.button == 1: # left
                    mods = Pyqt4.key.get_mods()
                    if mods & KMOD_LSHIFT:
                        self.ShiftMouseDown( p )
                    else:
                        self.MouseDown( p )
                elif event.button == 2: #middle
                    pass
                elif event.button == 3: #right
                    self.rMouseDown = True
                elif event.button == 4:
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

            if GUIEnabled:
                self.gui_app.event(event) #Pass the event to the GUI

        return True

    def run(self):
        """
        What would be the main loop is instead a call to 
        app.exec_() for the event-driven pyqt4.
        """
        global app
        self.step_timer = QtCore.QTimer()
        QObject.connect(self.step_timer, SIGNAL("timeout()"), lambda : self.Step(self.settings))
        self.step_timer.start(int((1000.0/self.settings.hz)))

        app.exec_()
        
        self.step_timer.stop()
        print('Cleaning up...')
        self.world.contactListener=None
        self.world.destructionListener=None
        self.world.debugDraw=None
        self.world=None

    def _Keyboard_Event(self, key, down=True):
        """
        Internal keyboard event, don't override this.

        Checks for the initial keydown of the basic testbed keys. Passes the unused
        ones onto the test via the Keyboard() function.
        """
        if down:
            if key==Keys.K_z:       # Zoom in
                self.viewZoom = min(1.1 * self.viewZoom, 50.0)
            elif key==Keys.K_x:     # Zoom out
                self.viewZoom = max(0.9 * self.viewZoom, 0.02)
            elif key==Keys.K_SPACE: # Launch a bomb
                self.LaunchRandomBomb()
            elif key==Keys.K_F1:    # Toggle drawing the menu
                self.settings.drawMenu = not self.settings.drawMenu
            else:              # Inform the test of the key press
                self.Keyboard(key)
        else:
            self.KeyboardUp(key)

    def CheckKeys(self):
        """
        Check the keys that are evaluated on every main loop iteration.
        I.e., they aren't just evaluated when first pressed down
        """
        if keys[Keys.K_LEFT]:
            self.viewCenter -= (0.5, 0)
        elif keys[Keys.K_RIGHT]:
            self.viewCenter += (0.5, 0)

        if keys[Keys.K_UP]:
            self.viewCenter += (0, 0.5)
        elif keys[Keys.K_DOWN]:
            self.viewCenter -= (0, 0.5)

        if keys[Keys.K_HOME]:
            self.viewZoom = 1.0
            self.viewCenter = (0.0, 20.0)

   
    def Step(self, settings):
        super(Pyqt4Framework, self).Step(settings)

    def ConvertScreenToWorld(self, x, y):
        return b2Vec2((x + self.viewOffset.x) / self.viewZoom, 
                           ((self.screenSize.y - y + self.viewOffset.y) / self.viewZoom))


    def DrawString(self, x, y, str, color=(229,153,153,255)):
        """
        Draw some text, str, at screen coordinates (x, y).
        """
        #self.screen.blit(self.font.render(str, True, color), (x,y))
        pass

    def DrawStringCR(self, str, color=(229,153,153,255)):
        """
        Draw some text at the top status lines
        and advance to the next line.
        """
        #self.screen.blit(self.font.render(str, True, color), (5,self.textLine))
        self.textLine += 15

    def Keyboard(self, key):
        """
        Callback indicating 'key' has been pressed down.
        The keys are mapped after pygame's style.

         from framework import Keys
         if key == Keys.K_z:
             ...
        """
        pass

    def KeyboardUp(self, key):
        """
        Callback indicating 'key' has been released.
        See Keyboard() for key information
        """
        pass


