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

%pythoncode %{
    def _init_kwargs(self, **kwargs):
        for key, value in list(kwargs.items()):
            try:
                setattr(self, key, value)
            except Exception as ex:
                raise ex.__class__('Failed on kwargs, class="%s" key="%s": %s' 
                            % (self.__class__.__name__, key, ex))
%}


%feature("shadow") b2ContactFilter::b2ContactFilter() {
    def __init__(self, **kwargs):
        if self.__class__ == b2ContactFilter:
            _self = None
        else:
            _self = self
        _Box2D.b2ContactFilter_swiginit(self,_Box2D.new_b2ContactFilter(_self, ))
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ContactListener::b2ContactListener() {
    def __init__(self, **kwargs):
        if self.__class__ == b2ContactListener:
            _self = None
        else:
            _self = self
        _Box2D.b2ContactListener_swiginit(self,_Box2D.new_b2ContactListener(_self, ))
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2QueryCallback::b2QueryCallback() {
    def __init__(self, **kwargs):
        if self.__class__ == b2QueryCallback:
            _self = None
        else:
            _self = self
        _Box2D.b2QueryCallback_swiginit(self,_Box2D.new_b2QueryCallback(_self, ))
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2DebugDraw::b2DebugDraw() {
    def __init__(self, **kwargs):
        if self.__class__ == b2DebugDraw:
            _self = None
        else:
            _self = self
        _Box2D.b2DebugDraw_swiginit(self,_Box2D.new_b2DebugDraw(_self, ))
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2DestructionListener::b2DestructionListener() {
    def __init__(self, **kwargs):
        if self.__class__ == b2DestructionListener:
            _self = None
        else:
            _self = self
        _Box2D.b2DestructionListener_swiginit(self,_Box2D.new_b2DestructionListener(_self, ))
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2AABB::b2AABB() {
    def __init__(self, **kwargs):
        _Box2D.b2AABB_swiginit(self,_Box2D.new_b2AABB())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Body::b2Body() {
    def __init__(self, **kwargs):
        _Box2D.b2Body_swiginit(self,_Box2D.new_b2Body())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2BodyDef::b2BodyDef() {
    def __init__(self, **kwargs):
        _Box2D.b2BodyDef_swiginit(self,_Box2D.new_b2BodyDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2CircleShape::b2CircleShape() {
    def __init__(self, **kwargs):
        _Box2D.b2CircleShape_swiginit(self,_Box2D.new_b2CircleShape())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ClipVertex::b2ClipVertex() {
    def __init__(self, **kwargs):
        _Box2D.b2ClipVertex_swiginit(self,_Box2D.new_b2ClipVertex())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Color::b2Color() {
    def __init__(self, **kwargs):
        _Box2D.b2Color_swiginit(self,_Box2D.new_b2Color())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ContactPoint::b2ContactPoint() {
    def __init__(self, **kwargs):
        _Box2D.b2ContactPoint_swiginit(self,_Box2D.new_b2ContactPoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ContactEdge::b2ContactEdge() {
    def __init__(self, **kwargs):
        _Box2D.b2ContactEdge_swiginit(self,_Box2D.new_b2ContactEdge())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ContactID::b2ContactID() {
    def __init__(self, **kwargs):
        _Box2D.b2ContactID_swiginit(self,_Box2D.new_b2ContactID())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ContactImpulse::b2ContactImpulse() {
    def __init__(self, **kwargs):
        _Box2D.b2ContactImpulse_swiginit(self,_Box2D.new_b2ContactImpulse())
        _init_kwargs(self, **kwargs)
}



%feature("shadow") b2DistanceInput::b2DistanceInput() {
    def __init__(self, **kwargs):
        _Box2D.b2DistanceInput_swiginit(self,_Box2D.new_b2DistanceInput())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2DistanceJoint::b2DistanceJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2DistanceJoint_swiginit(self,_Box2D.new_b2DistanceJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2DistanceJointDef::b2DistanceJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2DistanceJointDef_swiginit(self,_Box2D.new_b2DistanceJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2DistanceOutput::b2DistanceOutput() {
    def __init__(self, **kwargs):
        _Box2D.b2DistanceOutput_swiginit(self,_Box2D.new_b2DistanceOutput())
        _init_kwargs(self, **kwargs)
}



%feature("shadow") b2Filter::b2Filter() {
    def __init__(self, **kwargs):
        _Box2D.b2Filter_swiginit(self,_Box2D.new_b2Filter())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Fixture::b2Fixture() {
    def __init__(self, **kwargs):
        _Box2D.b2Fixture_swiginit(self,_Box2D.new_b2Fixture())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2FixtureDef::b2FixtureDef() {
    def __init__(self, **kwargs):
        _Box2D.b2FixtureDef_swiginit(self,_Box2D.new_b2FixtureDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2FrictionJoint::b2FrictionJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2FrictionJoint_swiginit(self,_Box2D.new_b2FrictionJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2FrictionJointDef::b2FrictionJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2FrictionJointDef_swiginit(self,_Box2D.new_b2FrictionJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2GearJoint::b2GearJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2GearJoint_swiginit(self,_Box2D.new_b2GearJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2GearJointDef::b2GearJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2GearJointDef_swiginit(self,_Box2D.new_b2GearJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Jacobian::b2Jacobian() {
    def __init__(self, **kwargs):
        _Box2D.b2Jacobian_swiginit(self,_Box2D.new_b2Jacobian())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2JointDef::b2JointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2JointDef_swiginit(self,_Box2D.new_b2JointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2JointEdge::b2JointEdge() {
    def __init__(self, **kwargs):
        _Box2D.b2JointEdge_swiginit(self,_Box2D.new_b2JointEdge())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2LineJoint::b2LineJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2LineJoint_swiginit(self,_Box2D.new_b2LineJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2LineJointDef::b2LineJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2LineJointDef_swiginit(self,_Box2D.new_b2LineJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Manifold::b2Manifold() {
    def __init__(self, **kwargs):
        _Box2D.b2Manifold_swiginit(self,_Box2D.new_b2Manifold())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2ManifoldPoint::b2ManifoldPoint() {
    def __init__(self, **kwargs):
        _Box2D.b2ManifoldPoint_swiginit(self,_Box2D.new_b2ManifoldPoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2MassData::b2MassData() {
    def __init__(self, **kwargs):
        _Box2D.b2MassData_swiginit(self,_Box2D.new_b2MassData())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Mat22::b2Mat22() {
    def __init__(self, **kwargs):
        _Box2D.b2Mat22_swiginit(self,_Box2D.new_b2Mat22())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Mat33::b2Mat33() {
    def __init__(self, **kwargs):
        _Box2D.b2Mat33_swiginit(self,_Box2D.new_b2Mat33())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2MouseJoint::b2MouseJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2MouseJoint_swiginit(self,_Box2D.new_b2MouseJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2MouseJointDef::b2MouseJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2MouseJointDef_swiginit(self,_Box2D.new_b2MouseJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Pair::b2Pair() {
    def __init__(self, **kwargs):
        _Box2D.b2Pair_swiginit(self,_Box2D.new_b2Pair())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2PolygonShape::b2PolygonShape() {
    def __init__(self, **kwargs):
        _Box2D.b2PolygonShape_swiginit(self,_Box2D.new_b2PolygonShape())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2PrismaticJoint::b2PrismaticJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2PrismaticJoint_swiginit(self,_Box2D.new_b2PrismaticJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2PrismaticJointDef::b2PrismaticJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2PrismaticJointDef_swiginit(self,_Box2D.new_b2PrismaticJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2PulleyJoint::b2PulleyJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2PulleyJoint_swiginit(self,_Box2D.new_b2PulleyJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2PulleyJointDef::b2PulleyJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2PulleyJointDef_swiginit(self,_Box2D.new_b2PulleyJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2RayCastInput::b2RayCastInput() {
    def __init__(self, **kwargs):
        _Box2D.b2RayCastInput_swiginit(self,_Box2D.new_b2RayCastInput())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2RayCastOutput::b2RayCastOutput() {
    def __init__(self, **kwargs):
        _Box2D.b2RayCastOutput_swiginit(self,_Box2D.new_b2RayCastOutput())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2RevoluteJoint::b2RevoluteJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2RevoluteJoint_swiginit(self,_Box2D.new_b2RevoluteJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2RevoluteJointDef::b2RevoluteJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2RevoluteJointDef_swiginit(self,_Box2D.new_b2RevoluteJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Segment::b2Segment() {
    def __init__(self, **kwargs):
        _Box2D.b2Segment_swiginit(self,_Box2D.new_b2Segment())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Sweep::b2Sweep() {
    def __init__(self, **kwargs):
        _Box2D.b2Sweep_swiginit(self,_Box2D.new_b2Sweep())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2TOIInput::b2TOIInput() {
    def __init__(self, **kwargs):
        _Box2D.b2TOIInput_swiginit(self,_Box2D.new_b2TOIInput())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Transform::b2Transform() {
    def __init__(self, **kwargs):
        _Box2D.b2Transform_swiginit(self,_Box2D.new_b2Transform())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Vec2::b2Vec2() {
    def __init__(self, **kwargs):
        _Box2D.b2Vec2_swiginit(self,_Box2D.new_b2Vec2())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Vec3::b2Vec3() {
    def __init__(self, **kwargs):
        _Box2D.b2Vec3_swiginit(self,_Box2D.new_b2Vec3())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2Version::b2Version() {
    def __init__(self, **kwargs):
        _Box2D.b2Version_swiginit(self,_Box2D.new_b2Version())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2WeldJoint::b2WeldJoint() {
    def __init__(self, **kwargs):
        _Box2D.b2WeldJoint_swiginit(self,_Box2D.new_b2WeldJoint())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2WeldJointDef::b2WeldJointDef() {
    def __init__(self, **kwargs):
        _Box2D.b2WeldJointDef_swiginit(self,_Box2D.new_b2WeldJointDef())
        _init_kwargs(self, **kwargs)
}


%feature("shadow") b2WorldManifold::b2WorldManifold() {
    def __init__(self, **kwargs):
        _Box2D.b2WorldManifold_swiginit(self,_Box2D.new_b2WorldManifold())
        _init_kwargs(self, **kwargs)
}
