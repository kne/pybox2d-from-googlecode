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

/*
* This is the main Python SWIG interface file.
*/

%module(directors="1") Box2D
%{
    #define USE_EXCEPTIONS 1
    #include "Box2D/Box2D.h"
//    float32 b2LineJoint::GetMaxMotorForce() const { return 0.0f; }
//       wrote my own function body for this, but hopefully itll be fixed in svn soon
%}

/*note:
  swig generated names: _Box2D.<class>_<name>
  python obfuscated names: __<class>_<name> 
*/

#ifdef SWIGPYTHON
    #ifdef USE_EXCEPTIONS
        // See Common/b2Settings.h also
        %include "exception.i"

        %exception {
            try {
                $action
            } catch(b2AssertException) {
                // error already set, pass it on to python
            }
        }
    #endif

    #pragma SWIG nowarn=314

    /* ---- classes to ignore ---- */
    //Most of these are just internal structures, so there is no need to have them
    // accessible by Python. You can safely comment out any %ignore if you for some reason
    // do need them. Shrinks the library by a bit, also.
    %ignore b2BroadPhase;
    %ignore b2ContactManager;
    %ignore b2Chunk;
    %ignore b2DynamicTree;
    %ignore b2DynamicTreeNode;
    %ignore b2Island;
    %ignore b2Position;
    %ignore b2Velocity;
    %ignore b2TimeStep;
    %ignore b2Simplex;
    %ignore b2SimplexVertex;
    %ignore b2SimplexCache;
    %ignore b2StackAllocator;
    %ignore b2StackEntry;

    /* ---- features ---- */
    /* Autodoc puts the basic docstrings for each function */
    %feature("autodoc", "1");

    /* Add callback support for the following classes: */
    %feature("director") b2ContactListener;
    %feature("director") b2ContactFilter;
    %feature("director") b2DestructionListener;
    %feature("director") b2DebugDraw;

    /* Director-exceptions are a result of callbacks that happen as a result to
       the physics step, usually. So, catch those errors and report them back to Python. */
    %exception b2World::Step {
        try { $action }
        catch (Swig::DirectorException) { SWIG_fail; }
    }

    /* ---- includes ---- */
    // The order of these is important. 
    %include "Box2D/Box2D_doxygen.i"
    %include "Box2D/Box2D_printing.i"
    %include "Box2D/Box2D_inline.i"
    %include "Box2D/Box2D_vectors.i"
    %include "Box2D/Box2D_typemaps.i"
    %include "Box2D/Box2D_userdata.i"
    %include "Box2D/Box2D_world.i"
    %include "Box2D/Box2D_bodyfixture.i"
    %include "Box2D/Box2D_shapes.i"
    %include "Box2D/Box2D_joints.i"

    /* ---- miscellaneous classes ---- */
    /**** Color ****/
    %extend b2Color {
    public:
        %pythoncode %{
        __iter__ = lambda self: iter((self.r, self.g, self.b)) 
         %}
    }

    /**** Contact ****/
    %extend b2Contact {
    public:
        %pythoncode %{
            # Read-write properties
            sensor = property(__IsSensor, __SetSensor)
            enabled = property(__IsEnabled, __SetEnabled)

            # Read-only
            next = property(__GetNext, None)
            touching = property(__IsTouching, None)
            fixtureB = property(__GetFixtureB, None)
            fixtureA = property(__GetFixtureA, None)
            continuous = property(__IsContinuous, None)
            manifold = property(__GetManifold, None)

        %}
    }

    %rename(__GetNext) b2Contact::GetNext;
    %rename(__IsTouching) b2Contact::IsTouching;
    %rename(__IsSensor) b2Contact::IsSensor;
    %rename(__GetFixtureB) b2Contact::GetFixtureB;
    %rename(__GetFixtureA) b2Contact::GetFixtureA;
    %rename(__IsContinuous) b2Contact::IsContinuous;
    %rename(__GetManifold) b2Contact::GetManifold;
    %rename(__IsEnabled) b2Contact::IsEnabled;
    %rename(__SetEnabled) b2Contact::SetEnabled;
    %rename(__SetSensor) b2Contact::SetSensor;

#endif

%include "Box2D/Box2D.h"

