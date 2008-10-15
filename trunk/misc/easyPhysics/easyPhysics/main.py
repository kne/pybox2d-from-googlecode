#!/usr/bin/env python
#
# Copyright (c) 2008 kne / sirkne at gmail dot com
# 
# Implemented using the pybox2d SWIG interface for Box2D (pybox2d.googlecode.com)
# 
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.


import box2d
from locals import *

# globals
debug_level = 0

# helper functions
def debugstr(level, string):
    global debug_level
    if debug_level >= level:
        print "(ep)", string

def _dict_format(d, indent=0):
    ret = ["{"]
    max_keylen = max( [len(key) for key in d.keys()] ) + 1

    for key in d.keys():
       if isinstance(d[key], dict):
           ret.append( _dict_format(d[key], indent+1) )
       else:
           ret.append(" %s%s: %s" % (key, ' ' * (max_keylen - len(key)), d[key]))
    ret.append("}")
    return ( '\n' + (indent * ' ') ).join(ret)

# classes
class CollisionClass (object):
    def add(self, info): #todo: change to appropriate args
        pass
    def persist(self, info):
        pass
    def delete(self, info):
        pass

class Renderer (object):
# notes:
# warn if scale functions not symmetric
# warn if scale is small (<= world 1:screen 2 ?)
# have basic w2s/s2w functions setup for common libraries, given scale
#  -- updatable by functions or camera tracking
    world_center=None
    screen_center=None

    world_aabb=None
    screen_aabb=None

    zoom=1.0
    offset=None
    screen_dim=None

    def __repr__(self):
        return "(Renderer)"

    def render_object(self, **kw):
        pass

    def expand_vector(self, vector):
        """Expands a vector into x, y components. If
        - vector is a b2Vec2:
          x, y = _expand_vector(a) # returns a.x, a.y
        - vector is a tuple/list
          x, y = _expand_vector(a) # returns a[0], a[1]
        """
        if isinstance(vector, (list, tuple)):
            return vector[0], vector[1]
        elif isinstance(vector, box2d.b2Vec2):
            return v.x, v.y
        else:
            raise TypeError, "Unexpected type"
    def _preset_same_type(self, input, output):
        """
        Make output the same type as input
        Assumes 'output' in list/tuple format
        E.g.,
         Input is tuple/list, returns list form of output
         Input is b2Vec2    , return b2Vec2 form of output
        """
        if isinstance(world, (list, tuple)):
            return output
        else:
            return box2d.b2Vec2().fromTuple(output)

    def set_scale_preset(self, preset_name):
        """Set the scale function to one of the built-in presets.
        If you are using pygame, try:
            set_scale_preset("pygame")
        Other options are:
            'pyglet', 'equal'

        NOTE:
        You can also set the w2s functions yourself by implementing
        or setting Renderer.w2s and s2w to your functions. Be sure to
        follow the necessary input/output requirements, as seen in
        the preset examples.
        """
        def w2s_preset_equal(world):
            x, y = self.expand_vector(world)
            return self._preset_same_type( world, (x, y))
        def s2w_preset_equal(screen):
            x, y = self.expand_vector(screen)
            return self._preset_same_type( screen, (x, y))

        def w2s_preset_pygame(world):
            x, y = self.expand_vector(world)
            return self._preset_same_type( world, (
                    (x * self.zoom) - self.offset.x, 
                    screen_dim.y - ((y * self.zoom) - self.offset.y)
                    ) )
        def s2w_preset_pygame(screen):
            x, y = self.expand_vector(screen)
            return self._preset_same_type( screen, (
                    (x + self.offset.x) / self.zoom, 
                    ((self.screen_dim.y - y + self.offset.y) / self.zoom)
                ) )

        def w2s_preset_pyglet(world):
            """ Pyglet world to screen preset
            Assumes using OpenGL projection and conversion is unnecessary.
            Returns world point intact.
            """
            x, y = self.expand_vector(world)
            return self._preset_same_type( world, (x, y) )
        def s2w_preset_pyglet(screen):
            """ Pyglet screen to world preset
            Assumes OpenGL projection code similar to that used in the testbed
            Might require some tweaking if not (a change of 'extents')
            """
            u = float(screen.x) / self.screen_dim.x
            v = float(screen.y) / self.screen_dim.y

            ratio = float(self.screen_dim.x) / self.screen_dim.y
            extents = box2d.b2Vec2(ratio * 25.0, 25.0)
            extents *= self.zoom

            lower = self.screen_center - extents
            upper = self.screen_center + extents

            worldx = (1.0 - u) * lower.x + u * upper.x
            worldy = (1.0 - v) * lower.y + v * upper.y
            return self._preset_same_type( screen, (worldx, worldy) )

        w2s = "w2s_preset_%s" % preset_name
        s2w = "s2w_preset_%s" % preset_name
        if w2s in locals() and s2w in locals():
            self.w2s = locals()[w2s]
            self.s2w = locals()[s2w]
            debugstr(2, "Scale preset '%s' used" % preset_name)
        else:
            raise ep_InvalidScalingFunction, preset_name

