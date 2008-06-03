#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlepages.com)
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

import TriangleMesh as tm

def H(x):
    return x/2.0

class BreakableBody(test_main.Framework):
    name="BreakableBody"
    # temporary vars to hold the examples
    maxAllowableForce = 0.0
    
    def __init__(self):
        super(BreakableBody, self).__init__()

        self.viewZoom = 6.0
        self.updateCenter()

        # geometries
        gx, gy  = 100.0, 1.0
        dx, br  =  34.0, 0.3
        sx, sy  = -dx-H(dx), 30

        # break joint, if the reactionforce exceeds:
        self.maxAllowableForce = 100.0

        # ground
        sd=box2d.b2PolygonDef()
        bd=box2d.b2BodyDef()

        bd.position.Set(0.0, 0.0)
        ground = self.world.CreateBody(bd)

        # bottom
        sd.SetAsBox( H(gx), H(gy) )
        ground.CreateShape(sd)
        sd.SetAsBox( H(dx), H(gy), box2d.b2Vec2(-dx,sy-1.0), 0.0 )
        ground.CreateShape(sd)

        # dyn bodies
        pd=box2d.b2PolygonDef()
        dj=box2d.b2DistanceJointDef()
        
        dj.dampingRatio     = 0.0
        dj.collideConnected = True
        
        nodes, segments, holes = self.ExampleData('B')
        dj.frequencyHz      = 50
        pd.density          = 1.0/70.0
        pd.friction         = 0.4
        pd.restitution      = 0.01
        self.CreateSoftBody( box2d.b2Vec2(sx,sy), 0,  pd, dj, nodes, segments, holes)
        
        nodes, segments, holes = self.ExampleData('ring')
        dj.frequencyHz      = 20
        pd.density          = 1.0/36.0
        pd.friction         = 0.1
        pd.restitution      = 0.5
        self.CreateSoftBody( box2d.b2Vec2(sx+6,sy), 0,  pd, dj,nodes, segments, holes)
        
        nodes, segments, holes = self.ExampleData('x')
        dj.frequencyHz      = 50.0
        pd.density          = 1.0/60.0
        pd.friction         = 0.6
        pd.restitution      = 0.0
        self.CreateSoftBody( box2d.b2Vec2(sx+13,sy),  0,    pd, dj,nodes, segments, holes)
        
        nodes, segments, holes = self.ExampleData('two')
        pd.density          = 0.01
        pd.friction         = 0.3
        pd.restitution      = 0.3
        self.CreateSoftBody( box2d.b2Vec2(sx+20,sy),  0,    pd, dj, nodes, segments, holes)
        
        nodes, segments, holes = self.ExampleData('D')
        self.CreateSoftBody( box2d.b2Vec2(sx+28,sy),  0,    pd, dj, nodes, segments, holes)
        
        nodes, segments, holes = self.ExampleData('b')
        pd.friction         = 0.9
        self.CreateSoftBody( box2d.b2Vec2(-5,5*gy),  40,    pd, dj ,nodes, segments, holes)

        cd=box2d.b2CircleDef()
        bd=box2d.b2BodyDef()
        cd.radius = br
        cd.density= 0.005
        bd.position.Set(0.0,10.0*gy)
        for i in range(60):
            b = self.world.CreateBody(bd)
            b.CreateShape(cd)
            b.SetMassFromShapes()
    
    # Create compound (soft) body using a triangle mesh
    # If meshDensity is 0, a minimal grid is generated.
    # Actually pd and dj define the behaviour for all triangles
    def CreateSoftBody(self, pos, meshDensity,pd, dj,nodes, segments, holes) :
        n_nodes   =len(nodes)
        n_segments=len(segments)
        n_holes   =len(holes) 

        # TriangleMesh defs
        md = tm.TriangleMesh()

        # box2d defs
        bd=box2d.b2BodyDef()

        # in case of meshDensit>3 ...
        md.SetMaxVertexCount(meshDensity)

        # triangulator main
        md.Mesh( nodes, n_nodes,  segments,n_segments,  holes, n_holes )
        md.PrintData()

        # bodies (triangles)
        triangles = md.GetTriangles()
        if triangles==None: return
        pd.vertexCount = 3

        for i in range(md.GetTriangleCount()):
            if ( triangles[i].inside ) :
                # triangle . box2d.b2PolygonDef
                pd.setVertex(0,triangles[i].v[0].x, triangles[i].v[0].y)
                pd.setVertex(1,triangles[i].v[1].x, triangles[i].v[1].y)
                pd.setVertex(2,triangles[i].v[2].x, triangles[i].v[2].y)
                bd.position.Set(pos.x,pos.y)
                b = self.world.CreateBody(bd)
                b.CreateShape(pd)
                b.SetMassFromShapes()
                # we need the body pointer in the triangles for the joints later
                triangles[i].userData = b
        # joints
        # for each triangle-pair in edges, connect with a distance joint
        edges = md.GetEdges()
        for i in range(md.GetEdgeCount()):
            t0 = edges[i].t[0]
            t1 = edges[i].t[1]
            if t0.inside==False or t1.inside==False: continue
            
            # Get bodies
            b1 = t0.userData
            b2 = t1.userData
            if b1==None or b2==None: continue
            
            dj.Initialize( b1,b2, b1.GetWorldCenter(), b2.GetWorldCenter())
            self.world.CreateJoint(dj).getAsType()

        # clean TriangleMesh
        md.Reset()
    
    def GetJoints(self):
        list=self.world.GetJointList()
        while list:
            yield list
            list = list.GetNext()

    # maybe here to check for maximal reaction forces to break a body
    def Step(self, settings):
        F=0.0
        jStressed = 0
        for j in self.GetJoints():
            tmp = j.GetReactionForce().Length()
            if tmp>F:
                F = tmp
                jStressed = j
        if jStressed and (F>self.maxAllowableForce):
            self.world.DestroyJoint(jStressed)
        self.DrawString(1, self.textLine,"|Reactionforce|%.0f |Allowable|%.0f change:-+" % (F,self.maxAllowableForce))
        self.textLine += 12
        super(BreakableBody, self).Step(settings)
    
    def Keyboard(self, key) :
        if key==K_MINUS:
            if self.maxAllowableForce > 0.0:
                self.maxAllowableForce -= 5.0
        elif key==K_PLUS or key==K_EQUALS:
            self.maxAllowableForce += 5.0
    
    # examples
    def ExampleData(self, which) :
        print "\nLoading data:", which
        data = {
            'ring_nodes' : (
                (6.00, 3.00),
                (5.12, 5.12),
                (3.00, 6.00),
                (0.88, 5.12),
                (0.00, 3.00),
                (0.88, 0.88),
                (3.00, 0.00),
                (5.12, 0.88),
                (4.50, 3.00),
                (4.06, 4.06),
                (3.00, 4.50),
                (1.94, 4.06),
                (1.50, 3.00),
                (1.94, 1.94),
                (3.00, 1.50),
                (4.06, 1.94)),

            'ring_segments' : (            
                (9, 10),
                (10, 11),
                (11, 12),
                (12, 13),
                (13, 14),
                (14, 15),
                (15, 16),
                (16, 9)),
            'ring_holes' : (
                (3.00, 3.00), ),
            # 'B'
            'B_nodes' : (
                (0.00, 0.00),
                (4.00, 0.00),
                (5.00, 2.00),
                (5.00, 4.00),
                (4.00, 5.00),
                (5.00, 6.00),
                (5.00, 8.00),
                (4.00, 9.00),
                (0.00, 9.00),
                (0.00, 5.00),
                (1.50, 1.50),
                (3.50, 1.50),
                (3.50, 4.00),
                (1.50, 4.00),
                (1.50, 6.00),
                (3.50, 6.00),
                (3.50, 8.50),
                (1.50, 8.50)),

            'B_segments' : (
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 5),
                (5, 6),
                (6, 7),
                (7, 8),
                (8, 9),
                (9, 10),
                (10, 1),
                (11, 12),
                (12, 13),
                (13, 14),
                (14, 11),
                (15, 16),
                (16, 17),
                (17, 18),
                (18, 15)),

            'B_holes' : (
                (5.00, 5.00),
                (2.50, 2.50),
                (2.50, 7.00)),
            # 'D'
            'D_nodes' : (
                (0.00, 0.00),
                (4.00, 0.00),
                (5.00, 2.50),
                (5.00, 7.00),
                (4.00, 9.00),
                (0.00, 9.00),
                (0.00, 5.00),
                (1.50, 2.50),
                (3.50, 2.50),
                (3.50, 7.00),
                (1.50, 7.00)),
            'D_segments' : (
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 5),
                (5, 6),
                (6, 7),
                (7, 1),
                (8, 9),
                (9, 10),
                (10, 11),
                (11, 8)),
            'D_holes' : ((2.50, 5.00), ),
            # 'x'
            'x_nodes' : (
                (0.00, 0.00),
                (1.00, 0.00),
                (5.00, 0.00),
                (6.00, 0.00),
                (6.00, 1.00),
                (6.00, 5.00),
                (6.00, 6.00),
                (1.00, 6.00),
                (5.00, 6.00),
                (0.00, 6.00),
                (0.00, 5.00),
                (0.00, 1.00),
                (3.00, 2.00),
                (4.00, 3.00),
                (3.00, 4.00),
                (2.00, 3.00)),

            'x_segments' : (
                (2, 13),
                (3, 13),
                (5, 14),
                (6, 14),
                (8, 15),
                (9, 15),
                (11, 16),
                (12, 16)),

            'x_holes' : (
                (3.00, 1.00),
                (5.00, 3.00),
                (3.00, 5.00),
                (1.00, 3.00)),
            # '2'
            'two_nodes' : (
                (0.00, 0.00),
                (6.00, 0.00),
                (6.00, 1.00),
                (2.00, 1.00),
                (2.00, 2.00),
                (6.00, 6.00),
                (6.00, 8.00),
                (5.00, 9.00),
                (2.00, 9.00),
                (1.00, 7.50),
                (0.00, 2.50),
                (5.00, 6.50),
                (5.00, 8.00),
                (2.50, 8.00),
                (2.00, 7.50)),
            'two_segments' : (
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 5),
                (5, 6),
                (6, 7),
                (7, 8),
                (8, 9),
                (9, 10),
                (10, 15),
                (11, 12),
                (12, 13),
                (13, 14),
                (14, 15)),
            'two_holes' : (
                (3.00, 5.00),
                (4.00, 3.00)),
            # '-' beam
            'beam_nodes' : (
                (0.00, 0.00),
                (32.00, 0.00),
                (32.00, 3.00),
                (0.00, 3.00)),
            'beam_segments' : None,
            'beam_holes' : None,
            # 'b' a box
            'b_nodes' : (
                (0.00, 0.00),
                (10.00, 0.00),
                (10.00, 10.00),
                (0.00, 10.00),
                (2.00, 2.00),
                (8.00, 2.00),
                (8.00, 8.00),
                (2.00, 8.00)),
            'b_segments' : (
                (5, 6),
                (6, 7),
                (7, 8),
                (8, 5)),
            'b_holes' : (
                (5.0, 5.0), )
            }
        # choose...
        nodes      = [tm.tmVertex( (x, y) )   for x, y  in data["%s_nodes" % which]]
        segments   = [tm.tmSegmentId((v0,v1)) for v0,v1 in data["%s_segments" % which]]
        holes      = [tm.tmVertex( (x, y) )   for x, y  in data["%s_holes" % which]]
        
        return (nodes, segments, holes)

if __name__=="__main__":
    test_main.main(BreakableBody)
