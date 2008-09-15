#!/usr/bin/python
#
# Python version Copyright (c) 2008 kne / sirkne at gmail dot com
# ported from Blaze http://www.dsource.org/projects/blaze/
#
# Original header:
#
# Copyright (c) 2008 Rene Schulte. http:#www.rene-schulte.info/
# Authors: Blaze team, see AUTHORS file
# Maintainers: Mason Green (zzzzrrr)
# License:
# zlib/png license
#
# NOTE - It is highly suggested that you use Meters-Kilogram-Seconds
# (MKS) units. Pay attention to your mass, friction, and restitution
# values. SPH requires fine tuning.
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
import random
from math import sqrt

# Max number of particles 
MAX_PARTICLES = 100
DENSITY_OFFSET = 100.0
GAS_CONSTANT = 0.1
VISCOSCITY = 0.002
CELL_SPACE = 15.0 / 64.0

def get_bodies(world):
    body = world.GetBodyList()
    while body:
        yield body
        body = body.GetNext()

def get_shapes(body):
    shape = body.GetShapeList()
    while shape:
        yield shape.getAsType()
        shape = shape.GetNext()

def get_all_shapes(world):
    for body in get_bodies(world):
        for shape in get_shapes(body):
            yield shape

def randomRange(low,high):
    return random.random() * (high - low) + low

class smoothingKernel(object):
    factor=0
    kernelSize=0
    kernelSizeSq=0
    kernelSize3=0
    
    # Initializes a new instance of the SmoothingKernel class.
    # kernelSize: Size of the kernel.
    def __init__(self, kernelSize=1.0):
        self.factor = 1.0
        self.kernelSize = kernelSize
        self.kernelSizeSq = kernelSize ** 2
        self.kernelSize3 = kernelSize ** 3
        self.calculateFactor()
    
    def calculateFactor(self): pass
    def calculate(self, distance): pass
    def calculateGradient(self, distance): pass
    def calculateLaplacian(self, distance): pass

class SKViscosity (smoothingKernel):
    def __init__(self, kernelSize=1.0):
        super(SKViscosity, self).__init__(kernelSize)
    
    def calculateFactor(self):
        self.factor = (15.0 / (2.0 * box2d.b2_pi * self.kernelSize3))
    
    def calculate(self, distance):
        lenSq = distance.LengthSquared()
        if lenSq > self.kernelSizeSq:
            return 0.0
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        len = sqrt(lenSq)
        len3 = len * len * len
        return self.factor * (((-len3 / (2.0 * self.kernelSize3)) + (lenSq / self.kernelSizeSq) + (self.kernelSize / (2.0 * len))) - 1.0)
    
    def calculateLaplacian(self, distance):
        lenSq = distance.LengthSquared()
        if lenSq > self.kernelSizeSq:
            return 0.0
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        len = sqrt(lenSq)
        return self.factor * (6.0 / self.kernelSize3) * (self.kernelSize - len)
    
    def calculateGradient(self, distance):
        raise Exception("Net yet implemented!")

class SKSpiky (smoothingKernel):
    def __init__(self, kernelSize=1.0):
        super(SKSpiky, self).__init__(kernelSize)
    
    def calculateFactor(self):
        kernelRad6 = pow(self.kernelSize, 6.0)
        self.factor = (15.0 / (box2d.b2_pi * kernelRad6))
    
    def calculate(self, distance):
        lenSq = distance.LengthSquared()
        
        if lenSq > self.kernelSizeSq:
            return 0.0
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        f = self.kernelSize - sqrt(lenSq)
        return self.factor * f * f * f
    
    def calculateGradient(self, distance):
        lenSq = distance.LengthSquared()
        if lenSq > self.kernelSizeSq:
            return box2d.b2Vec2(0.0, 0.0)
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        len = sqrt(lenSq)
        f = -self.factor * 3.0 * (self.kernelSize - len) * (self.kernelSize - len) / len
        return box2d.b2Vec2(distance.x * f, distance.y * f)
    
    def calculateLaplacian(self, distance):
        raise Exception("Not yet implemented!")