def _type_check(type_, value):
    if type_ == box2d.b2AABB:
        if isinstance(value, (list, tuple)):
            if len(value) != 4:
                raise ep_InvalidParameter, "Expected length-4 list or tuple (%s)" % key
            aabb = box2d.b2AABB()
            aabb.lowerBound.Set(*value[0:2])
            aabb.upperBound.Set(*value[2:4])
            return aabb
        elif isinstance(value, box2d.b2AABB):
            # note that this does not copy your AABB
            return value
        else:
            raise ep_InvalidParameter, "Expected length-4 list or tuple or b2AABB (%s)" % key

    elif type_ == box2d.b2Vec2:
        if isinstance(value, (list, tuple)):
            if len(value) != 2:
                raise ep_InvalidParameter, "Expected length-2 list or tuple (%s)" % key
            return box2d.b2Vec2().fromTuple(value)
        elif isinstance(value, box2d.b2Vec2):
            # copies the b2Vec2
            return value.copy()
        else:
            raise ep_InvalidParameter, "Expected length-2 list or tuple or b2Vec2 (%s)" % key

    else:
        if isinstance(value, type_):
            return value
        else:
            raise ep_InvalidParameter, "Expected type %s for parameter %s" % (str(type_), key)

class Config (object):
    def __init__(self, **kw):
        '''Configuration class
        Specify the attributes as keywords:

            Config(frequency=60.0)

        Raises ep_InvalidParameter on error.
        ''' 
        # defaults for instance-based properties
        self.worldaabb = box2d.b2AABB()
        self.worldaabb.lowerBound.Set(-100.0, -100.0)
        self.worldaabb.upperBound.Set( 100.0,  100.0)
        self.gravity = box2d.b2Vec2(0.0, -10.0)

        # set the rest from the parameters
        if kw:
            self._set(**kw)

    def __repr__(self):
        pairs = ["%s:%s" % (key, getattr(self, key)) for key in self._options.keys()]
        return "(Config: %s)" % (", ".join(pairs))

    def __getattr__(self, key):
        return self._options[key]['value']

    def __setattr__(self, key, value):
        option = self._options[key]
        option['value'] = _type_check(option['type'], value)

    def _set(self, **kw):
        '''Set some configuration variables.
        
        Specify the attributes as keywords:

            set(frequency=60.0)

        Raises ep_InvalidParameter on error.
        ''' 
        for key in kw.keys():
            value = kw[key]
            if key not in self._options:
                raise ep_InvalidParameter, "Invalid config parameter: %s" % key

            setattr(self, key, value)

            debugstr(2, "Configuration variable %s=%s" % (key, getattr(self, key)))

        global debug_level
        debug_level = self._options['debug_level']['value']

    _options = {
        'frequency'     : { 'value': 60.0, 'type' : (int, float) },
        'renderer'      : { 'value': None, 'type' : Renderer },
        'velocity_iter' : { 'value': 10,   'type' : int },
        'position_iter' : { 'value': 8,    'type' : int },
        'debug_level'   : { 'value': 0,    'type' : int },
        'worldaabb'     : { 'value': None, 'type' : box2d.b2AABB },
        'gravity'       : { 'value': None, 'type' : box2d.b2Vec2 },
        'doSleep'       : { 'value': True, 'type' : bool },
        'debugDraw'     : { 'value': True, 'type' : bool },
    }

