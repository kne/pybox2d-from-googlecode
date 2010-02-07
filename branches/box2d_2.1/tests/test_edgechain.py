import unittest
import Box2D

class testEdgeChain (unittest.TestCase):
    def setUp(self):
        pass

    def test_world(self):
        world = Box2D.b2World()

        ground = world.CreateBody(position=(0, 20))

        try:
            ground.CreateEdgeChain([])
        except ValueError:
            pass #good
        except Exception as s:
            self.fail("Failed to create empty edge chain (%s)" % s)

        try:
            ground.CreateEdgeChain(
                                [ (-20,-20),
                                  (-20, 20),
                                  ( 20, 20),
                                  ( 20,-20),
                                  (-20,-20) ]
                                )
        except Exception as s:
            self.fail("Failed to create valid edge chain (%s)" % s)

if __name__ == '__main__':
    unittest.main()

