pygame_path = ".." # path to pygame testbed files
ignore = [ "main" ]

import os
import re

print "Running this will overwrite files."
os.system("pause")

def checkFile(file):
    if file[-3:]==".py" and file[:5]=="test_":
        name = file[5:-3].lower()
        if name in ignore:
            return False
        return True
    return False

files = [file for file in os.listdir(pygame_path) if checkFile(file)]

for file in files:
    outfile = open(file, "w")
    for line in open(os.path.join(pygame_path, file), "r").readlines():
        if line.find("from pygame.locals import *") > -1:
            line = "import pyglet\n"
        elif line.find("key==K_") > -1:
            # terrible code, use regexps please
            line=line.replace("K_EQUALS", "pyglet.window.key.EQUAL")
            line=line.replace("key==K_", "key==pyglet.window.key.")
            temp = line.split("window.key.")
            temp[1] = temp[1][0].upper() + temp[1][1:]
            line = "window.key.".join(temp)
        outfile.write(line)