class SKPoly6(smoothingKernel):
    def __init__(self, kernelSize=1.0):
        super(SKPoly6, self).__init__(kernelSize)
    
    def calculateFactor(self):
        kernelRad9 = pow(self.kernelSize, 9.0)
        self.factor = (315.0 / (64.0 * box2d.b2_pi * kernelRad9))
    
    def calculate(self, distance):
        lenSq = distance.LengthSquared()
        if lenSq > self.kernelSizeSq:
            return 0.0
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        
        diffSq = self.kernelSizeSq - lenSq
        return self.factor * diffSq * diffSq * diffSq
    
    def calculateGradient(self, distance):
        lenSq = distance.LengthSquared()
        if lenSq > self.kernelSizeSq:
            return box2d.b2Vec2(0.0, 0.0)
        if lenSq < box2d.FLT_EPSILON:
            lenSq = box2d.FLT_EPSILON
        diffSq = self.kernelSizeSq - lenSq
        f = -self.factor * 6.0 * diffSq * diffSq
        return box2d.b2Vec2(distance.x * f, distance.y * f)
    
    def calculateLaplacian(self, distance):
        raise Exception("Net yet implemented!")


class FluidParticle(object):
    velocity=None
    position=None
    positionOld=None
    mass=0.0
    massInv=0.0
    density=0.0
    force=None
    pressure=0.0
    neighbors=[]
    gridSize=0.0
    margin=0.0 #static
    friction = 0.0
    restitution = 0.0
    aabb = None

    # Constructor
    def __init__(self, position, restitution, friction):
        super(FluidParticle, self).__init__()
        self.velocity=box2d.b2Vec2(0.0,0.0)
        self.force=box2d.b2Vec2(0.0,0.0)
        self.aabb = box2d.b2AABB()

        self.restitution = restitution
        self.friction = friction
        self.setMass(1.25)
        self.gridSize = CELL_SPACE * 1.25
        self.margin = 0.01
        self.position = position.copy()
        self.positionOld = position.copy()
        self.density = DENSITY_OFFSET
        self.updatePressure()
    
    def __repr__(self):
        return "(%s)" % self.ID

    # Updates the self.pressure using a modified ideal gas state equation
    # (see the paper "Smoothed particles: A new paradigm for animating highly deformable bodies." by Desbrun)
    def updatePressure(self):
        self.pressure = GAS_CONSTANT * (self.density - DENSITY_OFFSET)
    
    # Updates the particle.
    def update(self, step, gravity):
        acceleration = self.force * self.massInv + gravity
        
        # Vertlet integration
        damping = 0.01
        oldPos=self.position.copy()
        # Position = Position + (1.0 - Damping) * (Position - PositionOld) + dt * dt * a
        acceleration *= (step * step)
        t = self.position - self.positionOld
        t *= (1.0 - damping)
        t += acceleration
        self.position += t
        self.positionOld = oldPos
        
        # calculate velocity
        # Velocity = (Position - PositionOld) / dt
        t = self.position - self.positionOld
        self.velocity = t * 1.0 / step
    
    # Update the AABB */
    def updateAABB(self):
        self.aabb.lowerBound.x = self.position.x - self.gridSize
        self.aabb.lowerBound.y = self.position.y - self.gridSize
        self.aabb.upperBound.x = self.position.x + self.gridSize
        self.aabb.upperBound.y = self.position.y + self.gridSize
    
    def setMass(self, mass):
        self.mass = mass
        if mass > 0.0:
            self.massInv = 1.0 / mass
        else:
            self.massInv = 0.0
    
    def addNeighbor(self, ID):
        if ID not in self.neighbors:
            self.neighbors.append(ID)
    
    def addForce(self, force):
        self.force += force
    
    def containsPoint(self, v):
        return False
    
    def calculateInertia(self, m, offset):
        return 0.0
    
    def applyImpulse(self, penetration, penetrationNormal, rest, fric):
        # Handle collision
        # Calc new velocity using elastic collision with friction
        # . Split oldVelocity in normal and tangential component, revert normal component and add it afterwards
        # v = pos - oldPos
        #vn = n * Vector2.Dot(v, n) * -Bounciness
        #vt = t * Vector2.Dot(v, t) * (1.0 - Friction)
        #v = vn + vt
        #oldPos = pos - v

        v = self.position - self.positionOld
        tangent=box2d.b2Vec2(0.0,0.0)
        dp = v.dot(penetrationNormal)
        vn = penetrationNormal * dp * -rest
        dp = v.dot(tangent)
        vt = tangent * dp * (1.0 - fric)
        v = vn + vt

        self.position -= penetration
        self.positionOld = self.position - v

    def applyBuoyancyForce(self, body):
        # Apply buoyancy force to body
        angDrag = 0.25
        linDrag = 0.75
           
        f = self.force * linDrag
        r = self.position - body.GetPosition()

        # apply the force
        body.ApplyForce(f, body.GetWorldCenter())

        # apply the real torque
        torque = r.x * f.y * angDrag - r.y * f.x * angDrag
        body.ApplyTorque(torque)
        
    def computeSweptAABB(self,xf1,xf2):
        updateAABB()
    
    def updateSweepRadius(self, center):
        pass
    def computeMass(self, massData):
        pass
    def computeAABB(self, aabb, xf):
        pass
    def testSegment(xf, lambda_,  normal, segment, maxLambda):
        return SegmentCollide.MISS
    def testPoint(self, xf, p):
        return False