_basetypes = {
    'shape' : {
        'create_fcn'       : lambda world, body: body.CreateShape,
        ep_body            : box2d.b2Body,
        ep_density         : ep_number_type,
        ep_filter          : box2d.b2FilterData,
        ep_friction        : ep_number_type,
        ep_isSensor        : bool,
        ep_localPosition   : box2d.b2Vec2,
        ep_restitution     : ep_number_type,
        ep_userData        : ep_userdata_type,
        ep_collisionGroup  : 0 #ep_custom_type(CollisionGroup),
     },
    'joint' : {
        'create_fcn'       : lambda world, body: world.CreateJoint,
        ep_body1           : box2d.b2Body,
        ep_body2           : box2d.b2Body,
        ep_collideConnected: bool,
        ep_userData        : ep_userdata_type,
     },
     'body' : {
        ep_massData        : box2d.b2MassData,
        ep_userData        : ep_userdata_type,
        ep_position        : box2d.b2Vec2,
        ep_angle           : ep_number_type,
        ep_linearDamping   : ep_number_type,
        ep_angularDamping  : ep_number_type,
        ep_allowSleep      : bool,
        ep_isSleeping      : bool,
        ep_fixedRotation   : bool,
        ep_isBullet        : bool,
        ep_collisionGroup  : 0 #ep_custom_type(CollisionGroup),
     },
    }

_creation_info = {
    # shapes
    ep_circle : { 
        'class'     : box2d.b2CircleDef,
        'base'      : _basetypes['shape'],
        ep_radius   : ep_number_type,
     },
    ep_polygon : {
        'class'     : box2d.b2PolygonDef,
        'base'      : _basetypes['shape'],
        ep_vertices : ep_list_type,
     },
    ep_edge    : { 
        'class'    : box2d.b2EdgeChainDef,
        'base'     : _basetypes['shape'],
        ep_vertices: ep_list_type,
        ep_isALoop : bool,
     },

    # joints
    ep_distance : { 
        'class'             : box2d.b2DistanceJointDef,
        'base'              : _basetypes['joint'],
        ep_localAnchor1     : box2d.b2Vec2,
        ep_localAnchor2     : box2d.b2Vec2,
        ep_length           : ep_number_type,
     },
    ep_gear : { 
        'class'             : box2d.b2GearJointDef,
        'base'              : _basetypes['joint'],
        ep_joint1           : box2d.b2Joint,
        ep_joint2           : box2d.b2Joint,
        ep_ratio            : ep_number_type,
     },
    ep_line : { 
        'class'             : box2d.b2LineJointDef,
        'base'              : _basetypes['joint'],
        ep_enableLimit      : bool,
        ep_enableMotor      : bool,
        ep_localAnchor1     : box2d.b2Vec2,
        ep_localAnchor2     : box2d.b2Vec2,
        ep_localAxis1       : box2d.b2Vec2,
        ep_lowerTranslation : ep_number_type,
        ep_maxMotorForce    : ep_number_type,
        ep_motorSpeed       : ep_number_type,
        ep_upperTranslation : ep_number_type,
     },
    ep_mouse : { 
        'class'             : box2d.b2MouseJointDef,
        'base'              : _basetypes['joint'],
        ep_target           : box2d.b2Vec2,
        ep_maxForce         : ep_number_type,
        ep_frequencyHz      : ep_number_type,
        ep_dampingRatio     : ep_number_type,
        ep_timeStep         : ep_number_type,
     },
    ep_prismatic : { 
        'class'             : box2d.b2PrismaticJointDef,
        'base'              : _basetypes['joint'],
        ep_enableLimit      : bool,
        ep_enableMotor      : bool,
        ep_localAnchor1     : box2d.b2Vec2,
        ep_localAnchor2     : box2d.b2Vec2,
        ep_localAxis1       : box2d.b2Vec2,
        ep_lowerTranslation : ep_number_type,
        ep_maxMotorForce    : ep_number_type,
        ep_motorSpeed       : ep_number_type,
        ep_upperTranslation : ep_number_type,
        ep_referenceAngle   : ep_number_type,
     },
    ep_pulley : { 
        'class'             : box2d.b2PulleyJointDef,
        'base'              : _basetypes['joint'],
        ep_groundAnchor1    : box2d.b2Vec2,
        ep_groundAnchor2    : box2d.b2Vec2,
        ep_localAnchor1     : box2d.b2Vec2,
        ep_localAnchor2     : box2d.b2Vec2,
        ep_length1          : ep_number_type,
        ep_maxLength1       : ep_number_type,
        ep_length2          : ep_number_type,
        ep_maxLength2       : ep_number_type,
        ep_ratio            : ep_number_type,
     },
    ep_revolute : { 
        'class'             : box2d.b2RevoluteJointDef,
        'base'              : _basetypes['joint'],
        ep_localAnchor1     : box2d.b2Vec2,
        ep_localAnchor2     : box2d.b2Vec2,
        ep_referenceAngle   : ep_number_type,
        ep_enableLimit      : bool,
        ep_lowerAngle       : ep_number_type,
        ep_upperAngle       : ep_number_type,
        ep_motorSpeed       : ep_number_type,
        ep_maxMotorTorque   : ep_number_type,
      },
}

