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
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QColor, QPixmap
from PyQt4.QtCore import Qt, QSettings
from pyqt4_gui import Ui_MainWindow
from framework import *
#from Box2D.b2 import *
from time import time
import string
import sys

class Pyqt4DebugDraw(object):
    """
    This debug drawing class differs from the other frameworks.
    It provides an example of how to iterate through all the objects
    in the world and associate (in PyQt4's case) QGraphicsItems with
    them. 

    While DrawPolygon and DrawSolidPolygon are not used for the core
    shapes in the world (DrawPolygonShape is), they are left in for
    compatibility with other frameworks and the tests.

    world_coordinate parameters are also left in for compatibility.
    Screen coordinates cannot be used, as PyQt4 does the scaling and
    rotating for us.

    If you utilize this framework and need to add more items to the 
    QGraphicsScene for a single step, be sure to add them to the 
    temp_items array to be deleted on the next draw. 
    """
    MAX_TIMES=20
    def __init__(self, test): 
        self.test=test
        self.window=self.test.window
        self.scene=self.window.scene
        self.view=self.window.graphicsView
        self.render_times=[]
        self.item_cache={}
        self.temp_items=[]
        self.status_font=QtGui.QFont("Times", 10, QtGui.QFont.Bold)
        self.font_spacing=QtGui.QFontMetrics(self.status_font).lineSpacing()

    def StartDraw(self):
        for item in self.temp_items:
            self.scene.removeItem(item)
        self.temp_items=[]

        self.render_start=time()

    def EndDraw(self):
        render_time=time() - self.render_start
        self.render_times.append(render_time)

        if len(self.render_times) > self.MAX_TIMES:
            self.render_times.pop(0)
        
        average_time=sum(self.render_times) / len(self.render_times)
        if average_time > 1e-10:
            status_text=('average frame render time %.2gms, potential fps: %.5g' % (average_time*1000, 1./average_time))
            pen=QtGui.QPen(QColor(255,255,255))
            self.test.fps=1./average_time
            self.DrawString(0, 0, status_text, (255,255,255))

    def SetFlags(self, **kwargs): 
        """
        For compatibility with other debug drawing classes.
        """
        pass

    def DrawString(self, x, y, str, color):
        item=QtGui.QGraphicsSimpleTextItem(str)
        #brush=QtGui.QBrush(QColor(*color))
        brush=QtGui.QBrush(QColor(255,255,255,255))
        item.setFont(self.status_font)
        item.setBrush(brush)
        item.setPos(self.view.mapToScene(x,y))
        item.scale(1./self.test._viewZoom, -1./self.test._viewZoom)
        self.temp_items.append(item)

        self.scene.addItem(item)

    def DrawPoint(self, p, size, color, world_coordinates=True):
        """
        Draw a single point at point p given a pixel size and color.
        """
        self.DrawCircle(p, size/self.test.viewZoom, color, drawwidth=0)
        
    def DrawAABB(self, aabb, color, world_coordinates=True):
        """
        Draw a wireframe around the AABB with the given color.
        """
        line1=self.scene.addLine(aabb.lowerBound.x, aabb.lowerBound.y, aabb.upperBound.x, aabb.lowerBound.y, 
                         pen=QtGui.QPen(QColor(*color.bytes)))
        line2=self.scene.addLine(aabb.upperBound.x, aabb.upperBound.y, aabb.lowerBound.x, aabb.upperBound.y,
                         pen=QtGui.QPen(QColor(*color.bytes)))
        self.temp_items.append(line1)
        self.temp_items.append(line2)

    def DrawSegment(self, p1, p2, color, world_coordinates=True):
        """
        Draw the line segment from p1-p2 with the specified color.
        """
        line=self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen=QtGui.QPen(QColor(*color.bytes)))
        self.temp_items.append(line)

    def DrawTransform(self, xf):
        """
        Draw the transform xf on the screen
        """
        p1 = xf.position
        axisScale = 0.4
        p2 = p1 + axisScale * xf.R.col1
        p3 = p1 + axisScale * xf.R.col2

        line1=self.scene.addLine(p1[0], p1[1], p2[0], p2[1], pen=QtGui.QPen(QColor(255,0,0)))
        line2=self.scene.addLine(p1[0], p1[1], p3[0], p3[1], pen=QtGui.QPen(QColor(0,255,0)))
        self.temp_items.append(line1)
        self.temp_items.append(line2)

    def DrawCircle(self, center, radius, color, drawwidth=1, shape=None, world_coordinates=True):
        """
        Draw a wireframe circle given the center, radius, axis of orientation and color.
        Note that these functions 
        """
        border_color=[c*255 for c in color] + [255]
        pen  =QtGui.QPen(QtGui.QColor(*border_color))
        ellipse=self.scene.addEllipse(center[0]-radius, center[1]-radius, radius*2, radius*2, pen=pen)
        self.temp_items.append(ellipse)

    def DrawSolidCircle(self, center, radius, axis, color, shape=None, world_coordinates=True):
        """
        Draw a solid circle given the center, radius, axis of orientation and color.
        """
        border_color=color.bytes + [255]
        inside_color=(color / 2).bytes + [127]
        brush=QtGui.QBrush(QtGui.QColor(*inside_color))
        pen  =QtGui.QPen(QtGui.QColor(*border_color))
        ellipse=self.scene.addEllipse(center[0]-radius, center[1]-radius, radius*2, radius*2, brush=brush, pen=pen)
        line=self.scene.addLine(center[0], center[1], (center[0]-radius*axis[0]), (center[1]-radius*axis[1]), pen=QtGui.QPen(QColor(255,0,0)))

        self.temp_items.append(ellipse)
        self.temp_items.append(line)

    def DrawPolygon(self, vertices, color, shape=None, world_coordinates=True):
        """
        Draw a wireframe polygon given the world vertices vertices (tuples) with the specified color.
        """
        poly=QtGui.QPolygonF()
        pen=QtGui.QPen(QtGui.QColor(*color.bytes))

        for v in vertices:
            poly+=QtCore.QPointF(*v)

        item=self.scene.addPolygon(poly, pen=pen)
        self.temp_items.append(item)

    def DrawSolidPolygon(self, vertices, color, shape=None, world_coordinates=True):
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

        item=self.scene.addPolygon(poly, brush=brush, pen=pen)
        self.temp_items.append(item)

    def DrawCircleShape(self, shape, transform, color, temporary=False):
        center=b2Mul(transform, shape.pos)
        radius=shape.radius
        axis=transform.R.col1

        border_color=color.bytes + [255]
        inside_color=(color / 2).bytes + [127]
        brush=QtGui.QBrush(QtGui.QColor(*inside_color))
        pen  =QtGui.QPen(QtGui.QColor(*border_color))
        ellipse=self.scene.addEllipse(-radius, -radius, radius*2, radius*2, brush=brush, pen=pen)
        line=self.scene.addLine(center[0], center[1], (center[0]-radius*axis[0]), (center[1]-radius*axis[1]), pen=QtGui.QPen(QColor(255,0,0)))
        ellipse.setPos(*center)

        if temporary:
            self.temp_items.append(ellipse)
            self.temp_items.append(line)
        else:
            self.item_cache[hash(shape)]=[ellipse, line]
        
    def DrawPolygonShape(self, shape, transform, color, temporary=False):
        poly=QtGui.QPolygonF()
        border_color=color.bytes + [255]
        inside_color=(color / 2).bytes + [127]
        brush=QtGui.QBrush(QtGui.QColor(*inside_color))
        pen  =QtGui.QPen(QtGui.QColor(*border_color))

        for v in shape.vertices:
            poly+=QtCore.QPointF(*v)

        item=self.scene.addPolygon(poly, brush=brush, pen=pen)
        item.setRotation(transform.angle * 180.0 / b2_pi)
        item.setPos(*transform.position)

        if temporary:
            self.temp_items.append(item)
        else:
            self.item_cache[hash(shape)]=[item]

    def DrawShape(self, shape, transform, color, selected=False):
        """
        Draw any type of shape
        """
        if hash(shape) in self.item_cache:
            items=self.item_cache[hash(shape)]
            items[0].setRotation(transform.angle * 180.0 / b2_pi)
            if isinstance(shape, b2CircleShape):
                center=b2Mul(transform, shape.pos)
                items[0].setPos(*center)
                line=items[1]
                radius=shape.radius
                axis=transform.R.col1
                line.setLine(center[0], center[1], (center[0]-radius*axis[0]), (center[1]-radius*axis[1]))
            else:
                items[0].setPos(*transform.position)

            if not selected:
                return

        if selected:
            color=b2Color(1,1,1)
            temporary=True
        else:
            temporary=False

        if isinstance(shape, b2PolygonShape):
            self.DrawPolygonShape(shape, transform, color, temporary)
        elif isinstance(shape, b2EdgeShape):
            v1=b2Mul(transform, shape.vertex1)
            v2=b2Mul(transform, shape.vertex2)
            self.DrawSegment(v1, v2, color)
        elif isinstance(shape, b2CircleShape):
            self.DrawCircleShape(shape, transform, color, temporary)
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
        if self.test.selected_shape:
            sel_shape, sel_body=self.test.selected_shape
        else:
            sel_shape=None

        if settings.drawShapes:
            for body in world.bodies:
                transform=body.transform
                for fixture in body.fixtures:
                    shape=fixture.shape

                    if not body.active: color=colors['active']
                    elif body.type==b2_staticBody: color=colors['static']
                    elif body.type==b2_kinematicBody: color=colors['kinematic']
                    elif not body.awake: color=colors['asleep']
                    else: color=colors['default']
                    
                    self.DrawShape(fixture.shape, transform, color, (sel_shape==shape))


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


