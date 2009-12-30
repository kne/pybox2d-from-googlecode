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


%extend b2World {
public:        
    %pythoncode %{
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
        # also clearing the refcount of the function. TODO: test this
        def __SetDestructionListener(self, fcn):
            self.__listeners['destruction']=fcn
            self.__SetDestructionListener_internal(fcn)

        def __SetContactListener(self, fcn):
            self.__listeners['contact']=fcn
            self.__SetContactListener_internal(fcn)

        def __SetContactFilter(self, fcn):
            self.__listeners['contactfilter']=fcn
            self.__SetContactFilter_internal(fcn)

        def __SetDebugDraw(self, fcn):
            self.__listeners['debugdraw']=fcn
            self.__SetDebugDraw_internal(fcn)
        
        # Read-write properties
        gravity   = property(__GetGravity   , __SetGravity)
        __listeners = {} # holds the listeners so they can be properly destroyed

        # Read-only 
        contactCount  = property(__GetContactCount, None)
        bodyCount     = property(__GetBodyCount, None)
        proxyCount    = property(__GetProxyCount, None)
        joints    = property(lambda self: [joint.downcast() for joint in _list_from_linked_list(self.__GetJointList_internal())], None)
        bodies    = property(lambda self: _list_from_linked_list(self.__GetBodyList_internal()), None)
        contacts  = property(lambda self: _list_from_linked_list(self.__GetContactList_internal()), None)

        # Write-only
        destructionListener = property(None, __SetDestructionListener)
        contactListener     = property(None, __SetContactListener)
        contactFilter       = property(None, __SetContactFilter)
        debugDraw           = property(None, __SetDebugDraw)

        # other functions:
        # DestroyBody, DestroyJoint
        # Step, ClearForces, DrawDebugData, QueryAABB, RayCast,
        # IsLocked
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

