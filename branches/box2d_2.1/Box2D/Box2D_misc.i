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

/* ---- miscellaneous classes ---- */
/**** Color ****/
%extend b2Color {
public:
    %pythoncode %{
    __iter__ = lambda self: iter((self.r, self.g, self.b)) 
    def __SetBytes(self, value):
        if len(value) != 3:
            raise ValueError('Expected length 3 list')
        self.r, self.g, self.b = value[0]/255, value[1]/255, value[2]/255
    def __SetTuple(self, value):
        if len(value) != 3:
            raise ValueError('Expected length 3 list')
        self.r, self.g, self.b = value[0], value[1], value[2]

    list  = property(lambda self: list(self), __SetTuple)
    bytes = property(lambda self: [int(self.r*255), int(self.g*255), int(self.b*255)], __SetBytes)
     %}

    b2Color __div__(float32 a) {
        return b2Color($self->r / a, $self->g / a, $self->b / a);
    }
    b2Color __mul__(float32 a) {
        return b2Color($self->r * a, $self->g * a, $self->b * a);
    }
     
}

/**** Contact ****/
%extend b2Contact {
public:
    %pythoncode %{
        # Read-write properties
        sensor = property(__IsSensor, __SetSensor)
        enabled = property(__IsEnabled, __SetEnabled)

        # Read-only
        next = property(__GetNext, None)
        touching = property(__IsTouching, None)
        fixtureB = property(__GetFixtureB, None)
        fixtureA = property(__GetFixtureA, None)
        continuous = property(__IsContinuous, None)
        manifold = property(__GetManifold, None)

    %}
}

%rename(__GetNext) b2Contact::GetNext;
%rename(__IsTouching) b2Contact::IsTouching;
%rename(__IsSensor) b2Contact::IsSensor;
%rename(__GetFixtureB) b2Contact::GetFixtureB;
%rename(__GetFixtureA) b2Contact::GetFixtureA;
%rename(__IsContinuous) b2Contact::IsContinuous;
%rename(__GetManifold) b2Contact::GetManifold;
%rename(__IsEnabled) b2Contact::IsEnabled;
%rename(__SetEnabled) b2Contact::SetEnabled;
%rename(__SetSensor) b2Contact::SetSensor;

