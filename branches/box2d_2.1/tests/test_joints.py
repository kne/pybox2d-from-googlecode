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
            self.dbody1 = self.create_body((-3, 12))
            self.dbody1.userData = "dbody1"
            self.dbody2 = self.create_body((0, 12))
            self.dbody2.userData = "dbody2"
        except Exception, s:
            self.fail("Failed to create dynamic bodies (%s)" % s)

        try:
            self.sbody1 = self.create_body((0, 0), False)
            self.sbody1.userData = "sbody1"
            self.sbody2 = self.create_body((1, 4), False)
            self.sbody2.userData = "sbody2"
        except Exception, s:
            self.fail("Failed to create static bodies (%s)" % s)

    def create_body(self, position, dynamic=True):
        bodyDef = b2.b2BodyDef()
        fixtureDef = b2.b2FixtureDef()
        if dynamic:
            bodyDef.type = b2.b2_dynamicBody
            fixtureDef.density = 1
        else:
            bodyDef.type = b2.b2_staticBody
            fixtureDef.density = 0

        bodyDef.position = position
        body = self.world.CreateBody(bodyDef)
         
        dynamicBox = b2.b2PolygonShape()
        dynamicBox.SetAsBox(1, 1)

        fixtureDef.shape = dynamicBox
        fixtureDef.friction = 0.3
         
        body.CreateFixture(fixtureDef)
        return body

    def create_circle_body(self, position, dynamic=True):
        bodyDef = b2.b2BodyDef()
        fixtureDef = b2.b2FixtureDef()
        if dynamic:
            bodyDef.type = b2.b2_dynamicBody
            fixtureDef.density = 1
        else:
            bodyDef.type = b2.b2_staticBody
            fixtureDef.density = 0

        bodyDef.position = position
        body = self.world.CreateBody(bodyDef)
         
        circle = b2.b2CircleShape()
        circle.radius = 1.0

        fixtureDef = b2.b2FixtureDef()
        fixtureDef.shape = circle
        fixtureDef.density = 1
        fixtureDef.friction = 0.3
         
        body.CreateFixture(fixtureDef)
        return body

    def step_world(self, steps=10): 
        timeStep = 1.0 / 60
        vel_iters, pos_iters = 6, 2

        for i in range(steps):
            self.world.Step(timeStep, vel_iters, pos_iters)

    def check(self, dfn, joint, prop, joint_prop=""):
        a = getattr(dfn, prop)
        if joint_prop:
            b = getattr(joint, joint_prop)
        else:
            b = getattr(joint, prop)
        self.assertEquals(a, b, "(%s) %s != %s" % (prop, a, b) )

    # ---- revolute joint ----
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
        self.check(dfn, joint, "motorSpeed")
        self.check(dfn, joint, "lowerAngle", "lowerLimit")
        self.check(dfn, joint, "upperAngle", "upperLimit")
        self.check(dfn, joint, "enableMotor", "motorEnabled")
        self.check(dfn, joint, "enableLimit", "limitEnabled")
        self.check(dfn, joint, "bodyA")
        self.check(dfn, joint, "bodyB")

    def revolute_checks(self, dfn, joint):
        # check to make sure they are at least accessible 
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)
        i = joint.angle
        i = joint.motorTorque
        i = joint.speed
        i = joint.anchorA
        i = joint.anchorB
        joint.upperLimit = 2
        joint.maxMotorTorque = 10.0
        try:
            joint.foobar = 2
        except TypeError:
            pass # good

    # ---- prismatic joint ----
    def prismatic_definition(self, body1, body2, anchor, axis):
        dfn=b2.b2PrismaticJointDef()
        dfn.Initialize(body1, body2, anchor, axis)
        dfn.motorSpeed = 10
        dfn.maxMotorForce = 1000.0
        dfn.enableMotor = True
        dfn.lowerTranslation = 0
        dfn.upperTranslation = 20
        dfn.enableLimit = True
        return dfn

    def prismatic_asserts(self, dfn, joint):
        self.check(dfn, joint, "motorSpeed")
        self.check(dfn, joint, "lowerTranslation", "lowerLimit")
        self.check(dfn, joint, "upperTranslation", "upperLimit")
        self.check(dfn, joint, "enableMotor", "motorEnabled")
        self.check(dfn, joint, "enableLimit", "limitEnabled")
        self.check(dfn, joint, "bodyA")
        self.check(dfn, joint, "bodyB")
        self.check(dfn, joint, "maxMotorForce")

    def prismatic_checks(self, dfn, joint):
        # check to make sure they are at least accessible 
        i = joint.motorForce
        i = joint.anchorA
        i = joint.anchorB
        i = joint.speed
        i = joint.translation
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- distance joint ----
    def distance_definition(self, body1, body2, anchorA, anchorB):
        dfn=b2.b2DistanceJointDef()
        dfn.Initialize(body1, body2, anchorA, anchorB)
        dfn.length = (b2.b2Vec2(*anchorA) - b2.b2Vec2(*anchorB)).length
        dfn.frequencyHz = 4.0
        dfn.dampingRatio = 0.5
        return dfn

    def distance_asserts(self, dfn, joint):
        self.check(dfn, joint, "bodyA")
        self.check(dfn, joint, "bodyB")
        self.check(dfn, joint, "length")
        self.check(dfn, joint, "frequencyHz", "frequency")
        self.check(dfn, joint, "dampingRatio")

    def distance_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- pulley joint ----
    def pulley_definition(self, body1, body2):
        dfn=b2.b2PulleyJointDef()
        a, b = 2, 4
        y, L = 16, 12

        anchor1      =(body1.position.x, y + b)
        anchor2      =(body1.position.x, y + b)
        groundAnchor1=(body1.position.x, y + b + L)
        groundAnchor2=(body1.position.x, y + b + L)
        dfn.Initialize(body1, body2, groundAnchor1, groundAnchor2, anchor1, anchor2, 2.0)
        return dfn

    def pulley_asserts(self, dfn, joint):
        self.check(dfn, joint, "bodyA")
        self.check(dfn, joint, "bodyB")
        self.check(dfn, joint, "groundAnchorA")
        self.check(dfn, joint, "groundAnchorB")
        self.check(dfn, joint, "ratio")

    def pulley_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)
  
    # ---- mouse joint ----
    def mouse_definition(self, body1, body2):
        dfn=b2.b2MouseJointDef()
        dfn.bodyA = body1
        dfn.bodyB = body2
        dfn.target = (2, 1)
        dfn.maxForce = 10
        return dfn

    def mouse_asserts(self, dfn, joint):
        self.check(dfn, joint, "target")
        self.check(dfn, joint, "maxForce")
        self.check(dfn, joint, "frequencyHz", "frequency")
        self.check(dfn, joint, "dampingRatio")

    def mouse_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- line joint ----
    def line_definition(self, body1, body2, anchor, axis):
        dfn=b2.b2LineJointDef()
        dfn.Initialize(body1, body2, anchor, axis)
        dfn.motorSpeed = 0
        dfn.maxMotorForce = 100.0
        dfn.enableMotor = True
        dfn.lowerTranslation = -4.0
        dfn.upperTranslation = 4.0
        dfn.enableLimit = True
        return dfn

    def line_asserts(self, dfn, joint):
        self.check(dfn, joint, "motorSpeed")
        self.check(dfn, joint, "lowerTranslation", "lowerLimit")
        self.check(dfn, joint, "upperTranslation", "upperLimit")
        self.check(dfn, joint, "enableMotor", "motorEnabled")
        self.check(dfn, joint, "enableLimit", "limitEnabled")
        self.check(dfn, joint, "bodyA")
        self.check(dfn, joint, "bodyB")
        self.check(dfn, joint, "maxMotorForce")

    def line_checks(self, dfn, joint):
        # check to make sure they are at least accessible 
        i = joint.motorForce
        i = joint.anchorA
        i = joint.anchorB
        i = joint.speed
        i = joint.translation
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- weld joint ----
    def weld_definition(self, body1, body2):
        dfn=b2.b2WeldJointDef()
        dfn.bodyA = body1
        dfn.bodyB = body2
        return dfn

    def weld_asserts(self, dfn, joint):
        pass

    def weld_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- friction joint ----
    def friction_definition(self, body1, body2):
        dfn=b2.b2FrictionJointDef()
        dfn.bodyA = body1
        dfn.bodyB = body2
        dfn.localAnchorA = dfn.localAnchorB = (0,0)
        dfn.collideConnected = True
        dfn.maxForce = 10.0
        dfn.maxTorque = 20.0
        return dfn

    def friction_asserts(self, dfn, joint):
        self.check(dfn, joint, "maxForce")
        self.check(dfn, joint, "maxTorque")

    def friction_checks(self, dfn, joint):
        joint.GetReactionForce(1.0)
        joint.GetReactionTorque(1.0)

    # ---- ----

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
                self.fail("Failed on bodies %s and %s, joint creation (%s)" % (bodyA.userData, bodyB.userData, s))
                
            try:
                asserts(dfn, joint)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint assertions (%s)" % (bodyA.userData, bodyB.userData, s))

            try:
                checks(dfn, joint)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint checks (%s)" % (bodyA.userData, bodyB.userData, s))

            try:
                self.step_world(10)
            except Exception, s:
                self.fail("Failed on bodies %s and %s, joint simulation (%s)" % (bodyA.userData, bodyB.userData, s))

            try:
                self.world.DestroyJoint(joint)
            except Exception, s:
                self.fail("Failed on bodies %s and %s joint deletion (%s)" % (bodyA.userData, bodyB.userData, s))


    # --- the actual tests ---
    def test_revolute(self):
        self.do_joint_test("revolute", { 'anchor' : (0, 12) })

    def test_prismatic(self):
        self.do_joint_test("prismatic", { 'anchor' : (0, 0), 'axis' : (1,0) })

    def test_distance(self):
        self.do_joint_test("distance", { 'anchorA' : (-10, 0), 'anchorB' : (-0.5,-0.5) })

    def test_pulley(self):
        self.do_joint_test("pulley", {} )

    def test_mouse(self):
        self.do_joint_test("mouse", {} )

    def test_line(self):
        self.do_joint_test("line", { 'anchor' : (0, 8.5), 'axis' : (2,1) })

    def test_weld(self):
        self.do_joint_test("weld", {} )

    def test_friction(self):
        self.do_joint_test("friction", {} )

    def test_gear(self):
        # creates 2 revolute joints and then joins them, so it's done separately
        ground=self.world.CreateBody( b2.b2BodyDef() )
        shape=b2.b2PolygonShape()
        shape.SetAsEdge((50.0, 0.0), (-50.0, 0.0))
        ground.CreateFixture(shape)

        body1=self.create_circle_body((-3, 12))
        body2=self.create_circle_body(( 0, 12))

        jd1=b2.b2RevoluteJointDef() 
        jd1.Initialize(ground, body1, body1.position)
        joint1 = self.world.CreateJoint(jd1)
        
        jd2=b2.b2RevoluteJointDef() 
        jd2.Initialize(ground, body2, body2.position)
        joint2 = self.world.CreateJoint(jd2)

        gjd=b2.b2GearJointDef()
        gjd.bodyA = body1
        gjd.bodyB = body2
        gjd.joint1 = joint1
        gjd.joint2 = joint2
        gjd.ratio  = 2.0

        gj = self.world.CreateJoint(gjd)
        
        self.step_world(10)

        self.check(gjd, gj, "ratio")
        gj.GetReactionForce(1.0)
        gj.GetReactionTorque(1.0)

        self.world.DestroyJoint(gj)
        self.world.DestroyJoint(joint2)
        self.world.DestroyJoint(joint1)

if __name__ == '__main__':
    unittest.main()

