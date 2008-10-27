from settings import fwSettings

if fwSettings.backend == 'pygame':
    from pygame_main import *
elif fwSettings.backend == 'pyglet':
    from pyglet_main import *
else:
    print 'You have to set a suitable backend setting'
