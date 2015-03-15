## Manual ##

The original Box2D manual has been partially rewritten for Python. [2.0.x](http://pybox2d.googlecode.com/svn/branches/box2d_2.0/doc/manual.htm) manual / [2.1](GettingStartedManual.md) manual

Basic API documentation is available thanks to epydoc, for [2.0.2](http://pybox2d.googlecode.com/svn/branches/box2d_2.0/doc/epydoc/html/index.html) and for [2.1](http://pybox2d.googlecode.com/svn/doc/epydoc/index.html).

Though the 2.1 version has been improved in terms of user-friendliness, neither will be useful unless you know what you're looking for. The [testbed](http://code.google.com/p/pybox2d/source/browse/#svn%2Ftrunk%2Fexamples) examples are your best bet at seeing how to implement things.

## Version Numbers ##

The version numbers follow the main Box2D releases with a release number attached. For example, 2.0.1b3 is based on Box2D release 2.0.1 and is the third release of the bindings.

Starting Box2D 2.0.2b1, the version number of the source code is available in Box2D:
```
import Box2D
Box2D.__version__      # '2.0.2b1'
Box2D.__version_info__ # (2,0,2,1)
```

## Acknowledgements ##

  * Thanks to all of those who have reported bugs or submitted patches.
  * Special thanks go to giorgosg, for contributing the 2.0.2 Cairo backend, the Gish Tribute testbed example, and other things.
  * Thanks, santagada, for getting command-line arguments in the testbed.
  * And, of course, to Erin Catto for Box2D itself.

## Changes ##

### 2.0.2b1 (2/25/2009) ###
Since 2.0.2b0, there have been a good deal of changes to pybox2d:

  * Code structure completely reorganized
  * Doxygen comments converted to docstrings (should be a bit more friendly now, but still a bit C++'ish in places)
  * Lists and tuples may be used anywhere in place of b2Vec2's, and all of the tests have been updated to reflect this
  * Save/load state (pickling support for worlds)
  * Bug fix: Seg faults during `DebugDraw`/etc callbacks
  * Bug fix: userData reference counting causing leaks
  * Bug fix: getType() didn't work on line joints
  * Bug fix: `TestSegment` now returns from (-1,0,1) and not a bool
  * b2PolygonDef.setVertices() added, supports either b2Vec2 or list/tuple, so no need to specify. Old setVertices\_tuple/b2Vec2() are deprecated.
  * New pretty printing style. It takes up a good deal of space, but it's actually readable.
  * New examples: <a href='http://code.google.com/p/pybox2d/source/browse/trunk/testbed/test_BezierEdges.py'>bezier edges</a> with thin line segments, a simple <a href='http://code.google.com/p/pybox2d/source/browse/trunk/testbed/test_Belt.py'>belt</a>, basic <a href='http://code.google.com/p/pybox2d/source/browse/trunk/testbed/test_pickle.py'>pickling</a> example (might needs some updating)
  * (Optionally compilable) C++ assertion failures turned into Python exceptions<br>Additional properties and accessors to make coding easier (see below)<br>
<ul><li>Many tests were updated and rewritten to be cleaner<br>
</li><li>Added b2CheckPolygonDef and deprecated the Python ported version. This version adds (optional) additional checks to ensure that your shape is convex and properly sized to not have strange results<br>
</li><li>Added <code>GetVertices</code>() for b2EdgeShapes. Creating one b2ChainDef results in many b2EdgeShapes, so this properly loops through each connected shape and gets the vertices in order<br>
</li><li>Box2D source updated, b2GravityController fixed<br>
</li><li>A fix for not allowing b2Body/Joint/Controller/Shapes as dictionary keys. Don't know how I missed this one. Still won't be picklable unfortunately.<br>
</li><li>Basic iterators have been added: b2World (iterates over bodies), b2Body (iterates over shapes), b2Controller (iterates over bodies), b2PolygonShape (iterates over vertices)</li></ul>

There are several code-breaking features that you might run into:<br>
<ul><li>The library is now called <b><code>Box2D</code></b> (and not the cumbersome <code>Box2D2</code>)<br>
</li><li>Controllers now follow the factory style (see the <a href='http://code.google.com/p/pybox2d/source/browse/branches/new_setup/testbed/test_Buoyancy.py'>buoyancy</a> test for more information)<br>
</li><li>b2Distance updated (see <a href='http://code.google.com/p/pybox2d/source/detail?r=137'>here</a> if this affects you)<br>
</li><li>b2Body.<code>GetShapeList</code>() used to return only first shape, now returns actual list<br>
</li><li>b2World.<code>GetBodyList</code>/<code>Joint</code>() used to return only first body, now returns actual list<br>
</li><li>All occurences of the ugly '<code>m_*</code>' have been removed. This might require some changes in your code, since this applies to all b2Joint.<code>m_*</code> and others, not just testbed stuff.</li></ul>

The following are the additional properties added. Most are just for convenience and make the definition (e.g., b2ShapeDef) symmetric with the output (e.g., b2Shape). Ones in bold are changeable; the rest are read-only:<br>
<table><tbody><tr><td>b2World</td><td><b>gravity</b>, jointList, bodyList, groundBody, worldAABB, doSleep</td></tr><tr><td>b2Shape</td><td><b>filter</b>, <b>friction</b>, <b>restitution</b>, <b>density</b></td></tr><tr><td>b2Joint</td><td>type, userData, body1, body2, collideConnected</td></tr><tr><td>b2CircleShape </td><td>radius, localPosition</td></tr><tr><td>b2PolygonShape</td><td>vertices, coreVertices, normals</td></tr><tr><td>b2Body</td><td> <b>massData</b>, <b>position</b>, <b>angle</b>, linearDamping, angularDamping, <b>allowSleep</b>, isSleeping, <code>IsRotationFixed</code>, <b>isBullet</b>, <b>angularVelocity</b>, <b>linearVelocity</b>, shapeList</td></tr></tbody></table>

(later SVN versions add support for changing damping, fixedRotation, and shape isSensor)<br>
<br>
Basic epydoc documentation is now available <a href='http://pybox2d.googlecode.com/svn/epydoc/html/index.html'>here</a>. The testbed is no longer included in the installer, so please download it separately <a href='http://pybox2d.googlecode.com/files/pybox2d-testbed-2.0.2b1.zip'>here</a>.<br>
<br>
<br>
<h3>2.0.2b0 (10/23/2008)</h3>

First release that's not based on a major Box2D release. It combines Box2D SVN <a href='https://code.google.com/p/pybox2d/source/detail?r=177'>r177</a> and contributions from shaktool (thin line segment) and BorisTheBrave (controllers/buoyancy).<br>
<br>
<ul><li>Thin line segment support (forum <a href='http://www.box2d.org/forum/viewtopic.php?f=3&t=1577'>post</a>)<br>
</li><li>Buoyancy with generic controller support (forum <a href='http://www.box2d.org/forum/viewtopic.php?f=3&t=1664'>post</a>)<br>
</li><li>Pyglet 1.1 testbed (still has some issues. run convert-from-pygame.py to convert the tests from pygame)<br>
</li><li>OS X <a href='Installer.md'>Installer</a>
</li><li>Python 2.6 support<br>
</li><li>Line joints (see LineJoint test)<br>
</li><li>Raycasts (see RayCast test and BoxCutter test)<br>
</li><li>TestSegment support<br>
</li><li>BreakableBody test (forum <a href='http://www.box2d.org/forum/viewtopic.php?f=3&t=836'>post</a>)<br>
</li><li>Fixed: == was working, but != comparisons weren't.<br>
</li><li>Access to polygon normals, core vertices, etc.<br>
</li><li>cvar list fixed<br>
</li><li>Off by one bug fixed for vertices</li></ul>

New time step will require a few minor updates to your code:<br>
<br>
Old:<br>
<pre><code>world.Step(timeStep, iterationCount)<br>
</code></pre>

New:<br>
<pre><code>world.Step(timeStep, velocityIterations, positionIterations)<br>
</code></pre>
velocityIterations is usually 10, and positionIterations is usually 8.<br>
<br>
<h3>2.0.1b4 (6/1/2008)</h3>

<ul><li>Supports comparing shapes, joints, bodies. Doesn't require using userData anymore.<br>
</li><li>Major clean ups with Box2D.i<br>
</li><li>Added some docstrings to Box2D.i functions<br>
</li><li>Added b2PolygonDef.checkValues(): checks the Polygon definition to see if upon creation it will cause an assertion to fail (raises ValueError)<br>
</li><li>Wrapped shape.GetCoreVertices() like GetVertices() (for test<i>TimeOfImpact)<br>
</li><li>test_Web fixed<br>
</li><li>All stuff prettily printed by a semi-automated process now<br>
</li><li>Updated test_Bridge.py to SVN rev 156<br>
</li><li>Added many comments to test_main</li></ul></i>

<h3>2.0.1b3 (5/7/2008)</h3>

<ul><li>Updated the interface to allow SetUserData() (absolutely necessary for setting the ground's userdata)<br>
</li><li>Fixed b2PolygonShape (.vertexCount is now private, so the accessor is used instead)<br>
</li><li>Release for Python 2.4<br>
</li><li>Linux (possibly OS X) support with setup.py