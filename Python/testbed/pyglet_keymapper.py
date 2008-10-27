from pyglet.window import key
import string

def map_keys():
    keys = {}
    for letter in string.uppercase:
        keys['K_'+letter.lower()] = getattr(key, letter)
    
    return keys

temp = globals() 
temp.update(map_keys())

del key
del string
del temp