# Implementation of a SPH-based fluid simulation
class SPHSimulation(object):
    cellSpace = 0.0
    SKGeneral = None
    SKPressure = None
    SKViscos = None
    Viscosity = 0.0
    particles = []
    aabb = box2d.b2AABB()
    world = None
    def __init__(self, world):
        self.cellSpace = CELL_SPACE
        self.Viscosity = VISCOSCITY
        self.SKGeneral = SKPoly6(self.cellSpace)
        self.SKPressure= SKSpiky(self.cellSpace)
        self.SKViscos = SKViscosity(self.cellSpace)
        self.world = world

    # Add particle to simulation 
    def addParticle(self, particle):
        particle.ID = len(self.particles)
        self.particles.append(particle)

    # Remove particle from simulation 
    def removeParticle(self, particle):
       self.particles.remove(particle)

    # Return float of self.particles 
    def numParticles(self):
        return len(self.particles)

    # Return particle list 
    def getParticle(self):
        return self.particles

    # Reset force 
    def resetForce(self):
        for p in self.particles: 
            p.force = box2d.b2Vec2(0.0,0.0)

    def shellSort(self, shapes):
        increment = len(shapes) / 2
        while (increment > 0):
            for i in range(len(shapes)):
                j = i
                temp = shapes[i]
                while ((j >= increment) and (shapes[j - increment].aabb.lowerBound.x > temp.aabb.lowerBound.x)):
                    shapes[j] = shapes[j - increment]
                    j = j - increment
                shapes[j] = temp
            if increment == 2:
                increment = 1
            else:
                increment = int(increment * 0.45454545)
        return shapes

    def updateNeighbors(self, world):
        shapes = self.shellSort(list(self.particles))

        for i in range(len(shapes)):
            for j in range(i+1, len(shapes)):
                s1, a1 = shapes[i], shapes[i].aabb
                s2, a2 = shapes[j], shapes[j].aabb

                if a2.lowerBound.x > a1.upperBound.x:
                    break

                # Particle-particle collisions
                if box2d.b2AABBOverlaps(a1, s2.position):
                    s1.addNeighbor(s2.ID)
                if box2d.b2AABBOverlaps(a2, s1.position):
                    s2.addNeighbor(s1.ID)
        
    # Simulates the specified self.particles.
    # self.particles The self.particles.
    # gravity The gravity.
    # dTime The time step.
    def update(self,world,step,gravity):
        for particle in self.particles:
            particle.neighbors=[particle.ID]

        self.updateNeighbors(world)
        self.calculatePressureAndDensities()
        self.calculateForces()
        self.updateParticles(step, gravity)
        self.checkParticleDistance()

        for particle in self.particles:
            particle.updateAABB()
        self.updateAABB()

    # Calculates the pressure and densities.
    # particles The particles.
    # grid The grid.
    def calculatePressureAndDensities(self):
        for particle in self.particles:
            particle.density = 0.0
            for nId in particle.neighbors:
                neighbor = self.particles[nId]
                dist = particle.position - neighbor.position
                particle.density += (particle.mass * self.SKGeneral.calculate(dist))
            particle.updatePressure()

    # Calculates the pressure and viscosity forces.
    def calculateForces(self):
        for particle in self.particles:
            pId = self.particles.index(particle)
            for nId in particle.neighbors[1:pId]:
                neighbor = self.particles[nId]
                if neighbor.density > box2d.FLT_EPSILON:
                    dist = particle.position - neighbor.position
                    # pressure
                    scalar = neighbor.mass * (particle.pressure + neighbor.pressure) / (2.0 * neighbor.density)
                    force = self.SKPressure.calculateGradient(dist)
                    force *= scalar
                    particle.force -= force
                    neighbor.force += force
                    
                    # viscosity
                    scalar = neighbor.mass * self.SKViscos.calculateLaplacian(dist) * self.Viscosity * 1.0 / neighbor.density
                    force = neighbor.velocity - particle.velocity
                    force *= scalar
                    particle.force += force
                    neighbor.force -= force

    # Updates the particles positions using integration and clips them to the domain space.
    def updateParticles(self, step, gravity):
        # Update velocity + position using forces
        for particle in self.particles:
            particle.update(step, gravity)
            if not self.world.InRange(particle.aabb):
                print "Left world", particle

    # Checks the distance between the particles and corrects it, if they are too near.
    def checkParticleDistance(self):
        minDist = 0.5 * self.cellSpace
        minDistSq = minDist ** 2
        for particle in self.particles:
            pId = self.particles.index(particle)
            for nId in particle.neighbors[1:]:
                neighbor = self.particles[nId]
                dist = neighbor.position - particle.position
                distLenSq = dist.LengthSquared()
                if distLenSq < minDistSq:
                    if distLenSq > box2d.FLT_EPSILON:
                        distLen = sqrt(distLenSq)
                        dist *= 0.5 * (distLen - minDist) / distLen
                        neighbor.position -= dist
                        neighbor.positionOld -= dist
                        particle.position += dist
                        particle.positionOld += dist
                    else:
                        diff = 0.5 * minDist
                        neighbor.position.y -= diff
                        neighbor.positionOld.y -= diff
                        particle.position.y += diff
                        particle.positionOld.y += diff

    def collideCircleFluid(self, circle, particle):
        xf1 = circle.GetBody().GetXForm()

        p1 = box2d.b2Mul(xf1, circle.GetLocalPosition())
        p2 = particle.position
        normal=box2d.b2Vec2(0.0,0.0)

        d = p2 - p1
        distSqr = d.LengthSquared()
        r1 = circle.GetRadius()
        r2 = 0.0
        radiusSum = r1 + r2
        if distSqr > radiusSum * radiusSum:
            return False, None, None

        if distSqr < box2d.FLT_EPSILON:
            separation = -radiusSum
            normal.set(0.0, 1.0)
        else:
            dist = sqrt(distSqr)
            separation = dist - radiusSum
            a = 1.0 / dist
            normal.x = a * d.x
            normal.y = a * d.y

        penetration = normal * separation
        penetrationNormal = normal
        return True, penetration, penetrationNormal

    def collidePolyFluid(self, polygon, particle):
        xf1 = polygon.GetBody().GetXForm()
        xf2 = box2d.b2XForm()
        xf2.position = particle.position

        # Compute circle position in the frame of the polygon.
        c = box2d.b2Mul(xf2, box2d.b2Vec2_zero)
        cLocal = box2d.b2MulT(xf1, c)

        # Find the min separating edge.
        normalIndex = 0
        separation = -box2d.B2_FLT_MAX
        radius = particle.margin
        vertices = polygon.getVertices_b2Vec2()
        normals = polygon.getNormals_b2Vec2()
        vertexCount = len(vertices)

        for i in range(vertexCount):
            s = box2d.b2Dot(normals[i], cLocal - vertices[i])
            if s > radius:
                # Early out.
                return False, None, None
            elif s > separation:
                separation = s
                normalIndex = i

        if separation == -box2d.B2_FLT_MAX: # was causing crashes without this!
            return False, None, None

        # If the center is inside the polygon ...
        if separation < box2d.FLT_EPSILON:
            penetrationNormal = box2d.b2Mul(xf1.R, normals[normalIndex])
            separation = separation - radius
            penetration = penetrationNormal * separation
            return True, penetration, penetrationNormal

        # Project the circle center onto the edge segment.
        vertIndex1 = normalIndex
        vertIndex2 = vertIndex1 + 1
        if vertIndex2 >= vertexCount: vertIndex2=0

        e = vertices[vertIndex2] - vertices[vertIndex1]

        length = e.Normalize()
        assert(length > box2d.FLT_EPSILON)

        # Project the center onto the edge.
        u = box2d.b2Dot(cLocal - vertices[vertIndex1], e)
        if u <= 0.0:
            p = vertices[vertIndex1]
        elif u >= length: 
            p = vertices[vertIndex2]
        else:
            p = vertices[vertIndex1] + u * e

        d = cLocal - p
        dist = d.Normalize()
        if dist > radius:
            return False, None, None

        penetrationNormal = box2d.b2Mul(xf1.R, d)
        separation = dist - radius
        penetration = penetrationNormal * separation
        return True, penetration, penetrationNormal

    def checkCollideShape(self, shape, particle):
        restitution = particle.restitution * shape.GetRestitution()
        friction = particle.friction * shape.GetFriction()

        # python version: (20fps)
        if False:
            if shape.GetType()==box2d.e_circleShape:
                collide, penetration, penetrationNormal = self.collideCircleFluid(shape, particle)
            else:
                collide, penetration, penetrationNormal = self.collidePolyFluid(shape, particle)
        else:
            # c++ version, built into pybox2d: (30+fps)
            if shape.GetType()==box2d.e_circleShape:
                collide, penetration, penetrationNormal = box2d.collideCircleParticle(shape, particle.position)
            else:
                collide, penetration, penetrationNormal = box2d.b2CollidePolyParticle(shape, particle.position, particle.margin)

        if not collide:
            return

        particle.applyImpulse(penetration, penetrationNormal, restitution, friction)
        particle.applyBuoyancyForce(shape.GetBody())

    def checkShape(self, shape):
        aabb = box2d.b2AABB()
        shape.ComputeAABB(aabb, shape.GetBody().GetXForm())

        for particle in self.particles:
            if box2d.b2AABBOverlaps(particle.aabb, aabb):
                self.checkCollideShape(shape, particle)

    def updateAABB(self):
        # okay, so it's a really lame way of doing this. but i'm lazy.
        if len(self.particles) == 0:
            return

        xpos = []
        ypos = []
        for particle in self.particles:
            xpos.append(particle.position.x)
            ypos.append(particle.position.y)

        self.aabb.lowerBound.Set(min(xpos), min(ypos))
        self.aabb.upperBound.Set(max(xpos), max(ypos))

