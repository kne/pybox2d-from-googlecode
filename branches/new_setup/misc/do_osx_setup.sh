# for releasing mpkg versions of pybox2d. not required for normal installations!

cd ..

CXXFLAGS="-force_cpusubtype_ALL -mmacosx-version-min=10.4"
export CXXFLAGS

rm -rf dist

# python 2.5
rm _Box2D.so Box2D.py
python2.5 setup.py build
/Library/Frameworks/Python.framework/Versions/2.5/bin/bdist_mpkg

# python 2.6
rm _Box2D.so Box2D.py
python2.6 setup.py build
/Library/Frameworks/Python.framework/Versions/2.6/bin/bdist_mpkg

cd misc
