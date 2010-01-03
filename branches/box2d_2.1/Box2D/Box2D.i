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
    /* To disable assertions->exceptions, comment out the two lines that define
        USE_EXCEPTIONS */
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
    #define USE_EXCEPTIONS 1
    #ifdef USE_EXCEPTIONS
        /* See Common/b2Settings.h also. It defines b2Assert to instead throw
        an exception if USE_EXCEPTIONS is defined. */
        %include "exception.i"

        %exception {
            try {
                $action
            } catch(b2AssertException) {
                // error already set, pass it on to python
            }
        }

        /* Director-exceptions are a result of callbacks that happen as a result to
           the physics step or debug draw, usually. So, catch those errors and report
           them back to Python. */
        %exception b2World::Step {
            try { $action }
            catch (Swig::DirectorException) { SWIG_fail; }
        }
        %exception b2World::DrawDebugData {
            try { $action }
            catch (Swig::DirectorException) { SWIG_fail; }
        }
        %exception b2World::QueryAABB {
            try { $action }
            catch (Swig::DirectorException) { SWIG_fail; }
        }
        %exception b2World::RayCast {
            try { $action }
            catch (Swig::DirectorException) { SWIG_fail; }
        }
    #endif

    #pragma SWIG nowarn=314

    /* ---- classes to ignore ---- */
    /*Most of these are just internal structures, so there is no need to have them
      accessible by Python. You can safely comment out any %ignore if you for some reason
      do need them. Ignoring shrinks the library by a small amount. */
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

    /* Add callback support for the following classes */
    %feature("director") b2ContactListener;
    %feature("director") b2ContactFilter;
    %feature("director") b2DestructionListener;
    %feature("director") b2DebugDraw;
    %feature("director") b2QueryCallback;
    %feature("director") b2RaycastCallback;

    /* ---- includes ---- */
    /* The order of these is important. */

    /* Doxygen-generated docstrings. Can safely be commented out. */
    %include "Box2D/Box2D_doxygen.i"

    /* __dir__ replacement. Can safely be commented out. */
    %include "Box2D/Box2D_dir.i"

    /* __repr__ replacement -- pretty printing. Can safely be commented out. */
    %include "Box2D/Box2D_printing.i"

    /* Miscellaneous inline code. */
    %include "Box2D/Box2D_inline.i"

    /* Miscellaneous extended classes (b2Color, b2Contact, etc.) */
    %include "Box2D/Box2D_misc.i"
    
    /* Typemaps that allow for tuples to be used in place of vectors, 
        the removal of getAsType, etc. */
    %include "Box2D/Box2D_typemaps.i"

    /* b2Vec2, b2Vec3, b2Mat22, b2Transform, b2AABB and related extensions. */
    %include "Box2D/Box2D_vectors.i"

    /* Allows for userData to be used. Also modifies CreateBody/Joint. */
    %include "Box2D/Box2D_userdata.i"

    /* b2World only. */
    %include "Box2D/Box2D_world.i"

    /* b2Body, b2Fixture, and related definitions. */
    %include "Box2D/Box2D_bodyfixture.i"

    /* b2Shape, b2CircleShape, b2PolygonShape. */
    %include "Box2D/Box2D_shapes.i"

    /* All joints and definitions. Defines b2JointTypes dict. */
    %include "Box2D/Box2D_joints.i"

#endif

%include "Box2D/Box2D.h"

