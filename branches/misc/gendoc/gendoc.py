import Box2D2 as b2
import types
import re
import pickle

f = open("docs.pkl", "rb")
classes = pickle.load(f)
f.close()

ignore_list = ["Box2D2", "new", "new_instancemethod", "weakref", 
    "weakref_proxy", "func_code", "thisown", "b2Alloc", "b2BlockAllocator", "this", ]

internal_list = ["b2BodyCompare", "b2ShapeCompare", "b2CollideCircles", "b2CollidePolyParticle",
     "b2CollidePolygonAndCircle", "b2CollidePolygons", "collideCircleParticle" ]

def is_basic_type(x):
    if isinstance(x, (int, float, bool, str, tuple, list, types.NoneType)): return True
    return False

def has_info(x):
    if is_basic_type(x): 
        return False
    if isinstance(x, type(b2.b2World.CreateBody)): # instancemethod
        return False
    return True

def checkdocstr(s):
    m = re.search(".*_get\(.*\) -> (.*)", s)
    if m:
        return "Type: " + m.groups()[0]
    m = re.search("^Proxy of C\+\+ (.*) class", s)
    if m:
        return ""
    return "Docstring: " + reindent(s,0).replace("\n", "\n\n")

def reindent(str, count):
    lines = str.split("\n")
    ret = [" " * count + line.strip() for line in lines]
    return "\n".join(ret)
    
def finddocs(name):
    global classes
    tree = name.split(".")
    if len(tree) >= 3:
        try:
            docs = classes[tree[1]][tree[2]]
            ret =""
            if "briefdesc" in docs:
                ret += "\nDescription:\n" + docs["briefdesc"]
            if "documentation" in docs:
                ret += "\nDocumentation: {{apiref|" + docs["__link__"] + "}}" + "\n" + reindent(docs["documentation"], 1)
            return "", ret
        except KeyError:
            return "", ""
    elif len(tree) >= 2:
        try:
            return "{{apiref|" + classes[tree[1]]["__link__"] + "}}", ""
        except KeyError:
            return "", ""
    return "", ""

def get_info(c, cstr, level, maxlevel):
    internals = []
    externals = []
    basics    = []
    for s_attr in dir(c):
        if "_swigregister" in s_attr or s_attr[0]=="_": continue
        if "func_" in s_attr: continue
        if s_attr in ignore_list: continue

        attr = getattr(c, s_attr)

        # header = "=" * (level+2)
        if level == 1:
            header = "=="
        else: # level > 1:
            header = "'''"

        addon = []
        #print s_attr, type(attr)
        if s_attr=="cvar" or is_basic_type(attr):
            if level==1:
                addon = [ " ".join( ("'''", s_attr, "'''") ), "=" + str(attr), "" ]
                basics.extend(addon)
                continue
            else:
                addon = [ " ".join( ("'''", s_attr, "'''", str(type(attr))) ), "" ]
        else:
            link, docs = finddocs(cstr + "." + s_attr)
            docstring = checkdocstr(str(getattr(c, s_attr).__doc__))

            addon.append(" ".join( (header, s_attr, header) ))
            addon.append(link)

            if docstring: addon.append(docstring)
            if docs: addon.append(docs)

            if has_info(attr) and level+1 < maxlevel:
                addon.append("")
                bas_add, int_add, ext_add = get_info(attr, cstr + "." + s_attr, level+1, maxlevel)

                if s_attr in internal_list:
                    internals.extend(addon)
                else:
                    externals.extend(addon)
                basics.extend(bas_add)
                internals.extend(int_add)
                externals.extend(ext_add)
                continue

        addon.append("")

        if s_attr in internal_list:
            internals.extend(addon)
        else:
            externals.extend(addon)


    return basics, internals, externals


doc_bas, doc_int, doc_ext = get_info(b2, "Box2D", 1, 3)

print "= Interface ="
print "\n".join(doc_ext)
print "= Basics ="
print "\n".join(doc_bas)
print "= Internals ="
print "\n".join(doc_int)
