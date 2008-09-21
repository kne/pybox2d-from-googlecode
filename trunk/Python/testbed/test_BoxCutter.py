#!/usr/bin/python
#
# Original C++ version by Daid 
#  http://www.box2d.org/forum/viewtopic.php?f=3&t=1473
#
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

from test_main import *
class BoxCutter (Framework):
    name="BoxCutter"
    laserBody=None
    def __init__(self):
        super(BoxCutter, self).__init__() 

        self.world.GetGroundBody().SetUserData("ground")
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, -10.0)
        bd.userData = "ground1"
        ground = self.world.CreateBody(bd)
        
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)
    
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 50.0)
        bd.userData = "ground2"
        ground = self.world.CreateBody(bd)
        
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(50.0, 10.0)
        ground.CreateShape(sd)
    
        bd=box2d.b2BodyDef()
        bd.position.Set(0.0, 1.0)
        bd.userData = "laser"
        self.laserBody = self.world.CreateBody(bd)
        
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(5.0, 1.0)
        sd.density = 4.0
        self.laserBody.CreateShape(sd)
        self.laserBody.SetMassFromShapes()
    
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(3.0, 3.0)
        sd.density = 5.0
        
        bd=box2d.b2BodyDef()
        bd.userData = 1
        bd.position.Set(0.0, 8.0)
        body1 = self.world.CreateBody(bd)
        body1.CreateShape(sd)
        body1.SetMassFromShapes()
    
        sd=box2d.b2PolygonDef()
        sd.SetAsBox(3.0, 3.0)
        sd.density = 5.0
        
        bd=box2d.b2BodyDef()
        bd.userData = 1
        bd.position.Set(0.0, 8.0)
        body1 = self.world.CreateBody(bd)
        body1.CreateShape(sd)
        body1.SetMassFromShapes()
    
    def Cut(self):
        segmentLength = 30.0
        
        segment1=box2d.b2Segment()
        segment2=box2d.b2Segment()
        
        laserStart=box2d.b2Vec2(5.0-0.1,0.0)
        laserDir=box2d.b2Vec2(segmentLength,0.0)
        
        segment1.p1 = self.laserBody.GetWorldPoint(laserStart)
        segment1.p2 = self.laserBody.GetWorldVector(laserDir)
        segment1.p2+= segment1.p1
        
        segment2.p1 = segment1.p2
        segment2.p2 = segment1.p1
        
        lambda_,normal,shape1 = self.world.RaycastOne(segment1,False,None)
        if not shape1:
            return
        
        laserColor=box2d.b2Color(0,1.0,0)
        
        hitLoc1 = (1-lambda_)*segment1.p1+lambda_*segment1.p2
        
        laserColor.g = 0.5
        
        #Finding the exit point can be done better I guess. But that's not the main problem.
        shape2 = None
        while shape1 != shape2:
            lambda_,normal,shape2 = self.world.RaycastOne(segment2,False,None)
            if not shape2:
                return
            hitLoc2 = (1-lambda_)*segment2.p1+lambda_*segment2.p2
            
            self.debugDraw.DrawSegment(segment2.p1,(1-lambda_)*segment2.p1+lambda_*segment2.p2,laserColor)
            lambda_ += box2d.B2_FLT_EPSILON #Enter the shape a bit.
            
            segment2.p1 = (1-lambda_)*segment2.p1+lambda_*segment2.p2
        
        b = shape1.GetBody()
        if b.GetUserData() != 1 and shape1.GetType() == box2d.e_polygonShape:	#Check if we are a cutable shape.
            return

        shape = shape1.getAsType()
        
        #Beh, difficult job of defining the new shapes.
        pd=[box2d.b2PolygonDef(), box2d.b2PolygonDef()]
        pd[0].density = 5.0
        pd[1].density = 5.0
        
        localHitLoc1 = b.GetLocalPoint(hitLoc1)
        localHitLoc2 = b.GetLocalPoint(hitLoc2)
        vertices = shape.getVertices_b2Vec2()
        cutAdded = [0,0]
        last = -1
        for i in range(shape.GetVertexCount()):
            #Find out if this vertex is on the old or new shape.
            if box2d.b2Dot(box2d.b2Cross(localHitLoc2-localHitLoc1, 1), vertices[i]-localHitLoc1) > 0:
                n = 0
            else:
                n = 1
            if last != n:
                #If we switch from one shape to the other add the cut vertices.
                if last == 0:
                    assert(not cutAdded[0])
                    cutAdded[0] = 1
                    pd[last].setVertex(pd[last].vertexCount, localHitLoc2)
                    pd[last].vertexCount+=1
                    pd[last].setVertex(pd[last].vertexCount, localHitLoc1)
                    pd[last].vertexCount+=1
                elif last == 1:
                    assert(not cutAdded[last])
                    cutAdded[last] = 1
                    pd[last].setVertex(pd[last].vertexCount, localHitLoc1)
                    pd[last].vertexCount+=1
                    pd[last].setVertex(pd[last].vertexCount, localHitLoc2)
                    pd[last].vertexCount+=1
            pd[n].setVertex(pd[n].vertexCount, vertices[i])
            pd[n].vertexCount+=1
            last = n
        
        #Add the cut in case it has not been added yet.
        if (not cutAdded[0]) :
            pd[last].setVertex(pd[last].vertexCount, localHitLoc2)
            pd[last].vertexCount+=1
            pd[last].setVertex(pd[last].vertexCount, localHitLoc1)
            pd[last].vertexCount+=1
        if (not cutAdded[1]) :
            pd[last].setVertex(pd[last].vertexCount, localHitLoc1)
            pd[last].vertexCount+=1
            pd[last].setVertex(pd[last].vertexCount, localHitLoc2)
            pd[last].vertexCount+=1
        
        #Check if the new shapes are not too tiny.
        for n in range(2):
            for i in range(pd[n].vertexCount):
                for j in range(pd[n].vertexCount):
                    if i != j and (pd[n].getVertex(i) - pd[n].getVertex(j)).Length() < 0.1:
                        return

        # Make sure the shapes are valid before creation
        try:
            box2d.b2PythonCheckPolygonDef(pd[0])
            box2d.b2PythonCheckPolygonDef(pd[1])
        except ValueError, s:
            print "Created bad shape:", s
            return

        b.DestroyShape(shape1)
        b.CreateShape(pd[0])
        b.SetMassFromShapes()
        b.WakeUp()
        
        bd=box2d.b2BodyDef()
        bd.userData = 1
        bd.position = b.GetPosition()
        bd.angle = b.GetAngle()
        newBody = self.world.CreateBody(bd)
        newBody.CreateShape(pd[1])
        newBody.SetMassFromShapes()
    
    def Keyboard(self, key):
        if key==K_c:
            self.Cut()
    
    def CutDraw(self):
        segment1=box2d.b2Segment()
        segment2=box2d.b2Segment()

        segmentLength = 30.0
        
        laserStart=box2d.b2Vec2(5.0-0.1,0.0)
        laserDir=box2d.b2Vec2(segmentLength,0.0)
        
        segment1.p1 = self.laserBody.GetWorldPoint(laserStart)
        segment1.p2 = self.laserBody.GetWorldVector(laserDir)
        segment1.p2+= segment1.p1
        
        segment2.p1 = segment1.p2
        segment2.p2 = segment1.p1
        
        lambda_,normal,shape1 = self.world.RaycastOne(segment1,False,None)
        
        laserColor=box2d.b2Color(0,1.0,0)
        
        if not shape1:
            return

        hitLoc1 = (1-lambda_)*segment1.p1+lambda_*segment1.p2
        hitLoc2 = None
        shape2 = None
        while shape1 != shape2:
            lambda_,normal,shape2 = self.world.RaycastOne(segment2,False,None)
            if not shape2:
                return
            hitLoc2 = (1-lambda_)*segment2.p1+lambda_*segment2.p2
            lambda_ += box2d.B2_FLT_EPSILON #Enter the shape a bit.
            
            segment2.p1 = (1-lambda_)*segment2.p1+lambda_*segment2.p2

        self.debugDraw.DrawPoint(hitLoc1, 5.0,box2d.b2Color(0.0,1.0,0.0))
        self.debugDraw.DrawPoint(hitLoc2, 5.0,box2d.b2Color(0.0,1.0,0.0))
        self.debugDraw.DrawSegment(hitLoc1, hitLoc2,laserColor)
    
    def Step(self, settings):
        super(BoxCutter, self).Step(settings)
    
        self.DrawString(5, self.textLine, "Keys: Cut = c")
        self.textLine += 15

        segmentLength = 30.0
        
        segment=box2d.b2Segment()
        laserStart=box2d.b2Vec2(5.0-0.1,0.0)
        laserDir=box2d.b2Vec2(segmentLength,0.0)
        segment.p1 = self.laserBody.GetWorldPoint(laserStart)
        segment.p2 = self.laserBody.GetWorldVector(laserDir)
        segment.p2+=segment.p1
        
        for rebounds in range(10):
            lambda_,normal,shape  = self.world.RaycastOne(segment,False,None)
            
            laserColor=box2d.b2Color(1.0,0,0)
            
            if shape:
                self.debugDraw.DrawSegment(segment.p1,(1-lambda_)*segment.p1+lambda_*segment.p2,laserColor)
            else:
                self.debugDraw.DrawSegment(segment.p1,segment.p2,laserColor)
                break

            #Bounce
            segmentLength *=(1-lambda_)
            if segmentLength<=box2d.B2_FLT_EPSILON:
                break
            laserStart = (1-lambda_)*segment.p1+lambda_*segment.p2
            laserDir = segment.p2-segment.p1
            laserDir.Normalize()
            laserDir = laserDir -2 * box2d.b2Dot(laserDir,normal) * normal
            segment.p1 = laserStart-0.1*laserDir
            segment.p2 = laserStart+segmentLength*laserDir
        
        self.CutDraw()

if __name__=="__main__":
    main(BoxCutter)
