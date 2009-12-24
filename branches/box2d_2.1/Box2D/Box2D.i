/*
* Python SWIG interface file for Box2D (www.box2d.org)
*
* Copyright (c) 2008 kne / sirkne at gmail dot com
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

%module(directors="1") Box2D
%{
    #include "Box2D/Box2D.h"
//    float32 b2LineJoint::GetMaxMotorForce() const { return 0.0f; }
//       wrote my own function body for this, but hopefully itll be fixed in svn soon
%}

#note:
# swig generated names: _Box2D.<class>_<name>
# python obfuscated names: __<class>_<name>

#ifdef SWIGPYTHON
    #ifdef USE_EXCEPTIONS
        // See Common/b2Settings.h also
        %include "exception.i"

        %exception {
            try {
                $action
            } catch(b2AssertException) {
                // error already set, pass it on to python
            }
        }
    #endif

    #pragma SWIG nowarn=314
    // Add support for == and != in Python for shapes, joints, and bodies.
    %inline %{
        bool __b2PythonJointPointerEquals__(b2Joint* a, b2Joint* b) {
            return a==b;
        }
        bool __b2PythonBodyPointerEquals__(b2Body* a, b2Body* b) {
            return a==b;
        }
        bool __b2PythonShapePointerEquals__(b2Shape* a, b2Shape* b) {
            return a==b;
        }
        bool __b2PythonFixturePointerEquals__(b2Fixture* a, b2Fixture* b) {
            return a==b;
        }
    %}

    %include "Box2D/Box2D_doxygen.i"
    %include "Box2D/Box2D_printing.i"

    /* ---- features ---- */

    //Autodoc puts the basic docstrings for each function
    %feature("autodoc", "1");

    //Add callback support for the following classes:
    %feature("director") b2ContactListener;
    %feature("director") b2ContactFilter;
    %feature("director") b2BoundaryListener;
    %feature("director") b2DestructionListener;
    %feature("director") b2DebugDraw;

    // Director-exceptions are a result of callbacks that happen as a result to
    // the physics step, usually. So, catch those errors and report them back to Python.
    %exception b2World::Step {
        try { $action }
        catch (Swig::DirectorException) { SWIG_fail; }
    }
    /* ---- renames ---- */

    %rename(_GetShapeList) b2Body::GetShapeList; //Modify these to return actual lists, not linked lists
    %rename(_GetBodyList)  b2World::GetBodyList;
    %rename(_GetJointList) b2World::GetJointList;

    /* ---- handle userData ---- */
    %include "Box2D/Box2D_userdata.i"

    /* ---- classes to ignore ---- */
    //Most of these are just internal structures, so there is no need to have them
    // accessible by Python. You can safely comment out any %ignore if you for some reason
    // do need them. Shrinks the library by a bit, also.
    %ignore b2BroadPhase;
    %ignore b2Chunk;
    %ignore b2DynamicTree;
    %ignore b2DynamicTreeNode;
    %ignore b2Island;
    %ignore b2Position;
    %ignore b2Velocity;
    %ignore b2TimeStep;
    %ignore b2Simplex;
    %ignore b2SimplexVertex;
    %ignore b2SimplexCache;
    %ignore b2StackAllocator;
    %ignore b2StackEntry;

    /* ---- typemaps ---- */
    %typemap(in) b2Vec2* self {
        int res1 = SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_b2Vec2, 0);
        if (!SWIG_IsOK(res1)) {
            SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "$symname" "', argument " "$1_name"" of type '" "$1_type""'"); 
        }
    }

    //Resolve ambiguities in overloaded functions when you pass a tuple or list when 
    //SWIG expects a b2Vec2
    %typemap(typecheck,precedence=SWIG_TYPECHECK_POINTER) b2Vec2*,b2Vec2& {
       $1 = (PyList_Check($input)  || 
             PyTuple_Check($input) || 
             SWIG_CheckState(SWIG_ConvertPtr($input, 0, SWIGTYPE_p_b2Vec2, 0))
            ) ? 1 : 0;
    }

    // Allow b2Vec2* arguments be passed in as tuples or lists
    %typemap(in) b2Vec2* (b2Vec2 temp) {
        //input - $input -> ($1_type) $1 $1_descriptor
        if (PyTuple_Check($input) || PyList_Check($input)) {
            int sz = (PyList_Check($input) ? PyList_Size($input) : PyTuple_Size($input));
            if (sz != 2) {
                PyErr_Format(PyExc_TypeError, "Expected tuple or list of length 2, got length %d", PyTuple_Size($input));
                SWIG_fail;
            }
            int res1 = SWIG_AsVal_float(PySequence_GetItem($input, 0), &temp.x);
            if (!SWIG_IsOK(res1)) {
                PyErr_SetString(PyExc_TypeError,"Converting from sequence to b2Vec2, expected int/float arguments");
                SWIG_fail;
            } 
            res1 = SWIG_AsVal_float(PySequence_GetItem($input, 1), &temp.y);
            if (!SWIG_IsOK(res1)) {
                PyErr_SetString(PyExc_TypeError,"Converting from sequence to b2Vec2, expected int/float arguments");
                SWIG_fail;
            } 
        } else if ($input==Py_None) {
            temp.Set(0.0f,0.0f);
        } else {
            int res1 = SWIG_ConvertPtr($input, (void**)&$1, $1_descriptor, 0);
            if (!SWIG_IsOK(res1)) {
                SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "$symname" "', argument " "$1_name"" of type '" "$1_type""'"); 
                SWIG_fail;
            }
            temp =(b2Vec2&) *$1;
        }
        $1 = &temp;
    }

    // Allow b2Vec2& arguments be passed in as tuples or lists
    %typemap(in) b2Vec2& (b2Vec2 temp) {
        //input - $input -> ($1_type) $1 $1_descriptor
        if (PyTuple_Check($input) || PyList_Check($input)) {
            int sz = (PyList_Check($input) ? PyList_Size($input) : PyTuple_Size($input));
            if (sz != 2) {
                PyErr_Format(PyExc_TypeError, "Expected tuple or list of length 2, got length %d", PyTuple_Size($input));
                SWIG_fail;
            }
            int res1 = SWIG_AsVal_float(PySequence_GetItem($input, 0), &temp.x);
            if (!SWIG_IsOK(res1)) {
                PyErr_SetString(PyExc_TypeError,"Converting from sequence to b2Vec2, expected int/float arguments");
                SWIG_fail;
            } 
            res1 = SWIG_AsVal_float(PySequence_GetItem($input, 1), &temp.y);
            if (!SWIG_IsOK(res1)) {
                PyErr_SetString(PyExc_TypeError,"Converting from sequence to b2Vec2, expected int/float arguments");
                SWIG_fail;
            } 
        } else if ($input == Py_None) {
            temp.Set(0.0f,0.0f);
        } else {
            int res1 = SWIG_ConvertPtr($input, (void**)&$1, $1_descriptor, 0);
            if (!SWIG_IsOK(res1)) {
                SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "$symname" "', argument " "$1_name"" of type '" "$1_type""'"); 
            }
            temp =(b2Vec2&) *$1;
        }
        $1 = &temp;
    }

    //Allow access to void* types
    %typemap(in) void* {
        $1 = $input;
        Py_INCREF((PyObject*)$1);
    }
    %typemap(out) void* {
        if (!$1)
            $result=Py_None;
        else
            $result=(PyObject*)$1;

        Py_INCREF($result);
    }

    %typemap(directorin) b2Vec2* vertices {
        $input = PyTuple_New(vertexCount);
        PyObject* vertex;
        for (int i=0; i < vertexCount; i++) {
            vertex = PyTuple_New(2);
            PyTuple_SetItem(vertex, 0, PyFloat_FromDouble((float32)vertices[i].x));
            PyTuple_SetItem(vertex, 1, PyFloat_FromDouble((float32)vertices[i].y));

            PyTuple_SetItem($input, i, vertex);
        }
    }

    /* ---- ignores ---- */
    /*Re-implement these inaccessible members on the Python side:*/
    %ignore b2PolygonDef::vertices;
    %ignore b2EdgeChainDef::vertices;
    %ignore b2PolygonShape::vertices;
    %ignore b2PolygonShape::GetVertices;
    %ignore b2PolygonShape::GetNormals;

    %pythoncode %{
    def _list_from_linked_list(first):
        lst = []
        one = first

        if hasattr(one, "GetNext"):
            while one:
                lst.append(one)
                one = one.GetNext()
        else:
            while one:
                lst.append(one)
                one = one.next

        lst.reverse() # list is in reverse order
        return lst
    %}

    /* ---- extending classes ---- */
    /**** World ****/
    %extend b2World {
    public:        
        %pythoncode %{
            def __iter__(self):
                """
                Iterates over the bodies in the world
                """
                for body in self.bodies:
                    yield body

            # Read-write properties
            gravity   = property(__GetGravity   , __SetGravity)
   
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
            # CreateBody, DestroyBody, DestroyJoint
            # Step, ClearForces, DrawDebugData, QueryAABB, RayCast,
            # IsLocked
        %}
    }

    %rename (__GetGravity) b2World::GetGravity;
    %rename (__SetGravity) b2World::SetGravity;
    %rename (__GetJointList_internal) b2World::GetJointList;
    %rename (__GetBodyList_internal) b2World::GetBodyList;
    %rename (__GetContactList_internal) b2World::GetContactList;
    %rename (__SetDestructionListener) b2World::SetDestructionListener;
    %rename (__SetContactFilter) b2World::SetContactFilter;
    %rename (__SetContactListener) b2World::SetContactListener;
    %rename (__SetDebugDraw) b2World::SetDebugDraw;
    %rename (__GetContactCount) b2World::GetContactCount;
    %rename (__GetProxyCount) b2World::GetProxyCount;
    %rename (__GetBodyCount) b2World::GetBodyCount;

    /**** Fixture ****/
    %extend b2Fixture {
    public:
        long __hash__() { return (long)self; }
        
        PyObject* __GetShape() {
            b2Shape* shape=$self->GetShape();
            if (!shape)
                return NULL;

            switch (shape->GetType())
            {
            case b2Shape::e_circle:
                return SWIG_NewPointerObj(shape, $descriptor(b2CircleShape*), 0);
            case b2Shape::e_polygon:
                return SWIG_NewPointerObj(shape, $descriptor(b2PolygonShape*), 0);
            case b2Shape::e_unknown:
            default:
                return NULL;
            }
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
    %rename(__GetShape_uncasted) b2Fixture::GetShape;
    %rename(__GetAABB) b2Fixture::GetAABB;
    %rename(__GetDensity) b2Fixture::GetDensity;
    %rename(__GetBody) b2Fixture::GetBody;
    %rename(__SetSensor) b2Fixture::SetSensor;
    %rename(__SetDensity) b2Fixture::SetDensity;
    %rename(__SetFilterData) b2Fixture::SetFilterData;
    %rename(__SetFriction) b2Fixture::SetFriction;
    %rename(__SetRestitution) b2Fixture::SetRestitution;

    //Support using == on bodies, joints, and shapes
    %pythoncode %{
        def b2ShapeCompare(a, b):
            if not isinstance(a, b2Shape) or not isinstance(b, b2Shape):
                return False
            return __b2PythonShapePointerEquals__(a, b)
        def b2BodyCompare(a, b):
            if not isinstance(a, b2Body) or not isinstance(b, b2Body):
                return False
            return __b2PythonBodyPointerEquals__(a, b)
        def b2JointCompare(a, b):
            if not isinstance(a, b2Joint) or not isinstance(b, b2Joint):
                return False
            return __b2PythonJointPointerEquals__(a, b)
        def b2FixtureCompare(a, b):
            if not isinstance(a, b2Fixture) or not isinstance(b, b2Fixture):
                return False
            return __b2PythonFixturePointerEquals__(a, b)

    b2ShapeTypes = {
        _Box2D.b2Shape_e_unknown : "Unknown",
        _Box2D.b2Shape_e_circle  : "Circle",
        _Box2D.b2Shape_e_polygon : "Polygon", }

    %}

    %rename (__Length) b2Vec2::Length;
    %rename (__LengthSquared) b2Vec2::LengthSquared;
    %rename (__IsValid) b2Vec2::IsValid;

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
        __eq__ = lambda self, other: (self.x == other.x and self.y == other.y)
        __ne__ = lambda self,other: (self.x != other.x or self.y != other.y)
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
        def dot(self, v):
            """
            Dot product with v (list/tuple or b2Vec2)
            """
            if isinstance(v, (list, tuple)):
                return self.x*v[0] + self.y*v[1]
            else:
                return self.x*v.x + self.y*v.y
        def __set(self, x, y):
            self.x = x
            self.y = y
    
        tuple = property(lambda self: tuple(self.x, self.y), lambda self, value: self.__set(*value))
        length = property(__Length, None)
        lengthSquared = property(__LengthSquared, None)
        valid = property(__IsValid, None)

        %}
        b2Vec2 __div__(float32 a) { //convenience function
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

    /**** Shape ****/
    %extend b2Shape {
    public:
        long __hash__() { return (long)self; }
        %pythoncode %{
            __eq__ = b2ShapeCompare
            __ne__ = lambda self,other: not b2ShapeCompare(self,other)
            def __type_name(self):
                return b2ShapeTypes[type]
            def downcast(self):
                return (getattr(self, "__as%sShape" % self.__type_name())) ()
            # Read-only
            type = property(__GetType, None)
            
        %}

        b2CircleShape* __asCircleShape() {
            if ($self->GetType()==b2Shape::e_circle)
                return (b2CircleShape*)$self;
            return NULL;
        }

        b2PolygonShape* __asPolygonShape() {
            if ($self->GetType()==b2Shape::e_polygon)
                return (b2PolygonShape*)$self;
            return NULL;
        }
    }

    %ignore b2Shape::m_type;
    %rename(radius) b2Shape::m_radius;
    %rename(__GetType) b2Shape::GetType;

    /**** CircleShape ****/
    %extend b2CircleShape {
    public:
        %pythoncode %{
        __eq__ = b2ShapeCompare
        __ne__ = lambda self,other: not b2ShapeCompare(self,other)
        %}
    }

    %rename (pos) b2CircleShape::m_p;

    //Let python access all the vertices in the b2PolygonDef/Shape
    /**** PolygonShape ****/
    %extend b2PolygonShape {
    public:
        %pythoncode %{
        __eq__ = b2ShapeCompare
        __ne__ = lambda self,other: not b2ShapeCompare(self,other)
        def __repr__(self):
            return "b2PolygonShape(vertices: %s)" % (self.getVertices_tuple(), self.GetVertexCount())
        def __get_vertices_tuple(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append( (self.getVertex(i).x, self.getVertex(i).y ) )
            return vertices
        def __get_normals_tuple(self):
            """Returns all of the normals as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append( (self.getNormal(i).x, self.getNormal(i).y ) )
            return vertices
        def __iter__(self):
            """
            Iterates over the vertices in the polygon
            """
            for v in self.vertices:
                yield v

        vertices = property(__get_vertices_tuple, None)
        normals = property(__get_normals_tuple, None)
        %}
        const b2Vec2* __GetVertex(uint16 vnum) {
            if (vnum >= b2_maxPolygonVertices || vnum >= self->GetVertexCount()) return NULL;
            return &( $self->m_vertices[vnum] );
        }
        const b2Vec2* __GetNormal(uint16 vnum) {
            if (vnum >= b2_maxPolygonVertices || vnum >= self->GetVertexCount()) return NULL;
            return &( $self->m_normals[vnum] );
        }
    }
    %rename (centroid) b2PolygonShape::m_centroid;
    %rename (vertices) b2PolygonShape::m_vertices;
    %rename (normal) b2PolygonShape::m_normal;
    %rename (vertexCount) b2PolygonShape::m_vertexCount;
    %ignore b2PolygonShape::GetVertex;

    /**** Joint ****/
    %extend b2Joint {
    public:
        long __hash__() { return (long)self; }
        %pythoncode %{
        __eq__ = b2JointCompare
        __ne__ = lambda self,other: not b2JointCompare(self,other)
        def __setattr__(self, var, value):
            if self.__dict__.has_key(var):
                super(b2Joint, self).__setattr__(var, value)
            else: 
                raise TypeError("Shadow class has no property '%s'. Typo? (%s)" % (var, type(self)))
        __delattr__ = __setattr__

        def __type_name(self):
            """
            Return the name of the joint from:
             Unknown, Mouse, Gear, Distance, Prismatic, Pulley, Revolute
            """
            return b2JointTypes[self.type]
        def downcast(self):
            """
            Return a downcasted/typecasted version of the joint
            """
            return (getattr(self, "__as%sJoint" % self.__type_name())) ()

        # Read-only
        next = property(__GetNext, None)
        bodyA = property(__GetBodyA, None)
        bodyB = property(__GetBodyB, None)
        type = property(__GetType, None)
        active = property(__IsActive, None)

        %}

        b2MouseJoint* __asMouseJoint() {
            if ($self->GetType()==e_mouseJoint)
                return (b2MouseJoint*)$self;
            return NULL;
        }

        b2GearJoint* __asGearJoint() {
            if ($self->GetType()==e_gearJoint)
                return (b2GearJoint*)$self;
            return NULL;
        }

        b2DistanceJoint* __asDistanceJoint() {
            if ($self->GetType()==e_distanceJoint)
                return (b2DistanceJoint*)$self;
            return NULL;
        }

        b2PrismaticJoint* __asPrismaticJoint() {
            if ($self->GetType()==e_prismaticJoint)
                return (b2PrismaticJoint*)$self;
            return NULL;
        }

        b2PulleyJoint* __asPulleyJoint() {
            if ($self->GetType()==e_pulleyJoint)
                return (b2PulleyJoint*)$self;
            return NULL;
        }

        b2RevoluteJoint* __asRevoluteJoint() {
            if ($self->GetType()==e_revoluteJoint)
                return (b2RevoluteJoint*)$self;
            return NULL;
        }

        b2LineJoint* __asLineJoint() {
            if ($self->GetType()==e_lineJoint)
                return (b2LineJoint*)$self;
            return NULL;
        }
            
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

    /**** JointDef ****/
    %extend b2JointDef {
    public:
        %pythoncode %{
        def type_name(self):
            return b2JointTypes[self.type]
        %}
    }

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

    /**** Color ****/
    %extend b2Color {
    public:
        %pythoncode %{
        __iter__ = lambda self: iter((self.r, self.g, self.b)) 
         %}
    }

    
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
            # Write-only

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

    /* Additional supporting C++ code */
    %typemap(out) bool b2CheckPolygon(b2PolygonShape*) {
        if (!$1) 
            SWIG_fail;
        else
            $result = SWIG_From_bool(static_cast< bool >($1));
    }

    %feature("docstring") b2CheckPolygon "
        Checks the Polygon definition to see if upon creation it will cause an assertion.
        Raises ValueError if an assertion would be raised.

        b2PolygonDef* poly     - the polygon definition
        bool additional_checks - whether or not to run additional checks

        Additional checking: usually only in DEBUG mode on the C++ code.

        While shapes that pass this test can be created without assertions,
        they will ultimately create unexpected behavior. It's recommended
        to _not_ use any polygon that fails this test.
    ";

    %feature("docstring") b2AABBOverlaps "Checks if two AABBs overlap, or if a point
    lies in an AABB
    
    b2AABBOverlaps(AABB1, [AABB2/point])
    ";

    %inline %{
        // Add some functions that might be commonly used
        bool b2AABBOverlaps(const b2AABB& aabb, const b2Vec2& point) {
            //If point is in aabb (including a small buffer around it), return true.
            if (point.x < (aabb.upperBound.x + b2_epsilon) &&
                point.x > (aabb.lowerBound.x - b2_epsilon) &&
                point.y < (aabb.upperBound.y + b2_epsilon) &&
                point.y > (aabb.lowerBound.y - b2_epsilon))
                    return true;
            return false;
        }
        
        bool b2AABBOverlaps(const b2AABB& aabb, const b2AABB& aabb2) {
            //If aabb and aabb2 overlap, return true. (modified from b2BroadPhase::InRange)
            b2Vec2 d = b2Max(aabb.lowerBound - aabb2.upperBound, aabb2.lowerBound - aabb.upperBound);
            return b2Max(d.x, d.y) < 0.0f;
        }

        // Modified from the b2PolygonShape constructor
        // Should be as accurate as the original version
        b2Vec2 __b2ComputeCentroid(const b2Vec2* vs, int32 count) {
            b2Vec2 c; c.Set(0.0f, 0.0f);
            if (count < 3 || count >= b2_maxPolygonVertices) {
                PyErr_SetString(PyExc_ValueError, "Vertex count must be >= 3 and < b2_maxPolygonVertices");
                return c;
            }

            float32 area = 0.0f;

            // pRef is the reference point for forming triangles.
            // It's location doesn't change the result (except for rounding error).
            b2Vec2 pRef(0.0f, 0.0f);

            const float32 inv3 = 1.0f / 3.0f;

            for (int32 i = 0; i < count; ++i)
            {
                // Triangle vertices.
                b2Vec2 p1 = pRef;
                b2Vec2 p2 = vs[i];
                b2Vec2 p3 = i + 1 < count ? vs[i+1] : vs[0];

                b2Vec2 e1 = p2 - p1;
                b2Vec2 e2 = p3 - p1;

                float32 D = b2Cross(e1, e2);

                float32 triangleArea = 0.5f * D;
                area += triangleArea;

                // Area weighted centroid
                c += triangleArea * inv3 * (p1 + p2 + p3);
            }

            // Centroid
            if (area <= b2_epsilon) {
                PyErr_SetString(PyExc_ValueError, "ComputeCentroid: area <= FLT_EPSILON");
                return c;
            }

            c *= 1.0f / area;
            return c;
        }

        bool b2CheckVertices(b2Vec2* vertices, int32 count, bool additional_checks=true) {
            // Get the vertices transformed into the body frame.
            if (count < 3 || count >= b2_maxPolygonVertices) {
                PyErr_SetString(PyExc_ValueError, "Vertex count must be >= 3 and < b2_maxPolygonVertices");
                return false;
            }

            // Compute normals. Ensure the edges have non-zero length.
            b2Vec2 m_normals[b2_maxPolygonVertices];
            for (int32 i = 0; i < count; ++i)
            {
                int32 i1 = i;
                int32 i2 = i + 1 < count ? i + 1 : 0;
                b2Vec2 edge = vertices[i2] - vertices[i1];
                if (edge.LengthSquared() <= b2_epsilon * b2_epsilon) {
                    PyErr_SetString(PyExc_ValueError, "edge.LengthSquared < FLT_EPSILON**2");
                    return false;
                }
                
                m_normals[i] = b2Cross(edge, 1.0f);
                m_normals[i].Normalize();
            }

            // Compute the polygon centroid.
            b2Vec2 m_centroid = __b2ComputeCentroid(vertices, count);

            if (!additional_checks)
                return true;

            // Ensure the polygon is convex and the interior
            // is to the left of each edge.
            for (int32 i = 0; i < count; ++i)
            {
                int32 i1 = i;
                int32 i2 = i + 1 < count ? i + 1 : 0;
                b2Vec2 edge = vertices[i2] - vertices[i1];

                for (int32 j = 0; j < count; ++j)
                {
                    // Don not check vertices on the current edge.
                    if (j == i1 || j == i2)
                    {
                        continue;
                    }
                    
                    b2Vec2 r = vertices[j] - vertices[i1];

                    // Your polygon is non-convex (it has an indentation) or
                    // has colinear edges.
                    float32 s = b2Cross(edge, r);
                    if (s <= 0.0f) {
                        PyErr_SetString(PyExc_ValueError, "Your polygon is non-convex (it has an indentation) or has colinear edges.");
                        return false;
                    }
                }
            }

            return true;
        }

        bool b2CheckPolygon(b2PolygonShape *shape, bool additional_checks=true) {
            if (!shape)
                return false;

            return b2CheckVertices(shape->m_vertices, shape->m_vertexCount, additional_checks);
        }

        /* As of Box2D SVN r191, these functions are no longer in b2Math.h,
           so re-add them here for backwards compatibility */
        #define RAND_LIMIT      32767      
        // Random number in range [-1,1]
        float32 b2Random()      
        {      
                float32 r = (float32)(rand() & (RAND_LIMIT));      
                r /= RAND_LIMIT;      
                r = 2.0f * r - 1.0f;      
                return r;      
        }      
              
        /// Random floating point number in range [lo, hi]      
        float32 b2Random(float32 lo, float32 hi)      
        {      
                float32 r = (float32)(rand() & (RAND_LIMIT));      
                r /= RAND_LIMIT;      
                r = (hi - lo) * r + lo;      
                return r;      
        }

    %}
    
    /* Additional supporting Python code */
    %pythoncode %{
    b2_epsilon = 1.192092896e-07
    B2_FLT_MAX     = 3.402823466e+38
    %}

    /* Some final naming cleanups, for as of yet unused/unsupported classes */
    //b2PairManager
    %rename(broadPhase)      b2PairManager::m_broadPhase;
    %rename(callback)        b2PairManager::m_callback;
    %rename(pairs)           b2PairManager::m_pairs;
    %rename(freePair)        b2PairManager::m_freePair;
    %rename(pairCount)       b2PairManager::m_pairCount;
    %rename(pairBuffer)      b2PairManager::m_pairBuffer;
    %rename(pairBufferCount) b2PairManager::m_pairBufferCount;
    %rename(hashTable)       b2PairManager::m_hashTable;

    //b2BroadPhase
    %rename(pairManager)        b2BroadPhase::m_pairManager;
    %rename(proxyPool)          b2BroadPhase::m_proxyPool;
    %rename(freeProxy)          b2BroadPhase::m_freeProxy;
    %rename(bounds)             b2BroadPhase::m_bounds;
    %rename(queryResults)       b2BroadPhase::m_queryResults;
    %rename(querySortKeys)      b2BroadPhase::m_querySortKeys;
    %rename(queryResultCount)   b2BroadPhase::m_queryResultCount;
    %rename(worldAABB)          b2BroadPhase::m_worldAABB;
    %rename(quantizationFactor) b2BroadPhase::m_quantizationFactor;
    %rename(proxyCount)         b2BroadPhase::m_proxyCount;
    %rename(timeStamp)          b2BroadPhase::m_timeStamp;

    //b2Contact
    %rename(flags)             b2Contact::m_flags;
    %rename(manifoldCount)     b2Contact::m_manifoldCount;
    %rename(prev)              b2Contact::m_prev;
    %rename(next)              b2Contact::m_next;
    %rename(node1)             b2Contact::m_node1;
    %rename(node2)             b2Contact::m_node2;
    %rename(shape1)            b2Contact::m_shape1;
    %rename(shape2)            b2Contact::m_shape2;
    %rename(toi)               b2Contact::m_toi;

    //b2ContactManager
    %rename(world)             b2ContactManager::m_world;
    %rename(nullContact)       b2ContactManager::m_nullContact;
    %rename(destroyImmediate)  b2ContactManager::m_destroyImmediate;

#endif

%include "Box2D/Box2D.h"

