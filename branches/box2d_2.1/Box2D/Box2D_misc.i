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
    def __getitem__(self, i): 
        if i==0:
            return self.r
        elif i==1:
            return self.g
        elif i==2:
            return self.b
        else:
            raise IndexError
    def __setitem__(self, i, value): 
        if i==0:
            self.r=value
        elif i==1:
            self.g=value
        elif i==2:
            self.b=value
        else:
            raise IndexError

    list  = property(lambda self: list(self), __SetTuple)
    bytes = property(lambda self: [int(self.r*255), int(self.g*255), int(self.b*255)], __SetBytes)
     %}

    b2Color __truediv__(float32 a) {
        return b2Color($self->r / a, $self->g / a, $self->b / a);
    }
    b2Color __div__(float32 a) {
        return b2Color($self->r / a, $self->g / a, $self->b / a);
    }
    b2Color __mul__(float32 a) {
        return b2Color($self->r * a, $self->g * a, $self->b * a);
    }
    b2Color& __isub__(b2Color& o) {
        $self->r -= o.r;
        $self->g -= o.g;
        $self->b -= o.b;
        return *($self);
    }
    b2Color& __itruediv__(b2Color& o) {
        $self->r /= o.r;
        $self->g /= o.g;
        $self->b /= o.b;
        return *($self);
    }
    b2Color& __idiv__(b2Color& o) {
        $self->r /= o.r;
        $self->g /= o.g;
        $self->b /= o.b;
        return *($self);
    }
    b2Color& __imul__(b2Color& o) {
        $self->r *= o.r;
        $self->g *= o.g;
        $self->b *= o.b;
        return *($self);
    }
    b2Color& __iadd__(b2Color& o) {
        $self->r += o.r;
        $self->g += o.g;
        $self->b += o.b;
        return *($self);
    }
     
}

/**** DistanceProxy ****/
%extend b2DistanceProxy {
public:
    %pythoncode %{
        def __get_vertices(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            return [ (self.__get_vertex(i).x, self.__get_vertex(i).y )
                             for i in range(0, self.__get_vertex_count())]

        shape = property(None, __Set, doc='The shape to be used. (read-only)')
        vertices = property(__get_vertices, None)
    %}
}

/* Shouldn't need access to these, only by setting the shape. */
%rename (__Set) b2DistanceProxy::Set;
%rename (__get_vertex) b2DistanceProxy::GetVertex;
%rename (__get_vertex_count) b2DistanceProxy::GetVertexCount;
%ignore b2DistanceProxy::m_count;
%ignore b2DistanceProxy::m_vertices;
%ignore b2DistanceProxy::m_radius;

/**** Segment ****/
%extend b2Segment {
public:
    %pythoncode %{
    %}

    PyObject* TestSegment(const b2Segment& segment, float32 maxLambda) {
        bool hit;
        float32 lambda=0.0f;
        b2Vec2 normal(0.0f ,0.0f);

        hit=$self->TestSegment(&lambda, &normal, segment, maxLambda);

        PyObject* normal_tuple=PyTuple_New(2);
        PyTuple_SetItem(normal_tuple, 0, SWIG_From_float(normal.x));
        PyTuple_SetItem(normal_tuple, 1, SWIG_From_float(normal.y));

        PyObject* ret=PyTuple_New(3);
        PyTuple_SetItem(ret, 0, SWIG_From_bool(hit));
        PyTuple_SetItem(ret, 1, SWIG_From_float(lambda));
        PyTuple_SetItem(ret, 2, normal_tuple);
        return ret;
    }
}

/**** Version ****/
%extend b2Version {
public:
    %pythoncode %{
        def __repr__(self):
            return "b2Version(%s.%s.%s)" % (self.major, self.minor, self.revision)
    %}
}

/**** DebugDraw ****/
%extend b2DebugDraw {
    %pythoncode %{
        def SetFlags(self, **kwargs):
            flags = 0
            if 'drawShapes' in kwargs and kwargs['drawShapes']:
                flags |= b2DebugDraw.e_shapeBit
            if 'drawJoints' in kwargs and kwargs['drawJoints']:
                flags |= b2DebugDraw.e_jointBit
            if 'drawAABBs' in kwargs and kwargs['drawAABBs']:
                flags |= b2DebugDraw.e_aabbBit
            if 'drawPairs' in kwargs and kwargs['drawPairs']:
                flags |= b2DebugDraw.e_pairBit
            if 'drawCOMs' in kwargs and kwargs['drawCOMs']:
                flags |= b2DebugDraw.e_centerOfMassBit
            self.__SetFlags(flags)
        %}
}

%rename (__SetFlags) b2DebugDraw::SetFlags;

