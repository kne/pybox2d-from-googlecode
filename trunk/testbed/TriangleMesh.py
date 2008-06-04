#!/usr/bin/python
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.gphysics.com
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlepages.com)
# 
# Note that this code does not follow the zlib license like the rest of the code does.
#
# See the license below if you are planning on distributing a project that uses this
# code.
#
# -----------------------------------------------------------------------------
# Original comments (ported from the C++ version):
#
# lite delauney triangle mesh generator
#
# 2001/03 as part of a basic FEA package
# 2008/05 some small changes for box2d
# example: see main at the of this file
#
# See
# 1) A Delaunay Refinement Algorithm for Quality 2-Dimensional Mesh Generation
#    Jim Ruppert - Journal of Algorithms, 1995
# 2) Jonathan Shewchuk
#    http:#www.cs.cmu.edu/~quake/triangle.html
# Idea from
# 3) Francois Labelle
#    http:#www.cs.berkeley.edu/~flab/
#    a copy of original license (mesh.c):
#        Original author:
#        Francois Labelle <flab@cs.berkeley.edu>
#        University of California - Berkeley
#        
#        Licence:
#        - This code can be freely used, copied, and redistributed by anyone.
#        - You are free to modify or expand this code, provided that:
#        o  it contains this 16-line comment
#        o  it still obeys this licence
#        - You are free to use this code as a part of a larger program, provided
#        that the whole program can be freely used, copied, and redistributed
#        by anyone.
#        
#        Disclaimer:
#        Do not compile or run this code under any circumstance. Delete this
#        file now.

from math import sin, cos, atan2, sqrt, pow, floor, log

# errors and warnings
tmE_OK    =0
tmE_MEM   =1
tmE_HOLES =2

# constants
tmC_PI              =3.14159265359
tmC_PIx2            =6.28318530718
tmC_PI_3            =1.04719755119
tmC_SQRT2           =1.41421356237
tmC_BIGNUMBER       =1.0e10
tmC_MAXVERTEXCOUNT  =500

# options
tmO_SEGMENTBOUNDARY =  2
tmO_CONVEXHULL      =  4
tmO_MINIMALGRID     =  8
tmO_BASICMESH       = 16
# bit to mark if maxVertexCount was enough
tmO_ENOUGHVERTICES  =128

class tmVertex(object):
    # x, y
    def __init__(self, tuple=(0.0, 0.0)):
        self.x, self.y = tuple
    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

class tmSegment(object):
    # tmVertex v[2] 
    def __init__(self):
        self.v = [tmVertex(), tmVertex()]

class tmSegmentId(object):
    # i1, i2
    def __init__(self, tuple=(0, 0)):
        self.i1, self.i2 = tuple

class tmEdge(object):
    def __init__(self):
        self.v = [None, None]
        self.locked = False
        self.t = [None, None]

class Triangle(object):
    def __init__(self):
        self.v = [None, None, None]
        self.e = [tmEdge(), tmEdge(), tmEdge()]
        self.minAngle = 0.0
        self.angle    = 0.0
        self.inside   = False
        # hold attributes for the triangles, internally not used
        self.userData = None

