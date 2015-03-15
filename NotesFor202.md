### Manual / Getting Started ###

After installing pybox2d, if you want to know where to begin, see the python [manual](http://pybox2d.googlecode.com/svn/branches/box2d_2.0/doc/manual.htm).

**Please note** that this wiki was converted from an old copy of the defunct official box2d wiki. There may be some inconsistencies.


### Source Code Examples ###

  * A port of the Box2D Hello World: [hello.py](http://code.google.com/p/pybox2d/source/browse/branches/box2d_2.0/testbed/hello.py)
  * The Box2D testbed ported to Python ([browse](http://code.google.com/p/pybox2d/source/browse/branches/box2d_2.0/testbed/))
  * Other projects linked from the pybox2d wiki page, [Projects](http://code.google.com/p/pybox2d/wiki/Projects)

### Usage ###

#### 2.0.2b2 Notes ####
  * This version fixes a major memory leak.
  * 2.0.2 is an old version which is not often updated. Please try to move to the SVN 2.1.x version.
  * The inconvenient getAsType() is no longer necessary from 2.0.2b2 and on.
  * The vertexCount parameter has been removed in DrawSolidPolygon and DrawPolygon of b2DebugDraw (you will get a "Swig director method error" if you don't change it)
```
TypeError: "DrawSolidPolygon() takes exactly 4 arguments (3 given) Swig director method error Error detected when calling 'b2DebugDraw.DrawSolidPolygon'"
```

#### b2Vec2 ####

As of pybox2d 2.0.2b1, tuples and lists can now be used in place of b2Vec2.

Previously, such code would have been necessary (body is a b2Body):

```
pos = body.GetPosition() + box2d.b2Vec2(1.0, 0.0)
```

Now you are free to use:

```
pos = body.position + (1.0, 0.0)
```

This also goes for setting values. These are all equivalent:

```
groundBodyDef.position = [0, -10]
groundBodyDef.position = (0, -10)
groundBodyDef.position = box2d.b2Vec2(0, -10)
groundBodyDef.position.Set(0, -10)
```

Note that you cannot just make a tuple and expect it to behave as a b2Vec2. This works because the above properties/methods return b2Vec2. Should you want to use a vector for something else, first you would need to define one:

```
myvec = box2d.b2Vec2(0,5) # myvec = (0,5)
myvec *= 3 # myvec = (0,15)
myvec += (1,1) # myvec = (1,16)
```

#### Callbacks ####

```
class myContactListener(b2ContactListener):
    def __init__(self): super(myContactListener, self).__init__() 
    def Add(self, point):
        """Called when a contact point is created"""
        print "Add:", point
    def Persist(self, point):
        """Called when a contact point persists for more than a time step"""
        print "Persist:", point
    def Remove(self, point):
        """Called when a contact point is removed"""
        print "Remove:",point
```

Setting it (where self.world is a b2World):

```
self.myListener = myContactListener()
self.world.SetContactListener( self.myListener )
```

You should buffer your contact points and then deal with them once the Step is over with, as bodies/etc are locked during a physics step.

#### b2DebugDraw Callbacks ####

```
class myDebugDraw(b2DebugDraw):
    def __init__(self): super(myDebugDraw, self).__init__()
    def DrawCircle(self, center, radius, color):
        pass
    def DrawSegment(self, p1, p2, color):
        pass
    def DrawXForm(self, xf):
        pass
    def DrawSolidCircle(self, center, radius, axis, color):
        pass
    def DrawPolygon(self, vertices, vertexCount, color):
        pass
    def DrawSolidPolygon(self, vertices, vertexCount, color):
        print "DrawSolidPolygon [Vertices: %s Count: %d Color: (%f, %f, %f)]" % (vertices, vertexCount, color.r, color.g, color.b)
```

You'll notice that 'vertices' is now a list of vertexCount tuples in the format ( (x, y), (x, y) ... (x, y) ). Sample output:

```
DrawSolidPolygon [Vertices: ((9.5, 10.0), (10.5, 10.0), (10.5, 11.0), (9.5, 11.0)) Count: 4 Color: (0.9, 0.9, 0.9)]

```

Setting it:

```
self.myDraw = myDebugDraw()
self.myDraw.SetFlags(self.myDraw.e_shapeBit) # and whatever else you want it to draw 
self.world.SetDebugDraw( self.myDraw )
```

See the testbed for pygame and pyglet examples.

#### b2World.Query() ####

The usage of this function differs from the standard Box2D API. Usage:

```
number_of_shapes, shapes = world.Query(AABB, max_shapes_to_return)
```

Where the return value is a tuple indicating the number of shapes that match the query (number\_of\_shapes) and a list of those objects (shapes).

#### TestSegment ####

```
hit, lambda_, normal_tuple = TestSegment(xform, segment, fMaxLambda)
```

#### Raycasts (Raycast/RaycastOne) ####

One single RayCast:

```
lambda_, normal, shape = world.RaycastOne(segment, bSolidShapes, userData)
```

Multiple RayCasts:

```
number_of_shapes, shapes = world.Raycast(segment, maxcount, bSolidShapes, userData)
```

The userData most likely should be passed in as None, otherwise the raycasts might fail. Read the documentation (the C++ header file, as it's undocumented as of yet) for further information.

See [test\_RayCast.py](http://code.google.com/p/pybox2d/source/browse/branches/box2d_2.0/testbed/test_RaycastTest.py) or [test\_BoxCutter.py](http://code.google.com/p/pybox2d/source/browse/branches/box2d_2.0/testbed/test_BoxCutter.py) for more examples.

#### b2Joint? b2Shape? ####

If you by chance get a return value of a b2Joint or a b2Shape, and you want to get the appropriate shape, you need to do:

```
jd=box2d.b2RevoluteJointDef()
jd.Initialize(ground, gearw, gearw.GetWorldCenter())
revolutejoint = self.world.CreateJoint(jd).getAsType()
```

The 'revolutejoint' variable would then hold a b2RevoluteJoint. Without using .getAsType(), it would be a b2Joint. b2Shapes can similarly be retrieved.

NOTE getAsType() is no longer necessary from 2.0.2b2 and on.

### Crashes ###

#### Working with userData ####

**This has been FIXED in pybox2d 2.0.2b1**

A bug that has caught me a few times is the fact that unless ALL objects have userData, you can't loop through every body in the world and check them. It will cause a segfault. So, how do you set the ground's userData, then?

Easily enough:

```
world.GetGroundBody().SetUserData(["ground"])
```

Assuming you set the bodyDef.userData for the rest of your objects, you can now check the userData of any object, easily:

```
def get_bodies(world):
    body = world.GetBodyList()
    while body:
        yield body
        body = body.GetNext()

for body in get_bodies(world):
    print body.GetUserData()
```

#### Working with DebugDraw ####

**This has been FIXED in pybox2d 2.0.2b1**

Some of the most frustrating crashes can come from errors in your code while in a Box2D callback. For example, if you have any code that raises an exception in your b2DebugDraw class, it will fail and cause the whole application to crash.

To debug them, as far as I know, it's either necessary to wrap your code in try/except blocks to see where the exceptions are being thrown, or to move your code out of the callback class and try it on its own.

#### Multiple Source Files ####

So, you have your game split into several Python files. You want to access Box2D functions in each of them. You'd think you could just 'import Box2D2' as necessary in each of your files, but unfortunately that's not the case, due to some complications with SWIG. One file's definition of b2Vec2 will be of a different type than another file's, leading to TypeErrors and SWIG errors indicating invalid calls to overloaded functions.

**Work-around**

Designate one of your files to be your 'main' one.

  * game\_main.py

```
import Box2D2 as box2d
```

  * From all your other source files that need access to Box2D, do this:

```
from game_main import box2d
```

An easy enough fix, but perhaps not so obvious.

If it's safe you can also do a 'from game\_main import `*`', which should import everything properly.

#### Internal Call Backs (listeners/filters) ####

**This has been FIXED in pybox2d 2.0.2b1**

Any uncaught exception inside of a listener or filter callback function will always become a SWIG exception and cause a crash. This makes debugging code inside of these calls difficult, and code here should be carefully syntax checked prior to execution.

The issue here becomes apparent in collision listeners because improperly copying/accessing the b2ContactResult structure can raise the same exception. It is strongly recommended that when building your own container for the data in b2ContactResult that you test this code independently of any other code in the listener.

Note that bodies are still LOCKED during callbacks, even in Python. This means that if you want to destroy bodies, you have to wait until after Step() has been evaluated. Store your bodies to be removed in a separate list, then destroy them afterward.

### Bugs ###

See the pybox2d issues list [here](http://code.google.com/p/pybox2d/issues/list)