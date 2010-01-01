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

/**** Joint ****/
%extend b2Joint {
public:
    long __hash__() { return (long)self; }
    %pythoncode %{
    __eq__ = b2JointCompare
    __ne__ = lambda self,other: not b2JointCompare(self,other)
    def __setattr__(self, var, value):
        if var in dir(self):
            super(b2Joint, self).__setattr__(var, value)
        else: 
            raise TypeError("Shadow class has no property '%s'. %s Typo?" % (var, type(self)))
    __delattr__ = __setattr__

    # Read-only
    next = property(__GetNext, None)
    bodyA = property(__GetBodyA, None)
    bodyB = property(__GetBodyB, None)
    type = property(__GetType, None)
    active = property(__IsActive, None)

    %}

}

%rename(__GetNext) b2Joint::GetNext;
%rename(__GetBodyA) b2Joint::GetBodyA;
%rename(__GetBodyB) b2Joint::GetBodyB;
%rename(__GetType) b2Joint::GetType;
%rename(__IsActive) b2Joint::IsActive;
%rename(__GetAnchorA) b2Joint::GetAnchorA;
%rename(__GetAnchorB) b2Joint::GetAnchorB;

/**** RevoluteJoint ****/
%extend b2RevoluteJoint {
public:
    %pythoncode %{

        # Read-write properties
        motorSpeed = property(__GetMotorSpeed, __SetMotorSpeed)
        upperLimit = property(__GetUpperLimit, lambda self, v: self.SetLimits(self.lowerLimit, v))
        lowerLimit = property(__GetLowerLimit, lambda self, v: self.SetLimits(v, self.upperLimit))
        limits = property(lambda self: (self.lowerLimit, self.upperLimit), lambda self, v: self.SetLimits(*v) )
        motorEnabled = property(__IsMotorEnabled, __EnableMotor)
        limitEnabled = property(__IsLimitEnabled, __EnableLimit)

        # Read-only
        anchorB = property(lambda self: self._b2Joint__GetAnchorB(), None)
        anchorA = property(lambda self: self._b2Joint__GetAnchorA(), None)
        angle = property(__GetJointAngle, None)
        motorTorque = property(__GetMotorTorque, None)
        speed = property(__GetJointSpeed, None)

        # Write-only
        maxMotorTorque = property(None, __SetMaxMotorTorque)

    %}
}

%rename(__IsMotorEnabled) b2RevoluteJoint::IsMotorEnabled;
%rename(__GetUpperLimit) b2RevoluteJoint::GetUpperLimit;
%rename(__GetLowerLimit) b2RevoluteJoint::GetLowerLimit;
%rename(__GetJointAngle) b2RevoluteJoint::GetJointAngle;
%rename(__GetMotorSpeed) b2RevoluteJoint::GetMotorSpeed;
%rename(__GetMotorTorque) b2RevoluteJoint::GetMotorTorque;
%rename(__GetJointSpeed) b2RevoluteJoint::GetJointSpeed;
%rename(__IsLimitEnabled) b2RevoluteJoint::IsLimitEnabled;
%rename(__SetMotorSpeed) b2RevoluteJoint::SetMotorSpeed;
%rename(__EnableLimit) b2RevoluteJoint::EnableLimit;
%rename(__SetMaxMotorTorque) b2RevoluteJoint::SetMaxMotorTorque;
%rename(__EnableMotor) b2RevoluteJoint::EnableMotor;

/**** LineJoint ****/
%extend b2LineJoint {
public:
    %pythoncode %{

        # Read-write properties
        motorSpeed = property(__GetMotorSpeed, __SetMotorSpeed)
        maxMotorForce = property(__GetMaxMotorForce, __SetMaxMotorForce)
        motorEnabled = property(__IsMotorEnabled, __EnableMotor)
        limitEnabled = property(__IsLimitEnabled, __EnableLimit)
        upperLimit = property(__GetUpperLimit, lambda self, v: self.__SetLimits(self.lowerLimit, v))
        lowerLimit = property(__GetLowerLimit, lambda self, v: self.__SetLimits(v, self.upperLimit))
        limits = property(lambda self: (self.lowerLimit, self.upperLimit), lambda self, v: self.__SetLimits(*v) )

        # Read-only
        motorForce = property(__GetMotorForce, None)
        anchorA = property(lambda self: self._b2Joint__GetAnchorA(), None)
        anchorB = property(lambda self: self._b2Joint__GetAnchorB(), None)
        speed = property(__GetJointSpeed, None)
        translation = property(__GetJointTranslation, None)

    %}
}