class GraphicsScene (QtGui.QGraphicsScene):
    def __init__(self, test, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.test=test

    def keyPressEvent(self, event):
        self.test._Keyboard_Event(event.key(), down=True)

    def keyReleaseEvent(self, event):
        self.test._Keyboard_Event(event.key(), down=False)

    def mousePressEvent(self, event):
        pos=self.test.ConvertScreenToWorld(event.scenePos().x(), event.scenePos().y())
        if event.button()==Qt.RightButton:
            self.test.ShowProperties(pos)
        elif event.button()==Qt.LeftButton:
            if event.modifiers() == Qt.ShiftModifier:
                self.test.ShiftMouseDown(pos)
            else:
                self.test.MouseDown(pos)

    def mouseReleaseEvent(self, event):
        pos=event.scenePos().x(), event.scenePos().y()
        if event.button()==Qt.RightButton:
            self.test.MouseUp(pos)
        elif event.button()==Qt.LeftButton:
            self.test.MouseUp(pos)

    def mouseMoveEvent(self, event):
        pos=event.scenePos().x(), event.scenePos().y()
        self.test.MouseMove(self.test.ConvertScreenToWorld(*pos))
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)
        
class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, test, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.scene=GraphicsScene(test)
        self.test=test
        self.scene.setBackgroundBrush( QtGui.QBrush(QtGui.QColor(0,0,0)) )
        self.graphicsView.setScene(self.scene)
        self.graphicsView.scale(self.test.viewZoom, -self.test.viewZoom)
        self.reset_properties_list()

    def reset_properties_list(self):
        self.twProperties.clear()
        self.twProperties.setRowCount(0)
        self.twProperties.setColumnCount(3)
        self.twProperties.verticalHeader().hide() # don't show numbers on left
        self.twProperties.setHorizontalHeaderLabels(['class', 'name', 'value'])
    
    def keyPressEvent(self, event):
        self.test._Keyboard_Event(event.key(), down=True)

    def keyReleaseEvent(self, event):
        self.test._Keyboard_Event(event.key(), down=False)