class World (object):
    config = None
    world  = None

    def __init__(self, **kw):
        '''Initialize the world and set configuration variables.
        
        Specify the attributes as keywords:

          World(frequency=60.0, worldaabb=(-100,-100,100,100), gravity=(0,-10))

        AABB is (lowerX, lowerY, upperX, upperY)
        Unspecified variables default to the settings in the Config class
         (easyPhysics/main.py)

        The Box2D world will not be initialized until .init_world() is called.

        Raises ep_InvalidParameter on error.
        '''

        self.config = Config(**kw)

        global _creation_info
        for type_ in _creation_info.keys():
            data = _creation_info[type_]
            if 'base' in data:
                for basekey in data['base'].keys():
                    data[basekey] = data['base'][basekey]
                del data['base']

        debugstr(1, "Initialized") 
        debugstr(2, self.config) 

    def init_world(self):
        config = self.config
        self.world = box2d.b2World(config.worldaabb, config.gravity, config.doSleep)

    def get_config(self, key):
        '''Get a configuration value
        '''
        return getattr(self.config, key)

    def set_config(self, **kw):
        '''Set some configuration variables.
        
        Specify the attributes as keywords:

            set_config(frequency=60.0)

        Raises ep_InvalidParameter on error.
        ''' 
        self.config._set(**kw)

    def _create_body(self, bodyDef):
        '''Create a body based on a dict definition
        
        Returns: The created world body
        '''

        bd = box2d.b2BodyDef()
        body = self.world.CreateBody(bd)

        if ep_shapes in bodyDef:
            for shapedef in bodyDef[ep_shapes]:
                self._create_generic(shapedef, body)

    def _create_generic(self, defn, shapeBody=None, strictCheck=True):
        '''Create a body, shape, or joint based on a dict definition

        Returns: The created world object
        '''

        if 'type' not in defn: # assume body
            return self._create_body(defn)

        try:        
            type_ = defn[ep_type]
            cinfo = _creation_info[type_]
        except KeyError:
            raise ep_InvalidDefinition, "Requires valid type"

        b2def = cinfo['class']()

        debugstr(2, "Creating: %s (cinfo: %s)" % (_dict_format(defn), _dict_format(cinfo)))
        for key in defn.keys():

            if key not in cinfo:
                if key == ep_type:
                    continue
                if strictCheck:
                    raise ep_InvalidDefinition, "Extraneous entry '%s'. Remove or disable strict checking" % key
                debugstr(2, "Extraneous key '%s' found in definition" % key)
                continue

            setattr(b2def, key, _type_check(cinfo[key], defn[key]))


        create_fcn = cinfo['create_fcn'](self.world, shapeBody)
        return create_fcn(b2def)

    def create(self, objectDef):
        ###Not sure if I like this yet...
        """Create a body/joint/shape

        With a ..........

        If a b2[Body|Joint]Def is passed in, it will be passed
        to box2d and created.

        Raises ep_InvalidParameter if the type of the object cannot be determined.

        Returns: The created object
        """
        shape_defs = (box2d.b2ShapeDef, box2d.b2CircleDef, box2d.b2EdgeChainDef, box2d.b2PolygonDef)
        joint_defs = (box2d.b2DistanceJointDef, box2d.b2GearJointDef, box2d.b2JointDef, 
                      box2d.b2LineJointDef, box2d.b2MouseJointDef, box2d.b2PrismaticJointDef, 
                      box2d.b2PulleyJointDef, box2d.b2RevoluteJointDef)
        body_defs  = (box2d.b2BodyDef, )

        if isinstance(objectDef, body_defs):
            return self.world.CreateBody(objectDef)
        elif isinstance(objectDef, shape_defs):
            raise ep_InvalidParameter, "Shape must be created on a body (body.CreateShape)"
        elif isinstance(objectDef, joint_defs):
            return self.world.CreateJoint(objectDef)
        elif isinstance(objectDef, dict):
            return self._create_generic(objectDef)
        else:
            raise ep_InvalidParameter

    def delete(self, object):
        pass

    def save(self, file, format="xml"): # xml/pickle
        pass

    def load(self, file, format="xml"):
        pass

    def step(self):
        # skip render, pause physics step, ...
        pass

    def get_bodies(self):
        for i in []:
            yield i 

    def get_shapes(self, body):
        for i in []:
            yield i 

    def get_all_shapes(self):
        for i in []:
            yield i 

    def pick(self, pos):
        pass

