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

/**** b2GetPointStates ****/
%inline {
    PyObject* b2GetPointStates(const b2Manifold* manifold1, const b2Manifold* manifold2) {
        PyObject* ret=NULL;
        b2PointState state1[b2_maxManifoldPoints], state2[b2_maxManifoldPoints];

        if (!manifold1 || !manifold2)
            return NULL;

        b2GetPointStates(state1, state2, manifold1, manifold2);

        ret = PyTuple_New(2);
        
        int state1_length=-1, state2_length=-1;
        PyObject* state1_t=Py_None;
        PyObject* state2_t=Py_None;
        for (int i=0; i < b2_maxManifoldPoints; i++) {
            if (state1[i]==b2_nullState && state1_length==0)
                state1_length=i;
                if (state2_length > -1)
                    break;
            if (state2[i]==b2_nullState && state2_length==0)
                state2_length=i;
                if (state1_length > -1)
                    break;
        }

        if (state1_length < 0)
            state1_length = b2_maxManifoldPoints;
        if (state2_length < 0)
            state2_length = b2_maxManifoldPoints;

        if (state1_length > -1)
            state1_t=PyTuple_New(state1_length);
        else
            Py_INCREF(state1_t);

        if (state2_length > -1)
            state2_t=PyTuple_New(state2_length);
        else
            Py_INCREF(state2_t);

        PyTuple_SetItem(ret, 0, state1_t);
        PyTuple_SetItem(ret, 1, state2_t);

        for (int i=0; i < b2Max(state1_length, state2_length); i++) {
            if (i < state1_length)
                PyTuple_SetItem(state1_t, i, SWIG_From_int(state1[i]));
            if (i < state2_length)
                PyTuple_SetItem(state2_t, i, SWIG_From_int(state2[i]));
        }
        return ret;
   }
}
%ignore b2GetPointStates;

/**** Manifold ****/
%rename (localPlaneNormal) b2Manifold::m_localPlaneNormal;
%rename (localPoint) b2Manifold::m_localPoint;
%rename (pointCount) b2Manifold::m_pointCount;
%rename (type_) b2Manifold::m_type;
%ignore b2Manifold::m_points;

%extend b2Manifold {
public:
    %pythoncode %{
        def __setattr__(self, var, value): raise Exception("Type %s is immutable" % self.__class__.__name__)
        __delattr__ = __setattr__
        def __GetPoints(self):
            return [self.__GetPoint(i) for i in range(self.pointCount)]
        points = property(__GetPoints, None)
    %}

    b2ManifoldPoint* __GetPoint(int i) {
        if (i >= b2_maxManifoldPoints || i >= $self->m_pointCount)
            return NULL;
        return &( $self->m_points[i] );
    }
    
}

/**** WorldManifold ****/
%rename (normal) b2WorldManifold::m_normal;
%ignore b2WorldManifold::m_points;

%extend b2WorldManifold {
public:
    %pythoncode %{
        def __setattr__(self, var, value): raise Exception("Type %s is immutable" % self.__class__.__name__)
        __delattr__ = __setattr__
    %}

    PyObject* __GetPoints() {
        PyObject* ret=PyTuple_New(b2_maxManifoldPoints);
        PyObject* point;
        for (int i=0; i < b2_maxManifoldPoints; i++) {
            point = PyTuple_New(2);
            PyTuple_SetItem(point, 0, PyFloat_FromDouble((float32)$self->m_points[i].x));
            PyTuple_SetItem(point, 1, PyFloat_FromDouble((float32)$self->m_points[i].y));

            PyTuple_SetItem(ret, i, point);
        }
        return ret;
    }
    %pythoncode %{
        points = property(__GetPoints, None)
    %}
}


/**** Contact ****/
%extend b2Contact {
public:
    %pythoncode %{
        def __GetWorldManifold(self):
            ret=b2WorldManifold()
            self.__GetWorldManifold_internal(ret)
            return ret

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
        worldManifold = property(__GetWorldManifold, None)

    %}
}

%rename(__GetNext) b2Contact::GetNext;
%rename(__IsTouching) b2Contact::IsTouching;
%rename(__IsSensor) b2Contact::IsSensor;
%rename(__GetFixtureB) b2Contact::GetFixtureB;
%rename(__GetFixtureA) b2Contact::GetFixtureA;
%rename(__IsContinuous) b2Contact::IsContinuous;
%rename(__GetManifold) b2Contact::GetManifold;
%rename(__GetWorldManifold_internal) b2Contact::GetWorldManifold;
%rename(__IsEnabled) b2Contact::IsEnabled;
%rename(__SetEnabled) b2Contact::SetEnabled;
%rename(__SetSensor) b2Contact::SetSensor;

/**** Create our own ContactPoint structure ****/
/* And allow kwargs for it */

%feature("shadow") b2ContactPoint::b2ContactPoint() {
    def __init__(self, **kwargs):
        """__init__(self, **kwargs) -> b2ContactPoint """
        _Box2D.b2ContactPoint_swiginit(self,_Box2D.new_b2ContactPoint())
        for key, value in list(kwargs.items()):
            setattr(self, key, value)
}

%inline {
    class b2ContactPoint
    {
    public:
        b2ContactPoint() : fixtureA(NULL), fixtureB(NULL), state(b2_nullState) {
            normal.SetZero();
            position.SetZero();
        }
        ~b2ContactPoint() {}

        b2Fixture* fixtureA;
        b2Fixture* fixtureB;
        b2Vec2 normal;
        b2Vec2 position;
        b2PointState state;
    };
}