app=None
class Pyqt4Framework(FrameworkBase):
    TEXTLINE_START=0
    def setup_keys(self):
        # Only basic keys are mapped for now: K_[a-z0-9], K_F[1-12] and K_COMMA.

        for letter in string.uppercase:
            setattr(Keys, 'K_'+letter.lower(), getattr(Qt, 'Key_%s' % letter))
        for i in range(0,10):
            setattr(Keys, 'K_%d'%i, getattr(Qt, 'Key_%d' % i))
        for i in range(1,13):
            setattr(Keys, 'K_F%d'%i, getattr(Qt, 'Key_F%d' % i))
        Keys.K_LEFT=Qt.Key_Left
        Keys.K_RIGHT=Qt.Key_Right
        Keys.K_UP=Qt.Key_Up
        Keys.K_DOWN=Qt.Key_Down
        Keys.K_HOME=Qt.Key_Home
        Keys.K_PAGEUP=Qt.Key_PageUp
        Keys.K_PAGEDOWN=Qt.Key_PageDown
        Keys.K_COMMA=Qt.Key_Comma
        Keys.K_SPACE=Qt.Key_Space

    def __reset(self):
        # Screen/rendering-related
        self._viewZoom          = 10.0
        self._viewCenter        = None
        self._viewOffset        = None
        self.screenSize         = None
        self.textLine           = 0
        self.font               = None
        self.fps                = 0
        self.selected_shape     = None

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
        self.window=MainWindow(self)
        self.window.show()

        self.window.setWindowTitle( "Python Box2D Testbed - " + self.name)
        self.debugDraw = Pyqt4DebugDraw(self)

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
        self.window.graphicsView.centerOn(*self._viewCenter)
    
    def setZoom(self, zoom):
        self._viewZoom = zoom
        self.window.graphicsView.resetTransform()
        self.window.graphicsView.scale(self._viewZoom, -self._viewZoom)
        self.window.graphicsView.centerOn(*self._viewCenter)

    viewZoom   = property(lambda self: self._viewZoom, setZoom,
                           doc='Zoom factor for the display')
    viewCenter = property(lambda self: self._viewCenter, setCenter, 
                           doc='Screen center in camera coordinates')
    viewOffset = property(lambda self: self._viewOffset,
                           doc='The offset of the top-left corner of the screen')

    def run(self):
        """
        What would be the main loop is instead a call to 
        app.exec_() for the event-driven pyqt4.
        """
        global app
        self.step_timer = QtCore.QTimer()
        QObject.connect(self.step_timer, SIGNAL("timeout()"), lambda : self.SimulationLoop())
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
                self.viewZoom = min(1.10 * self.viewZoom, 50.0)
            elif key==Keys.K_x:     # Zoom out
                self.viewZoom = max(0.9 * self.viewZoom, 0.02)
            elif key==Keys.K_SPACE: # Launch a bomb
                self.LaunchRandomBomb()
            else:              # Inform the test of the key press
                self.Keyboard(key)
        else:
            self.KeyboardUp(key)

    def CheckKeys(self):
        pass

    def _ShowProperties(self, obj):
        class_=obj.__class__
        ignore_list=('thisown',)

        i=0
        for prop in dir(class_):
            if isinstance(getattr(class_, prop), property) and prop not in ignore_list:
                try:
                    value=getattr(obj, prop)
                except:
                    continue

                widget=None
                self.window.twProperties.setRowCount(self.window.twProperties.rowCount()+1)
                i=self.window.twProperties.rowCount()-1
                self.item=QTableWidgetItem(class_.__name__)
                self.window.twProperties.setItem(i, 0, QTableWidgetItem(class_.__name__))
                self.window.twProperties.setItem(i, 1, QtGui.QTableWidgetItem(prop))

                if isinstance(value, b2Vec2):
                    value=tuple(value)
                elif isinstance(value, bool):
                    widget=QtGui.QCheckBox('')
                    QtCore.QObject.connect(widget, SIGNAL('stateChanged(int)'), self.property_changed)
                elif isinstance(value, (int, float)):
                    widget=QtGui.QDoubleSpinBox()
                    QtCore.QObject.connect(widget, SIGNAL('valueChanged(double)'), self.property_changed)
                    widget.setValue(value)
                else:
                    pass

                if widget:
                    self.window.twProperties.setCellWidget(i, 2, widget)
                else:
                    value=QtGui.QTableWidgetItem(str(value))
                    self.window.twProperties.setItem(i, 2, value)
                i+=1

    def property_changed(self, value=None):
        print('property changed', value)

    def ShowProperties(self, p):
        aabb = b2AABB(lowerBound=p-(0.001, 0.001), upperBound=p+(0.001, 0.001))

        # Query the world for overlapping shapes.
        query = fwQueryCallback(p)
        self.world.QueryAABB(query, aabb)
        
        if query.fixture:
            self.window.reset_properties_list()

            fixture=query.fixture
            body=fixture.body
            self._ShowProperties(body)

            shape=fixture.shape
            self.selected_shape=(shape, body)
            self._ShowProperties(shape)

    def Step(self, settings):
        super(Pyqt4Framework, self).Step(settings)

    def ConvertScreenToWorld(self, x, y):
        """
        PyQt4 gives us transformed positions, so no need to convert
        """
        return b2Vec2(x, y)

    
    DrawString=lambda self, *args: self.debugDraw.DrawString(*args)
    def DrawStringCR(self, str, color=(229,153,153,255)):
        """
        Draw some text at the top status lines and advance to the next line.
        """
        self.DrawString(5, self.textLine, str, color)
        self.textLine += self.debugDraw.font_spacing

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

    def FixtureDestroyed(self, fixture):
        shape=fixture.shape
        if shape==self.selected_shape[0]:
            self.selected_shape=None
        if hash(shape) in self.debugDraw.item_cache:
            scene_items=self.debugDraw.item_cache[hash(shape)]
            for item in scene_items:
                self.window.scene.removeItem(item)
            del self.debugDraw.item_cache[hash(shape)]

