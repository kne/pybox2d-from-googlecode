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

    # Read-only
    next = property(__GetNext, None)
    bodyA = property(__GetBodyA, None)
    bodyB = property(__GetBodyB, None)
    type = property(__GetType, None)
    active = property(__IsActive, None)
    anchorB = property(__GetAnchorB, None)
    anchorA = property(__GetAnchorA, None)

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
        speed = property(__GetJointSpeed, None)
        translation = property(__GetJointTranslation, None)

    %}
}

%rename(__SetLimits) b2LineJoint::SetLimits;
%rename(__IsMotorEnabled) b2LineJoint::IsMotorEnabled;
%rename(__GetMotorSpeed) b2LineJoint::GetMotorSpeed;
%rename(__GetMotorForce) b2LineJoint::GetMotorForce;
%rename(__GetMaxMotorForce) b2LineJoint::GetMaxMotorForce;
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

%ignore e_atLowerLimit;
%ignore e_atUpperLimit;
%ignore e_distanceJoint;
%ignore e_equalLimits;
%ignore e_frictionJoint;
%ignore e_gearJoint;
%ignore e_inactiveLimit;
%ignore e_lineJoint;
%ignore e_mouseJoint;
%ignore e_prismaticJoint;
%ignore e_pulleyJoint;
%ignore e_revoluteJoint;
%ignore e_unknownJoint;
%ignore e_weldJoint;