class TriangleMesh(object):
    Vertices  = []
    Edges     = []
    Triangles = []
    Segments  = []
    def __init__(self, aMaxVertexCount=tmC_MAXVERTEXCOUNT, aMinAngle=30.0, aOptions=tmO_MINIMALGRID|tmO_CONVEXHULL):
        self.Reset()
        self.maxVertexCount = aMaxVertexCount
        self.minAngle       = aMinAngle
        self.options        = aOptions

    def SetMaxVertexCount(self, count):
       if count>3:
           self.maxVertexCount = count
           self.options &= ~tmO_MINIMALGRID

    def SetOptions(self, options): self.options = options
    def AddOption(self, options):  self.options |= options

    # angle in degrees!
    def SetAngle(self, angle): self.minAngle = angle
    def GetVertexCount(self):          return self.vertexCount        
    def GetInputVertexCount(self):     return self.inputVertexCount   
    def GetEdgeCount(self):            return self.edgeCount          
    def GetTriangleCount(self):        return self.triangleCount      
    def GetInsideTriangleCount(self):  return self.insideTriangleCount
    def GetVertices(self):  return self.Vertices  
    def GetEdges(self):     return self.Edges     
    def GetTriangles(self): return self.Triangles  
    
    def Mesh(self, input, n_input, segment, n_segment, hole, n_holes):
        i=0
        rtn = tmE_OK
        hasInsideTriangles=False

        self.inputVertexCount = n_input
        self.vertexCount      = n_input + 3

        # max sizes
        self.maxVertexCount  += 3
        self.maxEdgeCount     = 3*self.maxVertexCount - 6
        self.maxTriangleCount = 2*self.maxVertexCount - 5 + 1
        self.maxSegmentCount  = 3*self.maxVertexCount - 6

        # allocate space
        for i in range(self.maxVertexCount):
            self.Vertices.append(tmVertex())
        for i in range(self.maxEdgeCount):
            self.Edges.append(tmEdge())
        for i in range(self.maxTriangleCount):
            self.Triangles.append(Triangle())
        for i in range(self.maxSegmentCount):
            self.Segments.append(tmSegment())

        # first 3 points are big equilateral triangle
        for i in range(3):
            self.Vertices[i].x = tmC_BIGNUMBER * cos(i*(tmC_PIx2/3.0))
            self.Vertices[i].y = tmC_BIGNUMBER * sin(i*(tmC_PIx2/3.0))

        # copy input vertices
        if input and n_input>0:
            for i in range(3,self.vertexCount):
                self.Vertices[i].x = input[i-3].x
                self.Vertices[i].y = input[i-3].y

        # given segments (boundary restrictions)
        if n_segment>0:
            self.segmentCount = n_segment
            for i in range(n_segment):
                self.Segments[i].v[0] = self.Vertices[segment[i].i1+3-1]
                self.Segments[i].v[1] = self.Vertices[segment[i].i2+3-1]

        # add boundary and close last/first,this adds ALL input vertices
        if self.options & tmO_SEGMENTBOUNDARY:
            self.AutoSegment(1, inputVertexCount, True )

        # assign hole pointer
        self.holeCount = n_holes
        self.Holes     = hole

        self.Triangulate()

        if self.options & tmO_BASICMESH ==0:
            # convex graphs
            if self.options & tmO_CONVEXHULL:
                self.ConvexHull()

            self.InsertSegments()
            # mark triangles
            if self.options & tmO_ENOUGHVERTICES:
               self.MarkInsideTriangles(True)
               
               for i in range(self.triangleCount):
                    if self.Triangles[i].inside:
                         hasInsideTriangles = True
                         break
               assert( hasInsideTriangles )
            else:
               self.MarkInsideTriangles(False)
            #
            for i in range(self.segmentCount):
               e  = self.GetEdge(self.Segments[i].v[0], self.Segments[i].v[1])
               if e: e.locked = True
            #
            self.DeleteBadTriangles()
        else:
          self.MarkInsideTriangles(False)

        self.insideTriangleCount = 0
        for i in range(self.triangleCount):
            if self.Triangles[i].inside:
                self.insideTriangleCount += 1
        return rtn

    def Triangulate(self):
         self.triangleCount = 0
         self.edgeCount     = 0
         self.lastTriangle  = None
         
         v0 = self.Vertices[0]
         v1 = self.Vertices[1]
         v2 = self.Vertices[2]
         
         t0 = self.AddTriangle()
         t1 = self.AddTriangle()
         
         e0 = self.AddEdge()
         e1 = self.AddEdge()
         e2 = self.AddEdge()
         
         self.SetTriangle( t0, v0, v1, v2, e0, e1, e2)
         self.SetTriangle( t1, v0, v2, v1, e2, e1, e0)
         
         self.SetEdge(e0, v0, v1, t0, t1)
         self.SetEdge(e1, v1, v2, t0, t1)
         self.SetEdge(e2, v2, v0, t0, t1)
         
         for i in range(3, self.vertexCount):
             self.InsertVertex(self.Vertices[i])

    def CircumCenter(self, c, t):
         # center
         c0x = (t.v[0].x + t.v[1].x + t.v[2].x)/3.0
         c0y = (t.v[0].y + t.v[1].y + t.v[2].y)/3.0

         # deltas
         dx  = t.v[1].x - t.v[0].x
         dy  = t.v[1].y - t.v[0].y
         ex  = t.v[2].x - t.v[0].x
         ey  = t.v[2].y - t.v[0].y
         #
         f   = 0.5 / (ex*dy - ey*dx)
         e2  = ex*ex + ey*ey
         d2  = dx*dx + dy*dy
         c1x = t.v[0].x + f * (e2*dy - d2*ey)
         c1y = t.v[0].y + f * (d2*ex - e2*dx)

         # look if already existing
         for i in range(20):
              c.x = c1x
              c.y = c1y
              if self.FindVertex(c):
                   v = self.GetClosestVertex(c1x, c1y)
                   if (v==t.v[0] or v==t.v[1] or v==t.v[2]): return
              c1x = c0x + 0.9*(c1x-c0x)
              c1y = c0y + 0.9*(c1y-c0y)

         # center
         c.x = c0x
         c.y = c0y

    def DeleteTriangle(self, t):
        # delete recursive
         if t.inside==False: return 

         t.inside = False
         for i in range(3):
            e = t.e[i]
            if self.GetSegment( e.v[0], e.v[1])==None:
                assert( e.t[0]==t or e.t[1]==t )

                if   e.t[0]==t: self.DeleteTriangle(e.t[1])
                elif e.t[1]==t: self.DeleteTriangle(e.t[0])

    def AutoSegment(self, startNode, endNode, doclose):
         k = self.segmentCount
         for i in range(startNode-1, endNode-1):
             k+=1
             self.Segments[k].v[0] = self.Vertices[i+3]
             self.Segments[k].v[1] = self.Vertices[i+3+1]
             self.segmentCount+=1

         if doclose:
             self.Segments[k].v[0] = self.Vertices[i+3]
             self.Segments[k].v[1] = self.Vertices[3]
             self.segmentCount+=1

    def AddVertex(self):
         if self.vertexCount >= self.maxVertexCount: return None
         self.vertexCount+=1
         return self.Vertices[self.vertexCount-1]

    def AddEdge(self):
         assert( self.edgeCount<self.maxEdgeCount )
         self.edgeCount+=1
         return self.Edges[self.edgeCount-1]

    def AddSegment(self):
         assert( self.segmentCount<self.maxSegmentCount )
         self.segmentCount+=1
         return self.Segments[self.segmentCount-1]

    def AddTriangle(self):
         assert(self.triangleCount < self.maxTriangleCount)
         self.Triangles[self.triangleCount].userData = None
         self.triangleCount += 1
         return self.Triangles[self.triangleCount-1]

    def GetOppositeVertex(self, e, t):
        if e==t.e[0]: return t.v[2]
        if e==t.e[1]: return t.v[0]
        if e==t.e[2]: return t.v[1]
        assert(False)
        return None 

    def SetEdge(self, e, v0, v1, t0, t1):
        e.v[0], e.v[1] = v0, v1
        e.t[0], e.t[1] = t0, t1
        e.locked=False

    def GetEdge(self, v0, v1):
         for i in range(self.edgeCount):
              if ((v0==self.Edges[i].v[0] and v1==self.Edges[i].v[1]) or
                 (v0==self.Edges[i].v[1] and v1==self.Edges[i].v[0])):
                    return self.Edges[i]
         return None

    def SetTriangle(self,t,v0,v1,v2,e0,e1,e2) :
        t.v[0], t.v[1], t.v[2] = v0, v1, v2
        t.e[0], t.e[1], t.e[2] = e0, e1, e2
        t.minAngle, t.angle = self.SetTriangleData( v0, v1, v2)
        t.inside = True

    def SetTriangleData(self,v0,v1,v2):
         self.HasBoundingVertices(v0, v1, v2)
         
         d0x = v1.x - v0.x; d0y = v1.y - v0.y
         d1x = v2.x - v1.x; d1y = v2.y - v1.y
         d2x = v0.x - v2.x; d2y = v0.y - v2.y
         
         t0 = self.ArcTan2(d0y, d0x)
         t1 = self.ArcTan2(d1y, d1x)
         t2 = self.ArcTan2(d2y, d2x)
         
         a0 = self.GetAngle(t2 + tmC_PI, t0)
         a1 = self.GetAngle(t0 + tmC_PI, t1)
         a2 = self.GetAngle(t1 + tmC_PI, t2)

         amin = min(a0, a1, a2)

         minAngle = amin*180.0/tmC_PI
         
         if self.IsOppositeVertex( v2, v0, v1):  a0 = tmC_PI_3 
         if self.IsOppositeVertex( v0, v1, v2):  a1 = tmC_PI_3
         if self.IsOppositeVertex( v1, v2, v0):  a2 = tmC_PI_3

         amin = min(a0, a1, a2)
         
         if self.options & tmO_MINIMALGRID:
              angle = amin*180.0/tmC_PI
         else:
              d = sqrt( d0x*d0x + d0y*d0y ) + sqrt( d1x*d1x + d1y*d1y ) + sqrt( d2x*d2x + d2y*d2y )
              angle = amin/d/d

         return minAngle, angle

    def HasBoundingVertices(self,v0,v1,v2):
         return (v0 in self.Vertices[:3] or v1 in self.Vertices[:3] or v2 in self.Vertices[:3])

    def CheckNumber(self, x):
        pass
        # todo: assert x is finite
        #def isnan(x):
        #    return isinstance(x, float) and x != x
        #assert(not isnan(x))

    def ArcTan2(self, x, y):
        self.CheckNumber(x)
        self.CheckNumber(y)
        return atan2(x,y)

    def GetAngle(self, a1, a0):
         d = a1 - a0
         self.CheckNumber(a0)
         self.CheckNumber(a1)
         while d >   tmC_PI: d -= tmC_PIx2
         while d <= -tmC_PI: d += tmC_PIx2
         return d

    def GetSegment(self,v0,v1):
         for i in range(self.segmentCount):
              x0, x1 = self.Segments[i].v
              if (v0==x0 and v1==x1) or (v0==x1 and v1==x0):
                  return self.Segments[i]
         return None

    def GetAdjacentEdges(self, e, t) :
         assert( (e==t.e[0])or(e==t.e[1])or(e==t.e[2]) )

         if      (e==t.e[0]): return (t.e[1], t.e[2], t.v[2])
         elif (e==t.e[1]):    return (t.e[2], t.e[0], t.v[0])
         elif (e==t.e[2]):    return (t.e[0], t.e[1], t.v[1])

    def IsOppositeVertex(self, v0, v1, v2):
         return ( (v1 in self.Vertices[:self.inputVertexCount] )
             and (  self.GetSegment(v0, v1) != None      )
             and (  self.GetSegment(v1, v2) != None      )  )

    def FixEdge(self, e, t0, t1):
         assert( (e.t[0]==t0) or (e.t[1]==t0) )
         
         if   e.t[0]==t0:  e.t[0] = t1
         elif e.t[1]==t0:  e.t[1] = t1 

    def InsertVertexAt(self, v, e):
         t0, t1 = e.t
         v0, v2 = e.v
         e2, e3, v3 = self.GetAdjacentEdges(e, t0)
         e0, e1, v1 = self.GetAdjacentEdges(e, t1)
         
         t2 = self.AddTriangle()
         t3 = self.AddTriangle()
         f0 = self.AddEdge()
         f1 = self.AddEdge()
         f2 = self.AddEdge()
         
         i0     = t0.inside
         i1     = t1.inside
         locked = e.locked
         
         self.SetTriangle( t0, v3, v0, v, e3, e, f2)
         self.SetTriangle( t1, v0, v1, v, e0, f0, e)
         self.SetTriangle( t2, v1, v2, v, e1, f1, f0)
         self.SetTriangle( t3, v2, v3, v, e2, f2, f1)
         
         self.SetEdge(e, v0, v, t0, t1)
         self.SetEdge(f0, v1, v, t1, t2)
         self.SetEdge(f1, v2, v, t2, t3)
         self.SetEdge(f2, v3, v, t3, t0)
         
         self.FixEdge(e1, t1, t2)
         self.FixEdge(e2, t0, t3)
         
         t0.inside = i0
         t1.inside = i1
         t2.inside = i1
         t3.inside = i0
         
         e.locked  = locked
         f1.locked = locked
         
         if i0:
              self.CheckEdge( e2)
              self.CheckEdge( e3)
         if i1:
              self.CheckEdge( e0)
              self.CheckEdge( e1)

    def InsertVertex(self, v):
         t0 = self.FindVertex(v)
         assert( t0 != None )
         
         for i in range(3):
              v0 = t0.v[i]
              if i == 2: v1 = t0.v[0]
              else:      v1 = t0.v[i+1]
              if self.GetVertexPosition(v0, v1, v)==0:
                   self.InsertVertexAt( v, t0.e[i] )
                   return
         
         v0, v1, v2 = t0.v
         e0, e1, e2 = t0.e
         
         t1 = self.AddTriangle()
         t2 = self.AddTriangle()
         f0 = self.AddEdge()
         f1 = self.AddEdge()
         f2 = self.AddEdge()
         
         self.SetTriangle( t0, v0, v1, v, e0, f1, f0)
         self.SetTriangle( t1, v1, v2, v, e1, f2, f1)
         self.SetTriangle( t2, v2, v0, v, e2, f0, f2)
         
         self.SetEdge(f0, v0, v, t2, t0)
         self.SetEdge(f1, v1, v, t0, t1)
         self.SetEdge(f2, v2, v, t1, t2)
         
         self.FixEdge(e1, t0, t1)
         self.FixEdge(e2, t0, t2)
         
         self.CheckEdge(e0)
         self.CheckEdge(e1)
         self.CheckEdge(e2)

    def CheckEdge(self, e):
        if e.locked: return False
        t0, t1 = e.t
        assert( t0.inside==t1.inside )

        v0, v2 = e.v
        e2, e3, v3 = self.GetAdjacentEdges(e, t0)
        e0, e1, v1 = self.GetAdjacentEdges(e, t1)
        if self.GetVertexPosition( v1, v3, v2)>=0 or self.GetVertexPosition( v1, v3, v0)<=0:
            return False

        cCount = 0
        if self.HasBoundingVertices( v0, v2, v3): cCount+=1
        if self.HasBoundingVertices( v2, v0, v1): cCount+=1
        a0 = t0.minAngle
        a1 = t1.minAngle
        cAngle = min(a0, a1) 

        pCount = 0
        if self.HasBoundingVertices( v1, v3, v0): pCount+=1
        if self.HasBoundingVertices( v3, v1, v2): pCount+=1

        a0, q0 = self.SetTriangleData( v1, v3, v0)
        a1, q1 = self.SetTriangleData( v3, v1, v2)
        pAngle = min(a0, a1)

        if pCount<cCount or pAngle>cAngle:
            self.SetTriangle( t0, v1, v3, v0, e, e3, e0)
            self.SetTriangle( t1, v3, v1, v2, e, e1, e2)
            
            self.SetEdge( e, v1, v3, t0, t1)
            self.FixEdge( e0, t1, t0)
            self.FixEdge( e2, t0, t1)
            
            self.CheckEdge( e0)
            self.CheckEdge( e1)
            self.CheckEdge( e2)
            self.CheckEdge( e3)
            return True 
        return False 

    def GetClosestVertex(self, x, y):
        dmin=0.0
        v=None
        
        for i in range(self.vertexCount):
            dx = self.Vertices[i].x - x
            dy = self.Vertices[i].y - y
            d2 = dx*dx + dy*dy
            if i==0 or d2<dmin :
                dmin    = d2
                v = self.Vertices[i]
        return(v)

    def MarkInsideTriangles(self, holes):
         rtn=tmE_OK
         
         if holes:
              self.DeleteTriangle(self.Triangles[1])
              for i in range(self.holeCount):
                   t = self.FindVertex(  self.Holes[i] )
                   if ( t==None ): rtn = tmE_HOLES
                   else:           self.DeleteTriangle(t)
         else:
              for i in range(self.triangleCount):
                   self.Triangles[i].inside = (self.Triangles[i].v[0] in self.Vertices[3:] and
                                               self.Triangles[i].v[1] in self.Vertices[3:] and
                                               self.Triangles[i].v[2] in self.Vertices[3:])
         return rtn

    def DeleteBadTriangles(self):
         tBad=None
         vc=tmVertex()
         
         while self.vertexCount < self.maxVertexCount:
              angle = tmC_BIGNUMBER
              
              for i in range(self.triangleCount):
                   t = self.Triangles[i]
                   if t.inside and t.angle < angle:
                       angle  = t.angle
                       tBad   = t
              
              if (self.options & tmO_MINIMALGRID) and (angle>=self.minAngle):
                  return
              
              self.CircumCenter(vc, tBad)
              
              isInside = False
              for i in range(self.segmentCount):
                   if self.ContainsVertex(self.Segments[i].v[0], self.Segments[i].v[1], vc):
                       self.SplitSegment( self.Segments[i])
                       isInside = True
              if not isInside:
                   v  = self.AddVertex()
                   if not v: return
                   v.x, v.y = vc.x, vc.y
                   self.InsertVertex( v)

    def FindVertex(self, v):
         # initialize
         t = self.lastTriangle
         if t==None: t = self.Triangles[1]
         # search 
         repeat = True
         while repeat:
             repeat = False
             for i in range(3):
                  v0 = t.v[i]
                  if i==2: v1 = t.v[0]
                  else:    v1 = t.v[i+1]
                  if self.GetVertexPosition(v0, v1, v) < 0:
                       e = t.e[i]
                       assert( (e.t[0]==t) or (e.t[1]==t) )
                       if   e.t[0]==t: t = e.t[1] 
                       elif e.t[1]==t: t = e.t[0]
                       repeat = True
                       break
         # found
         self.lastTriangle = t

         if t.inside:
             return t
         else:
             return None

    def ContainsVertex(self, v0, v1, v):
         cx = 0.5 * (v0.x + v1.x)
         cy = 0.5 * (v0.y + v1.y)
         dx = v1.x - cx
         dy = v1.y - cy
         r2 = dx*dx + dy*dy
         dx = v.x - cx
         dy = v.y - cy
         d2 = dx*dx + dy*dy
         return d2 < r2

    def GetVertexPosition(self, a, b, c):
         if c in self.Vertices[:3]:
              d1 = (b.x - a.x)*(c.y - a.y)
              d2 = (b.y - a.y)*(c.x - a.x)
         else:
              d1 = (a.x - c.x)*(b.y - c.y)
              d2 = (a.y - c.y)*(b.x - c.x)
         return d1-d2

    def GetSplitPosition(self, v, v0, v1):
        vt = tmVertex()
        if v1 in self.Vertices[:self.inputVertexCount]:
            v0, v1 = v1, v0

        if v0 in self.Vertices[:self.inputVertexCount]:
            dx = v1.x - v0.x
            dy = v1.y - v0.y
            d  = sqrt(dx*dx + dy*dy)
            # 1) p41
            f  = pow(2.0, floor(tmC_SQRT2 * log(0.5*d) + 0.5) )/d
            v.x   = v0.x + f*dx
            v.y   = v0.y + f*dy
        else :
            v.x = 0.5*(v0.x + v1.x)
            v.y = 0.5*(v0.y + v1.y)

    def SplitSegment(self, s):
         e = self.GetEdge( s.v[0], s.v[1])
         assert(e!=None)
         
         v0 = s.v[0]
         v1 = s.v[1]
         v = self.AddVertex()
         if not v: return
         
         t = self.AddSegment()
         self.SetSegment(s, v0, v)
         self.SetSegment(t, v,  v1)
         
         self.GetSplitPosition( v, v0, v1)
         self.InsertVertexAt( v, e)

    def InsertSegments(self):
        inserting = True
        
        while inserting:
            inserting = False
            for i in range(self.segmentCount):
                s  = self.Segments[i]
                v0 = s.v[0]
                v1 = s.v[1]
                
                e = self.GetEdge(v0, v1)
                if not e:
                     v = self.AddVertex()
                     if not v: return
                     t = self.AddSegment()
                     self.SetSegment(s, v0, v)
                     self.SetSegment(t, v, v1)
                     
                     self.GetSplitPosition( v, v0, v1)
                     self.InsertVertex( v)

                     inserting = True

                elif (self.ContainsVertex(e.v[0], e.v[1], self.GetOppositeVertex(e, e.t[0])) or
                      self.ContainsVertex(e.v[0], e.v[1], self.GetOppositeVertex(e, e.t[1]))):
                     self.SplitSegment(s)
                     inserting = True
  
            if self.vertexCount==self.maxVertexCount:
                self.options &= ~tmO_ENOUGHVERTICES
                return
        
        self.options |= tmO_ENOUGHVERTICES

    def SetSegment(self,s,v0,v1):
        s.v[0], s.v[1] = v0, v1

    def ConvexHull(self):
        for i in range(self.triangleCount):
            # Check all combinations
            for j in range(3):
                if j == 0: i0, i1, i2 = 0, 1, 2
                elif j==1: i0, i1, i2 = 1, 2, 0
                elif j==2: i0, i1, i2 = 2, 0, 1

                if (self.Triangles[i].v[i0] in self.Vertices[3:] and
                    self.Triangles[i].v[i1] in self.Vertices[3:] and
                    self.Triangles[i].v[i2] in self.Vertices[:3] and
                    self.GetSegment(self.Triangles[i].v[i0], self.Triangles[i].v[i1])==None):
                       s = self.AddSegment()
                       self.SetSegment(s, self.Triangles[i].v[i0], self.Triangles[i].v[i1])
        
    def Reset(self):
        self.Vertices         = []
        self.Edges            = []
        self.Triangles        = []
        self.Segments         = []

        self.vertexCount      = 0
        self.inputVertexCount = 0
        self.edgeCount        = 0
        self.triangleCount    = 0
        self.segmentCount     = 0
        self.holeCount        = 0

    def PrintData(self):
         print "Options    : %d" % (self.options)
         print "MinAngle   : %G" % (self.minAngle)
         print "Max V/E/T/S: %d %d %d %d" % (self.maxVertexCount,self.maxEdgeCount,self.maxTriangleCount,self.maxSegmentCount)
         print "    actual : %d %d %d %d %d" % (self.vertexCount,self.edgeCount, self.triangleCount, self.segmentCount, self.holeCount)
         print "self.Vertices   : %d" % (self.vertexCount)
         print "self.Segments   : %d" % (self.segmentCount)
         print "self.Triangles  : %d (total: %d)" % (self.insideTriangleCount,self.triangleCount)

