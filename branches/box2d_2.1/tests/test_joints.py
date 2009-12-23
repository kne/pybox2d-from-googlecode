import unittest
import Box2D as b2
import itertools

class testBasic (unittest.TestCase):
    world = None
    dbody1 = None
    dbody2 = None
    sbody1 = None
    sbody2 = None
    def setUp(self):
        try:
            self.world = b2.b2World(b2.b2Vec2(0.0, -10.0), True)
        except Exception, s:
            self.fail("Failed to create world (%s)" % s)

        try:
            self.dbody1 = self.create_body((0, 1))
            self.dbody1.userData = "dbody1"
            self.dbody2 = self.create_body((0, 3))
            self.dbody2.userData = "dbody2"
        except Exception, s:
            self.fail("Failed to create dynamic bodies (%s)" % s)

        try:
            self.sbody1 = self.create_body((1, 2), False)
            self.sbody1.userData = "sbody1"
            self.sbody2 = self.create_body((1, 4), False)
            self.sbody2.userData = "sbody2"
        except Exception, s:
            self.fail("Failed to create static bodies (%s)" % s)

    def create_body(self, position, dynamic=True):
        bodyDef = b2.b2BodyDef()
        if dynamic:
            bodyDef.type = b2.b2_dynamicBody
        else:
            bodyDef.type = b2.b2_staticBody

        bodyDef.position = position
        body = self.world.CreateBody(bodyDef)
         
        dynamicBox = b2.b2PolygonShape()
        dynamicBox.SetAsBox(1, 1)

        fixtureDef = b2.b2FixtureDef()
        fixtureDef.shape = dynamicBox
        fixtureDef.density = 1
        fixtureDef.friction = 0.3
         
        body.CreateFixture(fixtureDef)
        return body

    def step_world(self): 
        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6, 2

        for i in range(60):
            world.Step(timeStep, vel_iters, pos_iters)
            world.ClearForces()

    def revolute_definition(self, body1, body2, anchor):
        dfn=b2.b2RevoluteJointDef()
        dfn.Initialize(body1, body2, anchor)
        dfn.motorSpeed = 1.0 * b2.b2_pi
        dfn.maxMotorTorque = 10000.0
        dfn.enableMotor = False
        dfn.lowerAngle = -0.25 * b2.b2_pi
        dfn.upperAngle = 0.5 * b2.b2_pi
        dfn.enableLimit = True
        dfn.collideConnected = True
        return dfn

    def revolute_asserts(self, dfn, joint):
        self.assertEqual(dfn.motorSpeed, joint.motorSpeed)
        self.assertEqual(dfn.lowerAngle, joint.lowerLimit)
        self.assertEqual(dfn.upperAngle, joint.upperLimit)
        self.assertEqual(dfn.enableMotor, joint.motorEnabled)
        self.assertEqual(dfn.enableLimit, joint.limitEnabled)
        self.assertEqual(dfn.bodyA, joint.bodyA)
        self.assertEqual(dfn.bodyB, joint.bodyB)

    def revolute_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)
        i = joint.jointAngle
        i = joint.motorTorque
        i = joint.jointSpeed
        i = joint.anchorA
        i = joint.anchorB
        joint.maxMotorTorque = 10.0

    def do_joint_test(self, name, init_args):
        create  = getattr(self, "%s_definition"%name)
        asserts = getattr(self, "%s_asserts"%name)
        checks  = getattr(self, "%s_checks"%name)

        for bodyA, bodyB in itertools.permutations( ( self.sbody1, self.sbody2, self.dbody1, self.dbody2), 2 ):
            try:
                dfn = create(body1=bodyA, body2=bodyB, **init_args)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint definition (%s)" % (bodyA.userData, bodyB.userData, s))

            try:
                joint = self.world.CreateJoint(dfn)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint definition (%s)" % (bodyA.userData, bodyB.userData, s))
                
            try:
                asserts(dfn, joint)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint assertions (%s)" % (bodyA.userData, bodyB.userData, s))

            try:
                self.world.DestroyJoint(joint)
            except Exception, s:
                self.fail("Failed on bodies %s and %s joint deletion (%s)" % (bodyA.userData, bodyB.userData, s))

    def test_revolute(self):
        name = "revolute"
        self.do_joint_test(name, { 'anchor' : (0, 12) })
        
if __name__ == '__main__':
    unittest.main()

