# pybox2d -- http://pybox2d.googlecode.com
#
# Copyright (c) 2010 Ken Lauer / sirkne at gmail dot com
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

try:
    from pgu import gui
except:
    raise ImportError('Unable to load PGU')

class fwGUI(gui.Table):
    """
    Deals with the initialization and changing the settings based on the GUI 
    controls. Callbacks are not used, but the checkboxes and sliders are polled
    by the main loop.
    """
    checkboxes =( ("Warm Starting", "enableWarmStarting"), 
                  ("Time of Impact", "enableContinuous"), 
                  ("Draw", None),
                  ("Shapes", "drawShapes"), 
                  ("Joints", "drawJoints"), 
                  ("AABBs", "drawAABBs"), 
                  ("Pairs", "drawPairs"), 
                  ("Contact Points", "drawContactPoints"), 
                  ("Contact Normals", "drawContactNormals"), 
                  ("Center of Masses", "drawCOMs"), 
                  ("Statistics", "drawStats"),
                  ("FPS", "drawFPS"),
                  ("Control", None),
                  ("Pause", "pause"),
                  ("Single Step", "singleStep") )
    form = None

    def __init__(self,settings, **params):
        # The framework GUI is just basically a HTML-like table
        # There are 2 columns right-aligned on the screen
        gui.Table.__init__(self,**params)
        self.form=gui.Form()

        fg = (255,255,255)

        # "Hertz"
        self.tr()
        self.td(gui.Label("F1: Toggle Menu",color=(255,0,0)),align=1,colspan=2)

        self.tr()
        self.td(gui.Label("Hertz",color=fg),align=1,colspan=2)

        # Hertz slider
        self.tr()
        e = gui.HSlider(settings.hz,5,200,size=20,width=100,height=16,name='hz')
        self.td(e,colspan=2,align=1)

        # "Vel Iters"
        self.tr()
        self.td(gui.Label("Vel Iters",color=fg),align=1,colspan=2)

        # Velocity Iterations slider (min 1, max 500)
        self.tr()
        e = gui.HSlider(settings.velocityIterations,1,500,size=20,width=100,height=16,name='velIters')
        self.td(e,colspan=2,align=1)

        # "Pos Iters"
        self.tr()
        self.td(gui.Label("Pos Iters",color=fg),align=1,colspan=2)

        # Position Iterations slider (min 0, max 100)
        self.tr()
        e = gui.HSlider(settings.positionIterations,0,100,size=20,width=100,height=16,name='posIters')
        self.td(e,colspan=2,align=1)

        # Add each of the checkboxes.
        for text, variable in self.checkboxes:
            self.tr()
            if variable == None:
                # Checkboxes that have no variable (i.e., None) are just labels.
                self.td(gui.Label(text, color=fg), align=1, colspan=2)
            else:
                # Add the label and then the switch/checkbox
                self.td(gui.Label(text, color=fg), align=1)
                self.td(gui.Switch(value=getattr(settings, variable),name=variable))

    def updateGUI(self, settings):
        """
        Change all of the GUI elements based on the current settings
        """
        for text, variable in self.checkboxes:
            if not variable: continue
            if hasattr(settings, variable):
                self.form[variable].value = getattr(settings, variable)

        # Now do the sliders
        self.form['hz'].value       = settings.hz
        self.form['posIters'].value = settings.positionIterations
        self.form['velIters'].value = settings.velocityIterations

    def updateSettings(self, settings):
        """
        Change all of the settings based on the current state of the GUI.
        """
        for text, variable in self.checkboxes:
            if variable == None: continue
            setattr(settings, variable, self.form[variable].value)

        # Now do the sliders
        settings.hz = int(self.form['hz'].value)
        settings.positionIterations = int(self.form['posIters'].value)
        settings.velocityIterations = int(self.form['velIters'].value)

        # If we're in single-step mode, update the GUI to reflect that.
        if settings.singleStep:
            settings.pause=True
            self.form['pause'].value = True
            self.form['singleStep'].value = False