%rename(__SetLimits) b2LineJoint::SetLimits;
%rename(__IsMotorEnabled) b2LineJoint::IsMotorEnabled;
%rename(__GetMotorSpeed) b2LineJoint::GetMotorSpeed;
%rename(__GetMotorForce) b2LineJoint::GetMotorForce;
%rename(__GetMaxMotorForce) b2LineJoint::GetMaxMotorForce;
%rename(__GetAnchorB) b2LineJoint::GetAnchorB;
%rename(__GetAnchorA) b2LineJoint::GetAnchorA;
%rename(__GetUpperLimit) b2LineJoint::GetUpperLimit;
%rename(__GetJointSpeed) b2LineJoint::GetJointSpeed;
%rename(__GetJointTranslation) b2LineJoint::GetJointTranslation;
%rename(__IsLimitEnabled) b2LineJoint::IsLimitEnabled;
%rename(__GetLowerLimit) b2LineJoint::GetLowerLimit;
%rename(__SetMotorSpeed) b2LineJoint::SetMotorSpeed;
%rename(__EnableLimit) b2LineJoint::EnableLimit;
%rename(__SetMaxMotorForce) b2LineJoint::SetMaxMotorForce;
%rename(__EnableMotor) b2LineJoint::EnableMotor;

/**** PrismaticJoint ****/
%extend b2PrismaticJoint {
public:
    %pythoncode %{

        # Read-write properties
        motorSpeed = property(__GetMotorSpeed, __SetMotorSpeed)
        motorEnabled = property(__IsMotorEnabled, __EnableMotor)
        limitEnabled = property(__IsLimitEnabled, __EnableLimit)
        upperLimit = property(__GetUpperLimit, lambda self, v: self.SetLimits(self.lowerLimit, v))
        lowerLimit = property(__GetLowerLimit, lambda self, v: self.SetLimits(v, self.upperLimit))
        limits = property(lambda self: (self.lowerLimit, self.upperLimit), lambda self, v: self.SetLimits(*v) )
        maxMotorForce = property(__GetMaxMotorForce, __SetMaxMotorForce)

        # Read-only
        motorForce = property(__GetMotorForce, None)
        translation = property(__GetJointTranslation, None)
        anchorA = property(lambda self: self._b2Joint__GetAnchorA(), None)
        anchorB = property(lambda self: self._b2Joint__GetAnchorB(), None)
        speed = property(__GetJointSpeed, None)

    %}
}

%rename(__IsMotorEnabled) b2PrismaticJoint::IsMotorEnabled;
%rename(__GetMotorSpeed) b2PrismaticJoint::GetMotorSpeed;
%rename(__GetMotorForce) b2PrismaticJoint::GetMotorForce;
%rename(__GetJointTranslation) b2PrismaticJoint::GetJointTranslation;
%rename(__GetUpperLimit) b2PrismaticJoint::GetUpperLimit;
%rename(__GetJointSpeed) b2PrismaticJoint::GetJointSpeed;
%rename(__IsLimitEnabled) b2PrismaticJoint::IsLimitEnabled;
%rename(__GetLowerLimit) b2PrismaticJoint::GetLowerLimit;
%rename(__SetMotorSpeed) b2PrismaticJoint::SetMotorSpeed;
%rename(__EnableLimit) b2PrismaticJoint::EnableLimit;
%rename(__SetMaxMotorForce) b2PrismaticJoint::SetMaxMotorForce;
%rename(__GetMaxMotorForce) b2PrismaticJoint::GetMaxMotorForce;
%rename(__EnableMotor) b2PrismaticJoint::EnableMotor;

/**** DistanceJoint ****/
%extend b2DistanceJoint {
public:
    %pythoncode %{

        # Read-write properties
        length = property(__GetLength, __SetLength)
        frequency = property(__GetFrequency, __SetFrequency)
        dampingRatio = property(__GetDampingRatio, __SetDampingRatio)

        # Read-only
        anchorA = property(lambda self: self._b2Joint__AnchorA(), None)
        anchorB = property(lambda self: self._b2Joint__AnchorB(), None)

    %}
}

%rename(__GetLength) b2DistanceJoint::GetLength;
%rename(__GetFrequency) b2DistanceJoint::GetFrequency;
%rename(__GetDampingRatio) b2DistanceJoint::GetDampingRatio;
%rename(__SetDampingRatio) b2DistanceJoint::SetDampingRatio;
%rename(__SetLength) b2DistanceJoint::SetLength;
%rename(__SetFrequency) b2DistanceJoint::SetFrequency;

/**** PulleyJoint ****/
%extend b2PulleyJoint {
public:
    %pythoncode %{

        # Read-only
        groundAnchorB = property(__GetGroundAnchorB, None)
        groundAnchorA = property(__GetGroundAnchorA, None)
        anchorB = property(lambda self: self._b2Joint__AnchorB(), None)
        anchorA = property(lambda self: self._b2Joint__AnchorA(), None)
        length2 = property(__GetLength2, None)
        length1 = property(__GetLength1, None)
        ratio = property(__GetRatio, None)

    %}
}

