import re
grabbing = False
grabText = []
cname = ""

classes = {}
classname = ""
secname = ""
nextid = ""
nextlink = ""

def eval(var, value):
    global classname
    global secname
    global nextid
    global nextlink

    if var == "cp-name":
        classname = value
        print "Class:", classname
        classes[classname] = { "__id__": nextid, "__link__": nextlink }
        print classname, nextid, nextlink
    elif var == "sec-mem-name":
        print "|->", var, "=", value
        secname = value
        classes[classname][secname] = { "__id__": nextid, "__link__": nextlink }
        print secname, nextid, nextlink
    elif var == "cp-id":
        nextid = value
        nextlink = nextid + ".htm"
    elif var == "sec-mem-id":
        nextid = value

        # make a html link out of it (only by observation - is this right?)
        clen = len(classes[classname]["__id__"])+2
        nextlink = classes[classname]["__id__"] + ".htm#" + nextid[clen:]

    replace_pairs = ( 
        ("@warning", "'''Warning'''"), 
#        ("@param", "'''Param'''"), 
        ("@return", "'''Returns'''"), 
        ("@see", "See"), 
        )

    for rfrom, rto in replace_pairs:
        value = value.replace(rfrom, rto)

    value = re.sub("@param\s(.*?)\s", r"'''\1''' ", value)

    if var == "sec-mem-briefdesc":
        if value.strip():
            classes[classname][secname]["briefdesc"] = value.strip()
            print "#", value.strip()
    elif var == "sec-mem-documentation":
        if value.strip():
            classes[classname][secname]["documentation"] = value.strip()
            print "#", value.strip()

for line in open("doxygen.def").readlines():
    if grabbing:
        if line.strip() == grabbing:
            grabbing = False
            eval(var, "".join(grabText))
        else:
            grabText.append( line )
        continue

    if "=" not in line:
        continue

    m = re.search("\s*(.*?)\s*=\s*'(.*)';", line)
    if m:
        var = m.groups()[0]
        value = m.groups()[1]
    else:
        m = re.search("\s*(.*?)\s*=\s*<<(.*)$", line)
        if m:
            var = m.groups()[0]
            grabbing = m.groups()[1] + ";"
            grabText = []
        continue

    eval(var, value)

import pickle

f = open("d:/dev/pybox2d/misc/gendoc/docs.pkl", "wb")
pickle.dump(classes, f)
f.close()
