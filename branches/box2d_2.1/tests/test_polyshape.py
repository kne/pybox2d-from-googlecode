import unittest
from Box2D import *

class cl (b2ContactListener):
    pass

class testBasic (unittest.TestCase):
    def setUp(self):
        pass

    def test_vertices(self):
        def dotest(v):
            body = world.CreateBody(b2BodyDef(type=b2_dynamicBody, position=(0,4),
                            fixtures=[ (b2PolygonShape(vertices=v), 1.0) ]))

        self.cont_list=cl()
        world = b2World(gravity=(0,-10), doSleep=True, contactListener=self.cont_list)

        try:
            # bad vertices list
            body = world.CreateBody(b2BodyDef(type=b2_dynamicBody, position=(0,4),
                            fixtures=[ (b2PolygonShape(vertices=(2,1)), 1.0),
                                       (b2PolygonShape(box=(2,1)), 1.0) 
                                ]))
        except ValueError:
            pass # good
        else:
            raise Exception("Should have failed with ValueError")
         
        body = world.CreateBody(b2BodyDef(type=b2_dynamicBody, position=(0,4),
                        fixtures=[ (b2PolygonShape(), 1.0) ]))
        dotest([])
        dotest( [(0,1),(1,1),(-1,1)] )
        dotest( [b2Vec2(0,1),(1,1),b2Vec2(-1,1)] )
        try:
            dotest( [(0,1,5),(1,1)] )
        except ValueError,s:
            pass # good
        else:
            raise Exception("Should have failed with ValueError")

        dotest( [(0,1)]*b2_maxPolygonVertices )

        try:
            dotest( [(0,1)]*(b2_maxPolygonVertices+1) )
        except ValueError,s:
            pass # good
        else:
            raise Exception("Should have failed with ValueError")

        shape=b2PolygonShape(vertices=[(0,1),(1,1),(-1,1)] )
        shape=b2PolygonShape(vertices=[(0,0), (0,0)] )
        print shape.valid

if __name__ == '__main__':
    unittest.main()