def main():
    # the geometry-boundary to mesh, points in length units.
    # a ring
    #
    # node points
    nodes = ( ( 5.00,	 0.00), #  1 outer boundary
              ( 3.54,	 3.54), #  2
              ( 0.00,	 5.00), #  3
              (-3.54,	 3.54), #  4
              (-5.00,	 0.00), #  5
              (-3.54,	-3.54), #  6
              ( 0.00,	-5.00), #  7
              ( 3.54,	-3.54), #  8
              ( 2.00,	 0.00), #  9 inner boundary
              ( 1.41,	 1.41), # 10
              ( 0.00,	 2.00), # 11
              (-1.41,	 1.41), # 12
              (-2.00,	 0.00), # 13
              (-1.41,	-1.41), # 14
              ( 0.00,	-2.00), # 15
              ( 1.41,	-1.41)) # 16

    nodes = [tmVertex(node) for node in nodes]

    # center hole point
    holes = [ tmVertex( (0.0, 0.0) ) ]
    # center hole boundary segments
    segs = (  ( 9, 10),
              (10, 11),
              (11, 12),
              (12, 13),
              (13, 14),
              (14, 15),
              (15, 16),
              (16,  9))

    segs = [tmSegmentId(seg) for seg in segs]

    # go
    md = TriangleMesh()
    md.Mesh(nodes, len(nodes), segs, len(segs), holes, len(holes))

    # show some minimal stats
    md.PrintData()

if __name__=="__main__":
     main()