class fluiDemo (Framework):
    name="fluiDemo"
    # The particle field gravity 
    gravity=None
    # Grid cell space 
    cellSpace=0.0
    #  restitution 
    restitution = 0.1
    # Friction coefficient 
    friction = 0.75
    # Max particle flag 
    full=False
    # Number of particles
    numParticles=0
    # Main simulation class instance
    sim = None
    viewZoom = 45.0
    steps=0

    def __init__(self):
        super(fluiDemo, self).__init__()
        gravity = box2d.b2Vec2(0.0, -9.81)
        self.world.SetGravity(gravity)

        random.seed(0) # make the tests all the same ###test###
        # Initialize the SPH simulator
        self.sim = SPHSimulation(self.world)

        # Create house
        position = box2d.b2Vec2(5.50, 1.5)
        angle = 0.0
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        rBody = self.world.CreateBody(bd)
        sd = box2d.b2PolygonDef()
        sd.friction = self.friction
        sd.restitution = self.restitution
        sd.SetAsBox(0.75, 1.0)
        sd.density = 10
        rBody.CreateShape(sd)
        rBody.SetMassFromShapes()
        rBody.SetUserData("HouseBase")
        
        # Create right roof
        position = box2d.b2Vec2(5.5, 4.1)
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        rBody = self.world.CreateBody(bd)
        density = 10
        sd = box2d.b2PolygonDef()
        bodyVertex = [ box2d.b2Vec2(0.5, -0.275), box2d.b2Vec2(-0.25, 0.25), box2d.b2Vec2(-0.25, -0.275) ]
        sd.setVertices_b2Vec2(bodyVertex)
        sd.density=density
        sd.friction = self.friction
        sd.restitution = self.restitution
        rBody.CreateShape(sd)
        rBody.SetMassFromShapes()
        rBody.SetUserData("RightRoof")
        
        # Create left roof
        position = box2d.b2Vec2(5.5, 4.1)
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        rBody = self.world.CreateBody(bd)
        bodyVertex = [ box2d.b2Vec2(0.25, -0.275), box2d.b2Vec2(0.25, 0.25), box2d.b2Vec2(-0.5, -0.275) ]
        sd = box2d.b2PolygonDef()
        sd.setVertices_b2Vec2(bodyVertex)
        sd.density=density
        sd.friction = self.friction
        sd.restitution = self.restitution
        rBody.CreateShape(sd)
        rBody.SetMassFromShapes()
        rBody.SetUserData("LeftRoof")
        
        # Create ball
        position = box2d.b2Vec2(3.0, 3.0)
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        rBody = self.world.CreateBody(bd)
        radius = 0.3
        density = 7.5
        sd = box2d.b2CircleDef()
        sd.density=density
        sd.radius=radius
        sd.friction = self.friction
        sd.restitution = self.restitution
        rBody.CreateShape(sd)
        rBody.SetMassFromShapes()
        rBody.SetUserData("Ball")
        
        # Create floor
        position = box2d.b2Vec2_zero
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle

        floor = self.world.CreateBody(bd)
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(30,0.5)
        sd.friction = self.friction
        floor.CreateShape(sd)
        floor.SetUserData("Floor")
        
        # Create left wall
        position = box2d.b2Vec2(0, 0.5)
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        leftWall = self.world.CreateBody(bd)
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 6)
        sd.friction = self.friction
        leftWall.CreateShape(sd)
        leftWall.SetUserData("Leftwall")
        
        # Create right wall
        position = box2d.b2Vec2(10.0, 0.5)
        bd = box2d.b2BodyDef()
        bd.position = position
        bd.angle = angle
        rightWall = self.world.CreateBody(bd)
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(0.5, 6)
        sd.friction = self.friction
        rightWall.CreateShape(sd)
        rightWall.SetUserData("Rightwall")

    def Step(self, settings) :
        if not settings.pause:
            self.steps += 1
            if self.steps % 2 == 0 and not self.full:
                # Create particle
                self.restitution = 0.01
                self.friction = 0.5
                x = randomRange(5.0, 6.0)
                position = box2d.b2Vec2(x, 4.0)
                particle = FluidParticle(position, self.restitution, self.friction)
                fx = randomRange(-300, 300)
                particle.force = box2d.b2Vec2(fx, 0.0)
                self.sim.addParticle(particle)
                if self.sim.numParticles() > MAX_PARTICLES:
                    self.full = True

            self.sim.update(self.world, 1.0/settings.hz, self.world.GetGravity())

            for shape in get_all_shapes(self.world):
                self.sim.checkShape(shape)

            self.sim.resetForce()

        super(fluiDemo, self).Step(settings)

        if self.sim.particles:
            for particle in self.sim.particles:
                self.debugDraw.DrawPoint(particle.position, 2.0, box2d.b2Color(0.2, 0.4, 1.0))
            for nId in self.sim.particles[-1].neighbors + [len(self.sim.particles)-1]:
                particle = self.sim.particles[nId]
                self.debugDraw.DrawPoint(particle.position, 2.0, box2d.b2Color(1.0, 0.0, 0.0))
                #self.debugDraw.DrawAABB(particle.aabb, (particle.ID/MAX_PARTICLES*255,255,255)) 

        #self.debugDraw.DrawAABB(self.sim.aabb, (255,255,255)) 

        self.DrawString(5, self.textLine, "Particle count: %d" % self.sim.numParticles())
        self.textLine += 15

if __name__=="__main__":
    test = fluiDemo()
    test.run()
