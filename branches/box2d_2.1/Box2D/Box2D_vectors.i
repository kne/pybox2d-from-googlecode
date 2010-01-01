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

//These operators do not work unless explicitly defined like this 
%rename(b2add) operator  + (const b2Vec2& a, const b2Vec2& b);
%rename(b2add) operator  + (const b2Mat22& A, const b2Mat22& B);
%rename(b2sub) operator  - (const b2Vec2& a, const b2Vec2& b);
%rename(b2mul) operator  * (float32 s, const b2Vec2& a);
%rename(b2equ) operator == (const b2Vec2& a, const b2Vec2& b);

%rename(b2mul) operator * (float32 s, const b2Vec3& a);
%rename(b2add) operator + (const b2Vec3& a, const b2Vec3& b);
%rename(b2sub) operator - (const b2Vec3& a, const b2Vec3& b);

//Since Python (apparently) requires __imul__ to return self,
//these void operators will not do. So, rename them, then call them
//with Python code, and return self. (see further down in b2Vec2)
%rename(add_vector) b2Vec2::operator += (const b2Vec2& v);
%rename(sub_vector) b2Vec2::operator -= (const b2Vec2& v);
%rename(mul_float ) b2Vec2::operator *= (float32 a);

/**** Vector classes ****/
%extend b2Vec2 {
public:
    b2Vec2(b2Vec2& other) {
        return new b2Vec2(other.x, other.y);
    }

    %pythoncode %{
    __iter__ = lambda self: iter( (self.x, self.y) )
    __eq__ = lambda self, other: b2equ(self, other)
    __ne__ = lambda self,other: not b2equ(self, other)
    def __repr__(self):
        return "b2Vec2(%g,%g)" % (self.x, self.y)
    def copy(self):
        """
        Return a copy of the vector.
        Remember that the following:
            a = b2Vec2()
            b = a
        Does not copy the vector itself, but b now refers to a.
        """
        return b2Vec2(self.x, self.y)
    def __iadd__(self, other):
        self.add_vector(other)
        return self
    def __isub__(self, other):
        self.sub_vector(other)
        return self
    def __imul__(self, a):
        self.mul_float(a)
        return self
    def __idiv__(self, a):
        self.div_float(a)
        return self
    def __set(self, x, y):
        self.x = x
        self.y = y
    def __getitem__(self, i): 
        if i==0:
            return self.x
        elif i==1:
            return self.y
        else:
            raise IndexError
    def __setitem__(self, i, value): 
        if i==0:
            self.x=value
        elif i==1:
            self.y=value
        else:
            raise IndexError

    tuple = property(lambda self: tuple(self.x, self.y), lambda self, value: self.__set(*value))
    length = property(__Length, None)
    lengthSquared = property(__LengthSquared, None)
    valid = property(__IsValid, None)

    %}
    float32 dot(b2Vec2& other) {
        return $self->x * other.x + $self->y * other.y;
    }
    b2Vec2 __div__(float32 a) {
        return b2Vec2($self->x / a, $self->y / a);
    }
    b2Vec2 __mul__(float32 a) {
        return b2Vec2($self->x * a, $self->y * a);
    }
    b2Vec2 __add__(b2Vec2* other) {
        return b2Vec2($self->x + other->x, $self->y + other->y);
    }
    b2Vec2 __sub__(b2Vec2* other) {
        return b2Vec2($self->x - other->x, $self->y - other->y);
    }

    b2Vec2 __rmul__(float32 a) {
        return b2Vec2($self->x * a, $self->y * a);
    }
    b2Vec2 __rdiv__(float32 a) {
        return b2Vec2($self->x / a, $self->y / a);
    }
    void div_float(float32 a) {
        $self->x /= a;
        $self->y /= a;
    }
}

%rename (__Length) b2Vec2::Length;
%rename (__LengthSquared) b2Vec2::LengthSquared;
%rename (__IsValid) b2Vec2::IsValid;

