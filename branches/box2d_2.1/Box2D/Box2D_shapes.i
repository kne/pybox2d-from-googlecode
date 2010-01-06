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

    b2ShapeTypes = {
        _Box2D.b2Shape_e_unknown : "Unknown",
        _Box2D.b2Shape_e_circle  : "Circle",
        _Box2D.b2Shape_e_polygon : "Polygon", }

%}

/**** Shape ****/
%extend b2Shape {
public:
    long __hash__() { return (long)self; }
    %pythoncode %{
        __eq__ = b2ShapeCompare
        __ne__ = lambda self,other: not b2ShapeCompare(self,other)
        # Read-only
        type = property(__GetType, None)
        
    %}
}

%ignore b2Shape::m_type;
%ignore b2Shape::Clone;
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

/**** PolygonShape ****/
%extend b2PolygonShape {
public:
    %pythoncode %{
    __eq__ = b2ShapeCompare
    __ne__ = lambda self,other: not b2ShapeCompare(self,other)
    def __repr__(self):
        return "b2PolygonShape(vertices: %s)" % (self.vertices)
    def __get_vertices(self):
        """Returns all of the vertices as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
        return [ (self.__get_vertex(i).x, self.__get_vertex(i).y )
                         for i in range(0, self.vertexCount)]
    def __get_normals(self):
        """Returns all of the normals as a list of tuples [ (x1,y1), (x2,y2) ... (xN,yN) ]"""
        return [ (self.__get_normal(i).x, self.__get_normal(i).y )
                         for i in range(0, self.vertexCount)]
    def __clear_vertices(self):
        self.vertexCount=0
        for i in range(0, b2_maxPolygonVertices):
            self.__set_vertex(i, 0, 0)
    def __set_vertices(self, values):
        if not values:
            self.__clear_vertices()
        else:
            if len(values) < 2 or len(values) > b2_maxPolygonVertices:
                raise ValueError('Expected tuple or list of length >= 2 and less than b2_maxPolygonVertices=%d, got length %d.' %
                                     (b2_maxPolygonVertices, len(values)))
            for i,value in enumerate(values):
                if isinstance(value, (tuple, list)):
                    if len(value) != 2:
                        raise ValueError('Expected tuple or list of length 2, got length %d' % len(value))
                    self.__set_vertex(i, *value)
                elif isinstance(value, b2Vec2):
                    self.__set_vertex(i, value)
                else:
                    raise ValueError('Expected tuple, list, or b2Vec2, got %s' % type(value))
                self.vertexCount=i+1 # follow along in case of an exception to indicate valid number set
            if self.valid:
                self.__set_vertices_internal() # calculates normals, centroid, etc.

    def __iter__(self):
        """
        Iterates over the vertices in the polygon
        """
        for v in self.vertices:
            yield v

    def __IsValid(self):
        return b2CheckPolygon(self)

    valid = property(__IsValid, None, doc="Checks the polygon to see if it can be properly created. Raises ValueError for invalid shapes.")
    vertices = property(__get_vertices, __set_vertices)
    normals = property(__get_normals, None)
    box = property(None, lambda self, value: self.SetAsBox(*value), doc="Property replacement for running SetAsBox (Write-only)")
    edge = property(None, lambda self, value: self.SetAsEdge(*value), doc="Property replacement for running SetAsEdge (Write-only)")
    %}

    const b2Vec2* __get_vertex(uint16 vnum) {
        if (vnum >= b2_maxPolygonVertices) return NULL;
        return &( $self->m_vertices[vnum] );
    }
    const b2Vec2* __get_normal(uint16 vnum) {
        if (vnum >= b2_maxPolygonVertices) return NULL;
        return &( $self->m_normals[vnum] );
    }
    void __set_vertex(uint16 vnum, b2Vec2& value) {
        if (vnum < b2_maxPolygonVertices)
            $self->m_vertices[vnum].Set(value.x, value.y);
    }
    void __set_vertex(uint16 vnum, float32 x, float32 y) {
        if (vnum < b2_maxPolygonVertices)
            $self->m_vertices[vnum].Set(x, y);
    }
    void __set_vertices_internal() {
        $self->Set($self->m_vertices, $self->m_vertexCount);
    }
}
%rename (centroid) b2PolygonShape::m_centroid;
%rename (vertexCount) b2PolygonShape::m_vertexCount;
%rename (__set_vertices_internal) b2PolygonShape::Set;
%ignore b2PolygonShape::m_normals;
%ignore b2PolygonShape::m_vertices;
%ignore b2PolygonShape::GetVertex;
%ignore b2PolygonShape::GetVertexCount;
%ignore b2PolygonShape::vertices;
%ignore b2PolygonShape::GetVertices;
%ignore b2PolygonShape::GetNormals;

