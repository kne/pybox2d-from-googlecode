# for releasing mpkg versions of pybox2d. not required for normal installations!

CXXFLAGS="-force_cpusubtype_ALL -mmacosx-version-min=10.4 -arch i386 -arch ppc"
export CXXFLAGS
make Gen/float/libbox2d.a
CXXFLAGS="-force_cpusubtype_ALL -mmacosx-version-min=10.4"
export CXXFLAGS

rm -rf dist

rm _Box2D2.so
python2.5 setup.py build
/Library/Frameworks/Python.framework/Versions/2.5/bin/bdist_mpkg

rm _Box2D2.so
python2.6 setup.py build
/Library/Frameworks/Python.framework/Versions/2.6/bin/bdist_mpkg
