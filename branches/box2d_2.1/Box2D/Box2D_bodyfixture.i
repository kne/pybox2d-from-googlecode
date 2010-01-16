/*
* pybox2d -- http://pybox2d.googlecode.com
*
* Copyright (c) 2010 Ken Lauer / sirkne at gmail dot com
* 
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
* 1. The origin of this software must not be misrepresented; you must not
* claim that you wrote the original software. If you use this software
* in a product, an acknowledgment in the product documentation would be
* appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
* misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/

/**** BodyDef ****/
%extend b2BodyDef {
public:        
    %pythoncode %{
        fixtures = None
    %}
}

/**** FixtureDef ****/
%extend b2FixtureDef {
public:        
    %pythoncode %{
    %}
}

/**** Fixture ****/
%extend b2Fixture {
public:
    long __hash__() { return (long)self; }
    /* This destructor is ignored by SWIG, but it stops the erroneous
    memory leak error. Will have to test with older versions of SWIG
    to ensure this is ok (tested with 1.3.40)
    */
    ~b2Fixture() {
    }

    %pythoncode %{
        __eq__ = b2FixtureCompare
        __ne__ = lambda self,other: not b2FixtureCompare(self,other)

        # Read-write properties
        friction = property(__GetFriction, __SetFriction)
        restitution = property(__GetRestitution, __SetRestitution)
        filterData = property(__GetFilterData, __SetFilterData)
        sensor = property(__IsSensor, __SetSensor)
        density = property(__GetDensity, __SetDensity)

        # Read-only
        next = property(__GetNext, None)
        type = property(__GetType, None)
        massData = property(__GetMassData, None)
        shape = property(__GetShape, None)
        aABB = property(__GetAABB, None)
        body = property(__GetBody, None)

    %}
}

%rename(__GetNext) b2Fixture::GetNext;
%rename(__GetFriction) b2Fixture::GetFriction;
%rename(__GetRestitution) b2Fixture::GetRestitution;
%rename(__GetFilterData) b2Fixture::GetFilterData;
%rename(__IsSensor) b2Fixture::IsSensor;
%rename(__GetType) b2Fixture::GetType;
%rename(__GetMassData) b2Fixture::GetMassData;
%rename(__GetShape) b2Fixture::GetShape;
%rename(__GetAABB) b2Fixture::GetAABB;
%rename(__GetDensity) b2Fixture::GetDensity;
%rename(__GetBody) b2Fixture::GetBody;
%rename(__SetSensor) b2Fixture::SetSensor;
%rename(__SetDensity) b2Fixture::SetDensity;
%rename(__SetFilterData) b2Fixture::SetFilterData;
%rename(__SetFriction) b2Fixture::SetFriction;
%rename(__SetRestitution) b2Fixture::SetRestitution;