%rename(__GetGroundAnchorB) b2PulleyJoint::GetGroundAnchorB;
%rename(__GetGroundAnchorA) b2PulleyJoint::GetGroundAnchorA;
%rename(__GetLength2) b2PulleyJoint::GetLength2;
%rename(__GetLength1) b2PulleyJoint::GetLength1;
%rename(__GetRatio) b2PulleyJoint::GetRatio;

/**** MouseJoint ****/
%extend b2MouseJoint {
public:
    %pythoncode %{

        # Read-write properties
        maxForce = property(__GetMaxForce, __SetMaxForce)
        frequency = property(__GetFrequency, __SetFrequency)
        dampingRatio = property(__GetDampingRatio, __SetDampingRatio)
        target = property(__GetTarget, __SetTarget)

    %}
}

%rename(__GetMaxForce) b2MouseJoint::GetMaxForce;
%rename(__GetFrequency) b2MouseJoint::GetFrequency;
%rename(__GetDampingRatio) b2MouseJoint::GetDampingRatio;
%rename(__GetTarget) b2MouseJoint::GetTarget;
%rename(__SetDampingRatio) b2MouseJoint::SetDampingRatio;
%rename(__SetTarget) b2MouseJoint::SetTarget;
%rename(__SetMaxForce) b2MouseJoint::SetMaxForce;
%rename(__SetFrequency) b2MouseJoint::SetFrequency;

/**** GearJoint ****/
%extend b2GearJoint {
public:
    %pythoncode %{
        # Read-write properties
        ratio = property(__GetRatio, __SetRatio)

    %}
}

%rename(__GetRatio) b2GearJoint::GetRatio;
%rename(__SetRatio) b2GearJoint::SetRatio;

/**** WeldJoint ****/
%extend b2WeldJoint {
}

/**** FrictionJoint ****/
%extend b2FrictionJoint {
public:
    %pythoncode %{
        # Read-write properties
        maxForce = property(__GetMaxForce, __SetMaxForce)
        maxTorque = property(__GetMaxTorque, __SetMaxTorque)
    %}
}

%rename(__GetMaxForce) b2FrictionJoint::GetMaxForce;
%rename(__GetMaxTorque) b2FrictionJoint::GetMaxTorque;
%rename(__SetMaxTorque) b2FrictionJoint::SetMaxTorque;
%rename(__SetMaxForce) b2FrictionJoint::SetMaxForce;

/**** Extend all of the joint definitions to allow kwargs ****/
%extend b2JointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2JointDef """
            _Box2D.b2JointDef_swiginit(self,_Box2D.new_b2JointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2RevoluteJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2RevoluteJointDef """
            _Box2D.b2RevoluteJointDef_swiginit(self,_Box2D.new_b2RevoluteJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2PrismaticJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2PrismaticJointDef """
            _Box2D.b2PrismaticJointDef_swiginit(self,_Box2D.new_b2PrismaticJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2DistanceJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2DistanceJointDef """
            _Box2D.b2DistanceJointDef_swiginit(self,_Box2D.new_b2DistanceJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2PulleyJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2PulleyJointDef """
            _Box2D.b2PulleyJointDef_swiginit(self,_Box2D.new_b2PulleyJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2MouseJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2MouseJointDef """
            _Box2D.b2MouseJointDef_swiginit(self,_Box2D.new_b2MouseJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2GearJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2GearJointDef """
            _Box2D.b2GearJointDef_swiginit(self,_Box2D.new_b2GearJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2LineJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2LineJointDef """
            _Box2D.b2LineJointDef_swiginit(self,_Box2D.new_b2LineJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2WeldJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2WeldJointDef """
            _Box2D.b2WeldJointDef_swiginit(self,_Box2D.new_b2WeldJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}


%extend b2FrictionJointDef {
public:
    %pythoncode %{

        def __init__(self, **kwargs): 
            """__init__(self, **kwargs) -> b2FrictionJointDef """
            _Box2D.b2FrictionJointDef_swiginit(self,_Box2D.new_b2FrictionJointDef())
            for key, value in kwargs.items():
                setattr(self, key, value)
    %}
}

/* -- End joint definitions -- */

%include "Dynamics/Joints/b2Joint.h"

%pythoncode %{
    b2JointTypes = {
        e_unknownJoint : "Unknown",
        e_revoluteJoint : "Revolute",
        e_prismaticJoint : "Prismatic",
        e_distanceJoint : "Distance",
        e_pulleyJoint : "Pulley",
        e_mouseJoint : "Mouse",
        e_gearJoint : "Gear",
        e_lineJoint : "Line",
        e_weldJoint : "Weld",
        e_frictionJoint : "Friction",
    }

%}
