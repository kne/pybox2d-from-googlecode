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

%feature("shadow") b2World::b2World(const b2Vec2& gravity, bool doSleep) {
    def __init__(self, *args, **kwargs): 
        """__init__(self, *args, **kwargs) -> b2World
        Non-named arguments:
         b2World(gravity, doSleep)

        Examples:
         b2World( (0,-10), True)
         b2World( gravity=(0,-10), doSleep=True)

        Required arguments:
        * gravity
        * doSleep
        """
        required = ('gravity', 'doSleep')
        if args:
            for key, value in zip(required, args):
                if key not in kwargs:
                    kwargs[key]=value
        if kwargs:
            missing=[v for v in required if v not in kwargs]
            if missing:
                raise ValueError('Arguments missing: %s' % ','.join(missing) )
        else:
            raise ValueError('Arguments required: %s' % ','.join(required) )

        args=( kwargs['gravity'], kwargs['doSleep'] )
        _Box2D.b2World_swiginit(self,_Box2D.new_b2World(*args))

        for key, value in kwargs.items():
            setattr(self, key, value)

}

%extend b2World {
public:        
    %pythoncode %{
        def __iter__(self):
            """
            Iterates over the bodies in the world
            """
            for body in self.bodies:
                yield body

        def CreateBody(self, defn):
            body=self.__CreateBody(defn)
            if defn.fixtures:
                for fixture in defn.fixtures:
                    if isinstance(fixture, (list, tuple)):
                        # create a fixture from a shape, in format (shape, density)
                        body.CreateFixture(*fixture)
                    elif isinstance(fixture, b2FixtureDef):
                        # create a fixture from a b2FixtureDef
                        body.CreateFixture(fixture)
                    elif isinstance(fixture, b2Shape):
                        # create a fixture from a b2Shape, assuming density of 0.0
                        body.CreateFixture(fixture, 0.0)
                    else:
                        raise ValueError('Unexpected element in fixture list: %s (type %s)' % (fixture, type(fixture)))
            return body

        def CreateJoint(self, defn):
            if isinstance(defn, b2GearJointDef):
                if not defn.joint1 or not defn.joint2:
                    raise ValueError('Joint(s) not set')
            else:
                if not defn.bodyA or not defn.bodyB:
                    raise ValueError('Body or bodies not set')
            joint=self.__CreateJoint(defn)
            return joint

        # The logic behind these functions is that they increase the refcount
        # of the listeners as you set them, so it is no longer necessary to keep
        # a copy on your own. Upon destruction of the object, it should be cleared
        # also clearing the refcount of the function.
        # Now using it also to buffer previously write-only values in the shadowed
        # class to make them read-write.
        # TODO: test this
        def __GetData(self, name):
            if name in self.__data.keys():
                return self.__data[name]
            else:
                return None
        def __SetData(self, name, value, fcn):
            self.__data[name] = value
            fcn(value)

        # Read-write properties
        gravity   = property(__GetGravity, __SetGravity)
        __data = {} # holds the listeners so they can be properly destroyed, and buffer other data
        destructionListener = property(lambda self: self.__GetData('destruction'), 
                                            lambda self, fcn: self.__SetData('destruction', fcn, self.__SetDestructionListener_internal))
        contactListener     = property(lambda self: self.__GetData('contact'), 
                                            lambda self, fcn: self.__SetData('contact', fcn, self.__SetContactListener_internal))
        contactFilter       = property(lambda self: self.__GetData('contactfilter'),
                                            lambda self, fcn: self.__SetData('contactfilter', fcn, self.__SetContactFilter_internal))
        debugDraw           = property(lambda self: self.__GetData('debugdraw'),
                                            lambda self, fcn: self.__SetData('debugdraw', fcn, self.__SetDebugDraw_internal))
        continuousPhysics = property(lambda self: self.__GetData('continuousphysics'), 
                                lambda self, fcn: self.__SetData('continuousphysics', fcn, self.__SetContinuousPhysics_internal))
        warmStarting = property(lambda self: self.__GetData('warmstarting'), 
                                lambda self, fcn: self.__SetData('warmstarting', fcn, self.__SetWarmStarting_internal))

        # Read-only 
        contactCount  = property(__GetContactCount, None)
        bodyCount     = property(__GetBodyCount, None)
        proxyCount    = property(__GetProxyCount, None)
        joints    = property(lambda self: _list_from_linked_list(self.__GetJointList_internal()), None)
        bodies    = property(lambda self: _list_from_linked_list(self.__GetBodyList_internal()), None)
        contacts  = property(lambda self: _list_from_linked_list(self.__GetContactList_internal()), None)
        locked    = property(__IsLocked, None)

        # other functions:
        # DestroyBody, DestroyJoint
        # Step, ClearForces, DrawDebugData, QueryAABB, RayCast
    %}
}

%rename (__GetGravity) b2World::GetGravity;
%rename (__SetGravity) b2World::SetGravity;
%rename (__GetJointList_internal) b2World::GetJointList;
%rename (__GetBodyList_internal) b2World::GetBodyList;
%rename (__GetContactList_internal) b2World::GetContactList;
%rename (__SetDestructionListener_internal) b2World::SetDestructionListener;
%rename (__SetContactFilter_internal) b2World::SetContactFilter;
%rename (__SetContactListener_internal) b2World::SetContactListener;
%rename (__SetDebugDraw_internal) b2World::SetDebugDraw;
%rename (__GetContactCount) b2World::GetContactCount;
%rename (__GetProxyCount) b2World::GetProxyCount;
%rename (__GetBodyCount) b2World::GetBodyCount;
%rename (__IsLocked) b2World::IsLocked;
%rename (__SetContinuousPhysics_internal) b2World::SetContinuousPhysics;
%rename (__SetWarmStarting_internal) b2World::SetWarmStarting;

