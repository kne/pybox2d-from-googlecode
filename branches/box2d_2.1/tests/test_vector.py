import unittest
from Box2D import b2Vec2, b2Vec3

class testVector (unittest.TestCase):
    def test_vector(self):
        x, y, z = 1.0, 2.0, 3.0
        v2 = b2Vec2(x, y)
        v3 = b2Vec3(x, y, z)

        v = v2 + v2
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)
        v = v2 - v2
        self.assertEquals(v.x, 0)
        self.assertEquals(v.y, 0)
        v = v2 / 2.0
        self.assertEquals(v.x, x/2)
        self.assertEquals(v.y, y/2)
        v = v2 * 2.0
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)
        v = 0.5 * v2
        self.assertEquals(v.x, x*0.5)
        self.assertEquals(v.y, y*0.5)
        v = 2.0 * v2
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)

        v = v3 + v3
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)
        self.assertEquals(v.z, z*2)
        v = v3 - v3
        self.assertEquals(v.x, 0)
        self.assertEquals(v.y, 0)
        self.assertEquals(v.z, 0)
        v = v3 / 2.0
        self.assertEquals(v.x, x/2)
        self.assertEquals(v.y, y/2)
        self.assertEquals(v.z, z/2)
        v = v3 * 2.0
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)
        self.assertEquals(v.z, z*2)
        v = 0.5 * v3
        self.assertEquals(v.x, x*0.5)
        self.assertEquals(v.y, y*0.5)
        self.assertEquals(v.z, z*0.5)
        v = 2.0 * v3
        self.assertEquals(v.x, x*2)
        self.assertEquals(v.y, y*2)
        self.assertEquals(v.z, z*2)

if __name__ == '__main__':
    unittest.main()


