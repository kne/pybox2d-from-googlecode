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

%pythoncode %{
class b2PickleError (Exception): pass

def _pickle_fix_value_load(lists, value):
    """
    From a dictionary, makes a b2Body, b2Shape, b2Joint, b2Controller
    """
    bodyList, jointList, controllerList=lists
    
    if not isinstance(value, dict):
        return value

    if 'pickle_type' not in value:
        return value

    if value['pickle_type']=='b2Body':
        return bodyList[ value['body'] ]
    elif value['pickle_type']=='b2Shape':
        body  = bodyList[ value['body'] ]
        shape = body.shapeList[ value['shape'] ]
        return shape
    elif value['pickle_type']=='b2Joint':
        return jointList[ value['joint'] ]
    elif value['pickle_type']=='b2Controller':
        return controllerList[ value['controller'] ]

    return value

def _pickle_fix_value_save(lists, value):
    """
    Fixes: b2Body, b2Shape, b2Joint, b2Controller

    In place of an unpicklable b2Body outside of a world, use a dictionary with
    an index to the appropriate place in the world.
    """
    bodyList, jointList, controllerList=lists

    if isinstance(value, b2Body):
        value = { 'pickle_type' : 'b2Body', 'body' : bodyList.index(value) }
    elif isinstance(value, b2Shape):
        body = value.GetBody()
        shapeID = body.shapeList.index(value)
        value = { 'pickle_type' : 'b2Shape', 'body': bodyList.index(body), 'shape' : shapeID}
    elif isinstance(value, b2Joint):
        value = { 'pickle_type' : 'b2Joint',  'joint': jointList.index(value) }
    elif isinstance(value, b2Controller):
        value = { 'pickle_type' : 'b2Controller', 'controller' : controllerList.index(value)}
    return value

def pickle_fix(world, var, func='save', lists=None):
    """
    Fix variables so that they may be pickled (or loaded from a pickled state).
    You cannot save a b2Body by itself, but if passed in with the world, it's possible
    to pickle it.

    So, be sure to use this on your box2d-related variables before and after pickling.

    e.g.,
    + Save:
      my_pickled_vars = box2d.pickle_fix(myworld, my_vars, 'save')
      pickle.dump([myworld, my_pickled_vars], open(fn, 'wb'))

    + Load
      world, my_pickled_vars = pickle.load(open(fn, 'rb'))
      myworld = world._pickle_finalize()
      my_vars=box2d.pickle_fix(myworld, my_pickled_vars, 'load')

    For an actual implementation of pickling, see the testbed (main test and test_pickle).
    """
    if func=='save':
        fix_function=_pickle_fix_value_save
    elif func=='load':
        fix_function=_pickle_fix_value_load
    else:
        raise ValueError, 'Expected func in ("save", "load")'

    if not lists:
        # these lists are all created dynamically, so do this once
        lists=[world.bodyList, world.jointList, world.controllerList]

    if isinstance(var, (list, tuple)):
        # Create a new list/tuple and fix each item
        new_list=[pickle_fix(world, value, func, lists) for value in var]
        if isinstance(var, tuple):
            # If it was originally a tuple, make this new list a tuple
            new_list=tuple(new_list)
        return new_list
    elif isinstance(var, dict):
        if func=='load' and 'pickle_type' in var:
            return fix_function(lists, var)

        # Create a new dictionary and fix each item
        new_dict={}
        for var, value in var.items():
            new_dict[var]=pickle_fix(world, value, func, lists)
        return new_dict
    else:
        # Not a dictionary/list, so it is probably just a normal value. 
        # Fix and return it.
        ret= fix_function(lists, var)
        return ret

# -- unpicklable object --
def no_pickle(self):
    raise b2PickleError, 'Cannot pickle this object. Pickle the typecasted object: object.getAsType()'

# -- generic get and set state --
def _generic_setstate(self, dict):
    self.__init__()
    for key, value in dict.iteritems():
        setattr(self, key, value)

def _generic_getstate(self, additional_ignore=[]):
    ignore_properties = ['thisown', 'this', 'next', 'prev', 
                         'world', 'coreVertices', 'normals']
    if additional_ignore:
        ignore_properties += additional_ignore

    vars = [v for v in dir(self.__class__) 
        if isinstance(getattr(self.__class__, v), property) 
            and v not in ignore_properties]
    return dict((var, getattr(self, var)) for var in vars)

# -- factory output -- (i.e., b2Body, 
def _pickle_factory_set(self, data):
    # the factory output cannot be created just yet,
    # so store the necessary information to create it later
    self.__pickle_data__ = data

# -- factory output finalizing (loading)
def _pickle_finalize(self, world=None, body=None):
    if not hasattr(self, '__pickle_data__'):
        raise b2PickleError
    
    #print '-> finalizing', type(self)

    pairs = [ (lambda w,b,v: w.CreateBody(v) , b2Body        , b2BodyDef),
              (lambda w,b,v: b.CreateShape(v), b2PolygonShape, b2PolygonDef),
              (lambda w,b,v: b.CreateShape(v), b2CircleShape , b2CircleDef),
              (lambda w,b,v: b.CreateShape(v), b2EdgeChainDef, b2EdgeChainDef),
            ]
    
    data = self.__pickle_data__
    createfcn = None

    for fcn, output, input in pairs:
        if isinstance(self, output):
            self = input()
            createfcn=fcn
            break

    if not createfcn:
        raise b2PickleError # I do not know quite what happened

    do_after_classes=(b2Body, b2Shape, list)
    do_after_props  =['linearVelocity', 'angularVelocity', 'isSleeping']
    finalize_after = []
    
    if isinstance(self, (b2PolygonDef, b2EdgeChainDef)):
        #print '* polygon/edge shape detected. setting vertices.'
        self.vertices = data['vertices']
        del data['vertices']

    for var in data:
        value = data[var]
        if isinstance(value, do_after_classes) or var in do_after_props:
            finalize_after.append( (var, value) )
        elif hasattr(self, var):
            #print 'setting %s=%s' % (var,value)
            setattr(self, var, value)

    #print '* creating'
    self = createfcn(world, body, self)

    if isinstance(self, b2World):
        world=self
    elif isinstance(self, b2Body):
        body = self

    #print '* finalize after...'
    for var, value in finalize_after:
        if var == 'shapeList':
            _pickle_finalize_shapelist(world, body, value)
        elif var == 'isSleeping':
            if value:
                self.PutToSleep()
            else:
                self.WakeUp()
        elif hasattr(self, var):
            if hasattr(value, '_pickle_finalize'):
                value=_pickle_finalize(value,world,body)
            setattr(self, var, value)
        #else:
        #    print 'Unknown:', var
    #print '* done'
    return self

# -- custom handlers --
def _pickle_finalize_controller(data, world):
    #print 'finalize controller'
    defn = globals()["b2%sControllerDef" % data['_type']] ()

    bodyList  = world.bodyList
    for var in data:
        value = data[var]
        if hasattr(defn, var):
            #print 'setting %s=%s' % (var,value)
            setattr(defn, var, value)
        else:
            #print 'not found', var
            pass

    #print '* creating controller'
    controller = world.CreateController(defn)
    #print '* created; adding bodies...'

    for body in data['bodyList']:
        try:
            real_body = bodyList[ int(body) ]
        except:
            raise b2PickleError, 'World not initialized properly; unable to create controller'
        controller.AddBody(real_body)

    return controller

def _pickle_finalize_joint(data, world):
    #print 'finalize joint'
    defn = globals()["b2%sJointDef" % data['_type']] ()

    body_names = ['body1', 'body2']
    joint_names = ['joint1', 'joint2']

    bodyList  = world.bodyList
    jointList = world.jointList
    for var in data:
        value = data[var]
        if var=='localXAxis1': var = 'localAxis1' # single rename necessary
        if hasattr(defn, var):
            if var in body_names:
                try:
                    value = bodyList[ int(value) ]
                except:
                    raise b2PickleError, 'World not initialized properly; unable to create joint'
            elif var in joint_names:
                # it seemed like this might cause a problem, but in reality it should not.
                # the joints linked by this have to have been created already, so their index
                # should be available already.
                try:
                    value = jointList[ int(value) ]
                except:
                    raise b2PickleError, 'World not initialized properly; unable to create joint'
            #print 'setting %s=%s' % (var,value)
            setattr(defn, var, value)
        else:
            #print 'not found', var
            pass

    #print '* creating joint'
    return world.CreateJoint(defn)

def _pickle_finalize_shapelist(world, body, shapelist):
    # auto added to the shapelist as the shapes are created
    for s in shapelist:
        if isinstance(s, dict):
            # special case, an edge shape
            temp=b2EdgeChainDef()
            temp.__pickle_data__=s
            _pickle_finalize(temp, world, body)
        else:
            s._pickle_finalize(world, body)

def _pickle_finalize_world(self):
    #print '-> finalizing world'
    if not hasattr(self, '__pickle_data__'):
        raise b2PickleError

    data = self.__pickle_data__
    
    #print 'Creating world...'
    world = b2World(data['worldAABB'], data['gravity'], data['doSleep'])

    #print "finalizing ground body"
    gb_data = data['groundBody'].__pickle_data__

    _pickle_finalize_shapelist(world, world.groundBody, gb_data['shapeList'])

    for var in gb_data.keys():
        value = gb_data[var]
        if isinstance(value, (b2Shape)) or var=='shapeList':
            pass
        elif hasattr(world.groundBody, var):
            try:
                setattr(world.groundBody, var, value)
            except AttributeError:
                pass

    #print 'Finalizing bodies...'
    for body in data['bodyList']:
        body._pickle_finalize(world)

    for joint in data['jointList']:
        _pickle_finalize_joint(joint, world)

    for controller in data['controllerList']:
        _pickle_finalize_controller(controller, world)

    return world

def _pickle_body_getstate(self):
    # everything is generic_getstate except for edge shape handling.

    def get_edge_vertices_and_shapes(shape):
        """
        returns is_loop, shapes, vertices
        """
        vertices = []
        shapes   = []
        edge     = shape
        while edge:
            shapes.append(edge)
            vertices.append( edge.vertex1 )
            last=edge.vertex2
            edge=edge.next
            if edge==shape: # a loop
                return True, shapes, vertices
        # not a loop
        vertices.append( last )
        return False, shapes, vertices
        
    ret = _generic_getstate(self, ['shapeList'])
    
    ret['shapeList']=[]
    handled_edges = []
    for shape in self.shapeList:
        if isinstance(shape, b2EdgeShape):
            if shape in handled_edges:
                #print 'found already handled edge; continuing'
                continue
            is_loop, shapes, vertices=get_edge_vertices_and_shapes(shape)
            handled_edges.extend(shapes)
            shape_info = _generic_getstate(shape, ['vertices','length','coreVertex1','coreVertex2'])
            shape_info['isALoop'] =is_loop
            shape_info['vertices']=vertices
            ret['shapeList'].append(shape_info)
        else:
            ret['shapeList'].append(shape)
    return ret

def _pickle_get_b2world(self):
    vars = ['worldAABB', 'gravity', 'doSleep', 'groundBody']
    data=dict((var, getattr(self, var)) for var in vars)

    data['bodyList']=self.bodyList[1:] # remove the ground body

    jointList = []
    for joint in self.jointList:
        joint=joint.getAsType()
        jointList.append( joint.__getstate__(self) )
    data['jointList']=jointList

    controllerList = []
    for controller in self.controllerList:
        controller=controller.getAsType()
        controllerList.append( controller.__getstate__(self) )
    data['controllerList']=controllerList

    return data

def _pickle_get_controller(self, world=None):
    if not world:
        raise b2PickleError, "Controllers can't be saved without the world itself"

    ignore_prop =['thisown', 'this', 'bodyList']
    defn = globals()[ "%sDef" % self.__class__.__name__ ]
    vars = [v for v in dir(defn) 
        if isinstance(getattr(defn, v), property) 
            and v not in ignore_prop]

    ret=dict((var, getattr(self, var)) for var in vars)
    ret['_type'] = self.typeName()

    main_bodyList = world.bodyList
    ctrl_bodyList = self.bodyList
    ret['bodyList']=[main_bodyList.index(body) for body in ctrl_bodyList]
    return ret

def _pickle_get_joint(self, world=None):
    if not world:
        raise b2PickleError, "Joints can't be saved without the world itself"

    ignore_prop =['thisown', 'this', 'world', 'type']
    defn = globals()[ "%sDef" % self.__class__.__name__ ]
    vars = [v for v in dir(defn) 
        if isinstance(getattr(defn, v), property) 
            and v not in ignore_prop]

    if 'localAxis1' in vars:
        # prismatic, rename:
        #    (defn)       (joint)
        #    localAxis1 = localXAxis1;
        # line, rename:
        #    (defn)       (joint)  
        #    localAxis1 = localXAxis1;
        vars.remove('localAxis1')
        vars.append('localXAxis1')

    ret=dict((var, getattr(self, var)) for var in vars)
    ret['_type'] = self.typeName()

    bodyList = world.bodyList
    jointList= world.jointList
    for key, value in ret.iteritems():
        if isinstance(value, b2Body):
            ret[key]=bodyList.index(value)
        elif isinstance(value, b2Joint):
            ret[key]=jointList.index(value)

    return ret

%}