%extend b2Vec3 {
public:
    b2Vec3(b2Vec3& other) {
        return new b2Vec3(other.x, other.y, other.z);
    }

    b2Vec3(b2Vec2& other) {
        return new b2Vec3(other.x, other.y, 0.0f);
    }

    %pythoncode %{
    __iter__ = lambda self: iter( (self.x, self.y, self.z) )
    __eq__ = lambda self, other: (self.x == other.x and self.y == other.y and self.z == other.z)
    __ne__ = lambda self,other: (self.x != other.x or self.y != other.y or self.z != other.z)
    def __repr__(self):
        return "b2Vec3(%g,%g,%g)" % (self.x, self.y, self.z)
    def copy(self):
        """
        Return a copy of the vector.
        Remember that the following:
            a = b2Vec3()
            b = a
        Does not copy the vector itself, but b now refers to a.
        """
        return b2Vec3(self.x, self.y, self.z)
    def __iadd__(self, other):
        self.add_vector(other)
        return self
    def __isub__(self, other):
        self.sub_vector(other)
        return self
    def __imul__(self, a):
        self.mul_float(a)
        return self
    def __idiv__(self, a):
        self.div_float(a)
        return self
    def dot(self, v):
        """
        Dot product with v (list/tuple or b2Vec3)
        """
        if isinstance(v, (list, tuple)):
            return self.x*v[0] + self.y*v[1] + self.z*v[2]
        else:
            return self.x*v.x + self.y*v.y + self.z*v.z
    def __set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __getitem__(self, i): 
        if i==0:
            return self.x
        elif i==1:
            return self.y
        elif i==2:
            return self.z
        else:
            raise IndexError
    def __setitem__(self, i, value): 
        if i==0:
            self.x=value
        elif i==1:
            self.y=value
        elif i==2:
            self.z=value
        else:
            raise IndexError

    tuple = property(lambda self: tuple(self.x, self.y, self.z), lambda self, value: self.__set(*value))
    length = property(_Box2D.b2Vec3___Length, None)
    lengthSquared = property(_Box2D.b2Vec3___LengthSquared, None)
    valid = property(_Box2D.b2Vec3___IsValid, None)

    %}

    bool __IsValid() {
        return b2IsValid($self->x) && b2IsValid($self->y) && b2IsValid($self->z);
    }
    float32 __Length() {
        return b2Sqrt($self->x * $self->x + $self->y * $self->y + $self->z * $self->z);
    }
    float32 __LengthSquared() {
        return ($self->x * $self->x + $self->y * $self->y + $self->z * $self->z);
    }
    b2Vec3 __div__(float32 a) {
        return b2Vec3($self->x / a, $self->y / a, $self->z / a);
    }
    b2Vec3 __mul__(float32 a) {
        return b2Vec3($self->x * a, $self->y * a, $self->z * a);
    }
    b2Vec3 __add__(b2Vec3* other) {
        return b2Vec3($self->x + other->x, $self->y + other->y, $self->z + other->z);
    }
    b2Vec3 __sub__(b2Vec3* other) {
        return b2Vec3($self->x - other->x, $self->y - other->y, $self->z - other->z);
    }

    b2Vec3 __rmul__(float32 a) {
        return b2Vec3($self->x * a, $self->y * a, $self->z * a);
    }
    b2Vec3 __rdiv__(float32 a) {
        return b2Vec3($self->x / a, $self->y / a, self->z / a);
    }
    void div_float(float32 a) {
        $self->x /= a;
        $self->y /= a;
        $self->z /= a;
    }
}

/**** Mat22 ****/
%extend b2Mat22 {
public:
    %pythoncode %{
        # Read-only
        inverse = property(__GetInverse, None)
        angle = property(__GetAngle, None)

    %}
    b2Vec2 __mul__(b2Vec2* other) {
        return b2Vec2($self->col1.x * other->x + $self->col2.x * other->y, $self->col1.y * other->x + $self->col2.y * other->y);
    }
    b2Mat22 __mul__(b2Mat22* other) {
        return b2Mat22(b2Mul(*($self), other->col1), b2Mul(*($self), other->col2));
    }
    b2Mat22 __add__(b2Mat22* other) {
        return b2Mat22($self->col1 + other->col1, $self->col2 + other->col2);
    }
}

%rename(__GetInverse) b2Mat22::GetInverse;
%rename(__GetAngle) b2Mat22::GetAngle;
%rename(set) b2Mat22::Set;

/**** Transform ****/
%extend b2Transform {
public:
    %pythoncode %{
        # Read-only
        angle = property(__GetAngle, None)

    %}
    b2Vec2 __mul__(b2Vec2& v) {
        float32 x = $self->position.x + $self->R.col1.x * v.x + $self->R.col2.x * v.y;
        float32 y = $self->position.y + $self->R.col1.y * v.x + $self->R.col2.y * v.y;

        return b2Vec2(x, y);
    }
}

%rename(__GetAngle) b2Transform::GetAngle;

/**** AABB ****/
%rename(__contains__) b2AABB::Contains;
%rename(__IsValid) b2AABB::IsValid;
%rename(__GetExtents) b2AABB::GetExtents;
%rename(__GetCenter) b2AABB::GetCenter;

%include "Box2D/Collision/b2Collision.h"

%feature("shadow") b2AABB::b2AABB() {
    def __init__(self, **kwargs):
        """__init__(self, **kwargs) -> b2AABB """
        _Box2D.b2AABB_swiginit(self,_Box2D.new_b2AABB())
        for key, value in kwargs.items():
            setattr(self, key, value)
}

%extend b2AABB {
public:
    %pythoncode %{
        # Read-only
        valid = property(__IsValid, None)
        extents = property(__GetExtents, None)
        center = property(__GetCenter, None)

    %}

    bool __contains__(const b2Vec2& point) {
        //If point is in aabb (including a small buffer around it), return true.
        if (point.x < ($self->upperBound.x + b2_epsilon) &&
            point.x > ($self->lowerBound.x - b2_epsilon) &&
            point.y < ($self->upperBound.y + b2_epsilon) &&
            point.y > ($self->lowerBound.y - b2_epsilon))
                return true;
        return false;
    }
    
    bool overlaps(const b2AABB& aabb2) {
        //If aabb and aabb2 overlap, return true. (modified from b2BroadPhase::InRange)
        b2Vec2 d = b2Max($self->lowerBound - aabb2.upperBound, aabb2.lowerBound - $self->upperBound);
        return b2Max(d.x, d.y) < 0.0f;
    }

}