/**** Body ****/
%extend b2Body {
public:
    long __hash__() { return (long)self; }
    %pythoncode %{
        __eq__ = b2BodyCompare
        __ne__ = lambda self,other: not b2BodyCompare(self,other)
        def __GetMassData(self):
            """
            Get a b2MassData object that represents this b2Body

            NOTE: To just get the mass, use body.mass
            """
            ret = b2MassData()
            ret.center=self.localCenter
            ret.I    = self.inertia
            ret.mass = self.mass
            return ret
        
        def __iter__(self):
            """
            Iterates over the fixtures in the body
            """
            for fixture in self.fixtures:
                yield fixture

        def CreateFixture(self, *args, **kwargs):
            """
            Create fixture(s) on the body.

            Takes kwargs; examples of valid combinations are as follows:
            CreateFixture(b2FixtureDef())
            CreateFixture( [b2FixtureDef(), b2FixtureDef(), ...])
            CreateFixture( [b2Shape(), b2Shape(), ...], density=1.0, friction=0.2, ...)
            CreateFixture(shape=b2Shape(), friction=0.2, ...)
            CreateFixture(shape=[b2Shape(), b2Shape()], friction=0.2, ...)
            
            The above lists can be any valid combination of b2FixtureDefs and b2Shapes.
            In the case of a fixture definition with kwargs passed in, the kwargs will be
            ignored and the fixture definition will be created as it was defined. Any shapes
            in that list will be created with the specified kwarg values.

            CreateFixture(dict(...)) is a special case that allows the creation of a body
            with fixtures set: 
            self.body = self.world.CreateBody(
                        position=(0, 2), 
                        fixtures=dict(shape=b2PolygonShape(box=(0.5, 0.5)), density=1, friction=0.3)
                    )
            It is the same as passing those arguments as kwargs in the first place.
            """
            if len(args) > 1:
                raise TypeError('Takes only one argument or kwargs. See help(b2Body.CreateFixture)')
            elif len(args)==1:
                if isinstance(args[0], b2FixtureDef):
                    defn = args[0]
                    return self.__CreateFixture(defn)
                elif isinstance(args[0], dict):
                    return self.CreateFixture(**args[0])
                elif isinstance(args[0], (list, tuple)):
                    return [self.CreateFixture(defn, **kwargs) for defn in args[0]]
                elif isinstance(args[0], b2Shape):
                    if not kwargs:
                        # create a fixture from a b2Shape, assuming density of 0
                        return self.__CreateFixture(args[0], 0)
                    else:
                        # create a fixture from a b2Shape, using all of the information
                        # in the kwargs as fixture specifications
                        fixture_args = kwargs.copy()
                        fixture_args['shape']=args[0]
                        return self.__CreateFixture(b2FixtureDef(**fixture_args))
                else:
                    raise ValueError('Expected shape, b2FixtureDef, or sequence; got %s' % args[0])
            else: # no arguments, just kwargs
                if not kwargs or 'shape' not in kwargs:
                    raise TypeError('Expected shape kwarg holding the shape to create')
                if isinstance(kwargs['shape'], (list, tuple)):
                    shapes = kwargs['shape']
                    del kwargs['shape']
                    return [self.CreateFixture(shape, **kwargs) for shape in shapes]
                else:
                    return self.__CreateFixture(b2FixtureDef(**kwargs))

        def CreateEdgeChain(self, edge_list):
            """
            Creates a body a set of connected edge chains.
            Expects edge_list to be a list of vertices, length >= 2.
            """
            prev=None
            if len(edge_list) < 2:
                raise ValueError('Edge list length >= 2')

            shape=b2PolygonShape(edge=[list(i) for i in edge_list[0:2]])
            self.CreateFixture(shape)

            prev = edge_list[1]
            for edge in edge_list[1:]:
                if len(edge) != 2:
                    raise ValueError('Vertex length != 2, "%s"' % list(edge))
                shape.edge = [list(prev), list(edge)]
                self.CreateFixture(shape)
                prev=edge

        # Read-write properties
        sleepingAllowed = property(__IsSleepingAllowed, __SetSleepingAllowed)
        angularVelocity = property(__GetAngularVelocity, __SetAngularVelocity)
        linearVelocity = property(__GetLinearVelocity, __SetLinearVelocity)
        awake = property(__IsAwake, __SetAwake)
        angularDamping = property(__GetAngularDamping, __SetAngularDamping)
        fixedRotation = property(__IsFixedRotation, __SetFixedRotation)
        linearDamping = property(__GetLinearDamping, __SetLinearDamping)
        bullet = property(__IsBullet, __SetBullet)
        type = property(__GetType, __SetType)
        active = property(__IsActive, __SetActive)
        angle = property(__GetAngle, lambda self, angle: self.__SetTransform(self.position, angle))
        transform = property(__GetTransform, lambda self, value: self.__SetTransform(*value))
        massData = property(__GetMassData, __SetMassData)

        # Read-only
        joints = property(lambda self: _list_from_linked_list(self.__GetJointList_internal()), None)
        contacts = property(lambda self: _list_from_linked_list(self.__GetContactList_internal()), None)
        fixtures = property(lambda self: _list_from_linked_list(self.__GetFixtureList_internal()), None)
        next = property(__GetNext, None)
        position = property(__GetPosition, lambda self, pos: self.__SetTransform(pos, self.angle))
        mass = property(__GetMass, None)
        worldCenter = property(__GetWorldCenter, None)
        world = property(__GetWorld, None)
        localCenter = property(__GetLocalCenter, None)
        inertia = property(__GetInertia, None)
       
    %}
}

%rename(__GetAngle) b2Body::GetAngle;
%rename(__IsSleepingAllowed) b2Body::IsSleepingAllowed;
%rename(__GetAngularVelocity) b2Body::GetAngularVelocity;
%rename(__GetJointList_internal) b2Body::GetJointList;
%rename(__GetFixtureList_internal) b2Body::GetFixtureList;
%rename(__GetContactList_internal) b2Body::GetContactList;
%rename(__GetLinearVelocity) b2Body::GetLinearVelocity;
%rename(__GetNext) b2Body::GetNext;
%rename(__GetPosition) b2Body::GetPosition;
%rename(__GetMass) b2Body::GetMass;
%rename(__IsAwake) b2Body::IsAwake;
%rename(__GetTransform) b2Body::GetTransform;
%rename(__SetTransform) b2Body::SetTransform;
%rename(__GetWorldCenter) b2Body::GetWorldCenter;
%rename(__GetAngularDamping) b2Body::GetAngularDamping;
%rename(__IsFixedRotation) b2Body::IsFixedRotation;
%rename(__GetWorld) b2Body::GetWorld;
%rename(__GetLinearDamping) b2Body::GetLinearDamping;
%rename(__IsBullet) b2Body::IsBullet;
%rename(__GetLocalCenter) b2Body::GetLocalCenter;
%rename(__GetType) b2Body::GetType;
%rename(__GetInertia) b2Body::GetInertia;
%rename(__IsActive) b2Body::IsActive;
%rename(__SetLinearVelocity) b2Body::SetLinearVelocity;
%rename(__SetSleepingAllowed) b2Body::SetSleepingAllowed;
%rename(__SetAngularDamping) b2Body::SetAngularDamping;
%rename(__SetActive) b2Body::SetActive;
%rename(__SetAngularVelocity) b2Body::SetAngularVelocity;
%rename(__SetMassData) b2Body::SetMassData;
%rename(__SetBullet) b2Body::SetBullet;
%rename(__SetFixedRotation) b2Body::SetFixedRotation;
%rename(__SetAwake) b2Body::SetAwake;
%rename(__SetLinearDamping) b2Body::SetLinearDamping;
%rename(__SetType) b2Body::SetType;

//