# These were originally set programmatically, which is perhaps cleaner,
# but this will set every class up properly without any unnecessary code
# execution

%extend b2World {
 %pythoncode %{
  __getstate__=_pickle_get_b2world
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_world
 %}
}
            

%extend b2PrismaticJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2ContactID {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ShapeDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2GravityController {
 %pythoncode %{
  __getstate__=_pickle_get_controller
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_controller
 %}
}
            

%extend b2LineJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Body {
 %pythoncode %{
  __getstate__=_pickle_body_getstate
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize
 %}
}
            

%extend b2TensorDampingController {
 %pythoncode %{
  __getstate__=_pickle_get_controller
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_controller
 %}
}
            

%extend b2ManifoldPoint {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Color {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2BodyDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Version {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Joint {
 %pythoncode %{
  __getstate__=no_pickle
  __setstate__=_generic_setstate
 %}
}
            

%extend b2JointEdge {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactListener {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2StackEntry {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactManager {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Bound {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Segment {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2DebugDraw {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ConstantForceControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Pair {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2RevoluteJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2BuoyancyController {
 %pythoncode %{
  __getstate__=_pickle_get_controller
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_controller
 %}
}
            

%extend b2EdgeShape {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize
 %}
}
            

%extend b2PolygonDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2XForm {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2DistanceJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2Contact {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2EdgeChainDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Vec2 {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Vec3 {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2BoundaryListener {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2GravityControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactFilter {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ConstantForceController {
 %pythoncode %{
  __getstate__=_pickle_get_controller
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_controller
 %}
}
            

%extend b2PairCallback {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ConstantAccelControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2MassData {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2BuoyancyControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2AABB {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Mat22 {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactID_features {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactRegister {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Sweep {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Controller {
 %pythoncode %{
  __getstate__=no_pickle
  __setstate__=_generic_setstate
 %}
}
            

%extend b2PulleyJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2BufferedPair {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2JointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2DestructionListener {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2CircleDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ControllerEdge {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2PolygonShape {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize
 %}
}
            

%extend b2Manifold {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2GearJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2BlockAllocator {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2FilterData {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2RevoluteJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2MouseJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2TensorDampingControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Mat33 {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactPoint {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2OBB {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ControllerDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2TimeStep {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2PairManager {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2PulleyJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactEdge {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2DistanceJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ContactResult {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2ConstantAccelController {
 %pythoncode %{
  __getstate__=_pickle_get_controller
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_controller
 %}
}
            

%extend b2StackAllocator {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2MouseJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2Proxy {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2BroadPhase {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2PrismaticJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2CircleShape {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize
 %}
}
            

%extend b2LineJoint {
 %pythoncode %{
  __getstate__=_pickle_get_joint
  __setstate__=_pickle_factory_set
  _pickle_finalize=_pickle_finalize_joint
 %}
}
            

%extend b2GearJointDef {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Jacobian {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2NullContact {
 %pythoncode %{
  __getstate__=_generic_getstate
  __setstate__=_generic_setstate
 %}
}
            

%extend b2Shape {
 %pythoncode %{
  __getstate__=no_pickle
  __setstate__=_generic_setstate
 %}
}
            

