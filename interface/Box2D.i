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

#todo: use enumerate
#implement the checkDef() code here
%module(directors="1") Box2D2
%{
    #include "../Include/Box2D.h"
    
    //Define these functions so that SWIG does not fail
    void b2BroadPhase::ValidatePairs() { }

%}

#ifdef SWIGPYTHON
    
    #ifdef TARGET_FLOAT32_IS_FIXED
        //figure out what to do here :)
        %include "Box2D_fixed.i"
    #endif

    //Autodoc puts the basic docstrings for each function
    %feature("autodoc", "1");

    //Add callback support for the following classes:
    %feature("director") b2ContactListener;
    %feature("director") b2BoundaryListener;
    %feature("director") b2DestructionListener;
    %feature("director") b2DebugDraw;

    //These operators do not work unless explicitly defined like this 
    %rename(b2add) operator  + (const b2Vec2& a, const b2Vec2& b);
    %rename(b2add) operator  + (const b2Mat22& A, const b2Mat22& B);
    %rename(b2sub) operator  - (const b2Vec2& a, const b2Vec2& b);
    %rename(b2mul) operator  * (float32 s, const b2Vec2& a);
    %rename(b2equ) operator == (const b2Vec2& a, const b2Vec2& b);
    
    //Since Python (apparently) requires __imul__ to return self,
    //these void operators will not do. So, rename them, then call them
    //with Python code, and return self. (see further down in b2Vec2)
    %rename(add_vector) b2Vec2::operator += (const b2Vec2& v);
    %rename(sub_vector) b2Vec2::operator -= (const b2Vec2& v);
    %rename(mul_float ) b2Vec2::operator *= (float32 a);

    /*%ignore b2Shape::GetUserData;
    %ignore b2Body::GetUserData;
    %ignore b2Joint::GetUserData;*/

    //Allow access to (m_)userData
    %typemap(in) void* userData, void* m_userData {
        //In
        if ($input == Py_None) {
            $1 = NULL;
        } else {
            $1 = (void*)( $input );
            Py_INCREF($input);
        }
    }

    %typemap(out) void* userData, void* m_userData {
        //Out
        if ($1 == NULL) {
            $result = Py_None;
        } else {
            $result = (PyObject*)( $1 );
        }
        Py_INCREF($result);
    }


    %extend b2World {
    public:
        PyObject* Query(const b2AABB& aabb, uint32 maxCount) {
            PyObject* ret=Py_None;
            b2Shape** shapes=(b2Shape**)malloc(maxCount * sizeof(b2Shape*));

            if (!shapes) {
                PyErr_SetString(PyExc_MemoryError, "Insufficient memory");
                return ret;
            }

            int32 num=$self->Query(aabb, shapes, maxCount);
            if (num < 0)
                num = 0;

            ret = PyTuple_New(2);
            
            PyObject* shapeList=PyTuple_New(num);
            PyObject* shape;

            for (int i=0; i < num; i++) {
                shape=SWIG_NewPointerObj(SWIG_as_voidptr(shapes[i]), SWIGTYPE_p_b2Shape, 0 );
                PyTuple_SetItem(shapeList, i, shape);
            }

            PyTuple_SetItem(ret, 0, SWIG_From_int(num));
            PyTuple_SetItem(ret, 1, shapeList);

            free(shapes);
            return ret;
        }
    }

    /*
    //hmm
    %feature("director:except") {
        if ($error != NULL) {
            throw Swig::DirectorMethodException();
        }
    }*/
        
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

    // memory leak with vertices, I think :(

    %feature("shadow") GetUserData {
        def GetUserData(self): # override the C++ version as it does not work. 
            """Get the specified userData (m_userData)"""
            return self.pyGetUserData()
    }

    //Typecast the shape as necessary so Python can use them properly (2.0)
    %include "Collision/Shapes/b2Shape.h"
    %extend b2Shape {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Shape(from Body %s )" % (self.GetBody())
        def typeName(self):
            types = {  e_unknownShape   : "Unknown",
                        e_circleShape   : "Circle",
                        e_polygonShape  : "Polygon",
                        e_shapeTypeCount: "ShapeType" }
            return types[self.GetType()]
        def getAsType(self):
            """Return a typecasted version of the shape"""
            return (getattr(self, "as%s" % self.typeName())) ()
        %}
        b2CircleShape* asCircle() {
            if ($self->GetType()==e_circleShape)
                return (b2CircleShape*)$self;
            return NULL;
        }
        b2PolygonShape* asPolygon() {
            if ($self->GetType()==e_polygonShape)
                return (b2PolygonShape*)$self;
            return NULL;
        }
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }
    }
   
    //Generic joint information
    %pythoncode %{
        def b2JointInfo(self):
            """Return a rather verbose string representation of a joint"""
            props = dir(self)
            ignoreList = ('this', 'thisown', 'next', 'prev', 'm_next', 'm_prev')
            info  = []
            for prop in dir(self):
                if prop[:2]=='__' or prop in ignoreList: continue
                if not callable(getattr(self, prop)): 
                    info.append(prop + ":")
                    info.append(str(getattr(self, prop)))
            return "%s(%s)" % (self.__class__.__name__, " ".join(info))
    %}

    %extend b2MouseJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }

    %extend b2GearJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }

    %extend b2DistanceJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }

    %extend b2PrismaticJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }
 
   %extend b2PulleyJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }

   %extend b2RevoluteJoint {
    public:
        %pythoncode %{
        def __repr__(self):
            return b2JointInfo(self)
        %}
    }

    %include "Dynamics/Joints/b2Joint.h"

    %extend b2JointDef {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2JointDef(body1: %s body2: %s)" % (self.body1, self.body2)
        def typeName(self):
            types = { e_unknownJoint  : "Unknown",
                      e_mouseJoint    : "Mouse", 
                      e_gearJoint     : "Gear",
                      e_distanceJoint : "Distance",
                      e_prismaticJoint: "Prismatic",
                      e_pulleyJoint   : "Pulley",
                      e_revoluteJoint : "Revolute" }
            return types[self.GetType()]
        %}
    }

    %extend b2Joint {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Joint(m_body1: %s m_body2: %s getAsType(): %s)" % (self.m_body1, self.m_body2, self.getAsType())
        def typeName(self):
            types = { e_unknownJoint  : "Unknown",
                      e_mouseJoint    : "Mouse", 
                      e_gearJoint     : "Gear",
                      e_distanceJoint : "Distance",
                      e_prismaticJoint: "Prismatic",
                      e_pulleyJoint   : "Pulley",
                      e_revoluteJoint : "Revolute" }
            return types[self.GetType()]
        def getAsType(self):
            """Return a typecasted version of the joint"""
            return (getattr(self, "as%sJoint" % self.typeName())) ()
        %}
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }

        b2MouseJoint* asMouseJoint() {
            if ($self->GetType()==e_mouseJoint)
                return (b2MouseJoint*)$self;
            return NULL;
        }

        b2GearJoint* asGearJoint() {
            if ($self->GetType()==e_gearJoint)
                return (b2GearJoint*)$self;
            return NULL;
        }

        b2DistanceJoint* asDistanceJoint() {
            if ($self->GetType()==e_distanceJoint)
                return (b2DistanceJoint*)$self;
            return NULL;
        }

        b2PrismaticJoint* asPrismaticJoint() {
            if ($self->GetType()==e_prismaticJoint)
                return (b2PrismaticJoint*)$self;
            return NULL;
        }

        b2PulleyJoint* asPulleyJoint() {
            if ($self->GetType()==e_pulleyJoint)
                return (b2PulleyJoint*)$self;
            return NULL;
        }

        b2RevoluteJoint* asRevoluteJoint() {
            if ($self->GetType()==e_revoluteJoint)
                return (b2RevoluteJoint*)$self;
            return NULL;
        }
    }

    %ignore b2PolygonShape::GetVertices; //Inaccessible 

    //Let python access all the vertices in the b2PolygonDef/Shape
    %extend b2PolygonShape {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PolygonShape(vertices: %s count: %d)" % (self.getVertices_tuple(), self.vertexCount)
        def getVertices_tuple(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.vertexCount):
                vertices.append( (self.getVertex(i).x, self.getVertex(i).y ) )
            return vertices
        def getVertices_b2Vec2(self):
            """Returns all of the vertices as a list of b2Vec2's [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.GetVertexCount()):
                vertices.append(self.getVertex(i))
            return vertices
        %}
        const b2Vec2* getVertex(uint16 vnum) {
            if (vnum > b2_maxPolygonVertices || vnum > self->GetVertexCount()) return NULL;
            return &( $self->GetVertices() [vnum] );
        }
    }
    
    %extend b2PolygonDef{
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2PolygonDef(vertices: %s count: %d)" % (self.getVertices_tuple(), self.vertexCount)
        def getVertices_tuple(self):
            """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.vertexCount):
                vertices.append( (self.getVertex(i).x, self.getVertex(i).y ) )
            return vertices
        def getVertices_b2Vec2(self):
            """Returns all of the vertices as a list of b2Vec2's [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
            vertices = []
            for i in range(0, self.vertexCount):
                vertices.append(self.getVertex(i))
            return vertices
        def setVertices_tuple(self, vertices):
            """Sets all of the vertices (up to b2_maxPolygonVertices) given a tuple 
                in the format ( (x1,y1), (x2,y2) ... (xN,yN) )"""
            if len(vertices) > b2_maxPolygonVertices:
                raise ValueError
            self.vertexCount = len(vertices)
            for i in range(0, self.vertexCount):
                self.setVertex(i, vertices[i][0], vertices[i][1])
        def setVertices_b2Vec2(self, vertices):
            """Sets all of the vertices (up to b2_maxPolygonVertices) given a tuple 
                in the format ( (x1,y1), (x2,y2) ... (xN,yN) ) where each vertex
                is a b2Vec2"""
            if len(vertices) > b2_maxPolygonVertices:
                raise ValueError
            self.vertexCount = len(vertices)
            for i in range(0, self.vertexCount):
                self.setVertex(i, vertices[i])
        %}
        b2Vec2* getVertex(uint16 vnum) {
            if (vnum > b2_maxPolygonVertices || vnum > self->vertexCount) return NULL;
            return &( $self->vertices[vnum] );
        }
        void setVertex(uint16 vnum, b2Vec2& value) {
            if (vnum > b2_maxPolygonVertices) return;
            $self->vertices[vnum].Set(value.x, value.y);
        }
        void setVertex(uint16 vnum, float32 x, float32 y) {
            if (vnum > b2_maxPolygonVertices) return;
            $self->vertices[vnum].Set(x, y);
        }
    }

    //Extend the vector class to support Python print statements
    //Also, add vector addition and scalar multiplication
    %extend b2Vec2 {
        %pythoncode %{
        def __repr__(self):
            return "b2Vec2(%g,%g)" % (self.x, self.y)
        def tuple(self):
            return (self.x, self.y)
        def fromTuple(self, tuple):
            self.x, self.y = tuple
            return self
        def copy(self):
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
        b2Vec2 __rdiv__(float32 a) { //perhaps not _correct_, but convenient
            return b2Vec2($self->x / a, $self->y / a);
        }
        void div_float(float32 a) {
            self->x /= a;
            self->y /= a;
        }
    }

    //Pretty printing section
    %extend b2Body {
        %pythoncode %{
        def __repr__(self):
            return "b2Body(Position: %s)" % (self.GetPosition())
        %}
        PyObject* pyGetUserData() {
            PyObject* ret=(PyObject*)self->GetUserData();
            Py_INCREF(ret);
            return ret;
        }
    }

    %extend b2ContactID_features {
        %pythoncode %{
        def __repr__(self):
            return "b2ContactID::Features(\n\treferenceFace: %d incidentEdge: %d incidentVertex: %d flip: %d)" % \
                (self.referenceFace, self.incidentEdge, self.incidentVertex, self.flip)
        %}
    }
    %extend b2ContactID {
        %pythoncode %{
        def __repr__(self):
            return "b2ContactID(key: %d Features: \n\t%s)" % \
                (self.key, self.features)
        %}
    }

    %extend b2ContactPoint {
        %pythoncode %{
        def __repr__(self):
            return "b2ContactPoint(\n\tid: %s\n\tshape1: %s\n\tshape2: %s\n\tposition: %s\n\tnormal: %s\n\tseparation: %f normalForce: %f tangentForce: %f)" % \
                (self.id, self.shape1, self.shape2, self.position, self.normal, self.separation, self.normalForce, self.tangentForce)
        %}
    }

    %extend b2JointEdge {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2JointEdge(other: %s)" % (self.other)
        %}
    }
    
    %extend b2Jacobian {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Jacobian(linear1: %s: linear2: %s angular1: %s angular2: %s)" %\
                (self.linear1, self.linear2, self.angular1, self.angular2)
        %}
    }

    %extend b2Mat22 {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Mat22(col1: %s col2: %s)" % (self.col1, self.col2)
        %}
    }

    %extend b2Color {
    public:
        %pythoncode %{
        def __repr__(self):
            return "b2Color(RGB: %g,%g,%g)" % (self.r, self.g, self.b)
        %}
    }


#endif

%include "../Include/Box2D.h"


