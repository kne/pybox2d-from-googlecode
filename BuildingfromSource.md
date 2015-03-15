### Building from Source ###

### Linux ###
To compile the latest SVN version, follow these steps:

  1. Download and install the latest version of [SWIG](http://www.swig.org) (preferably 2.0.0+) with your package manager.
> > If you are using **Ubuntu**, you can install it via Synaptic Package Manager (package name 'swig'). You will also need
> > to install the python-dev package, and build-essential (and python-pygame if you want to run the testbed).
```
sudo apt-get install build-essential python-dev swig python-pygame subversion
```
  1. Check out the SVN
```
svn checkout http://pybox2d.googlecode.com/svn/trunk/ pybox2d
```
  1. Build and install the pybox2d library
```
python setup.py build
# Assuming everything goes well...
sudo python setup.py install --force
```

#### Errors ####

#### Old versions of setuptools ####

If you see an error like this:
```
  File "/usr/lib/python2.6/distutils/command/build_ext.py", line 460, in
build_extension
    ext_path = self.get_ext_fullpath(ext.name)
  File "/usr/lib/python2.6/distutils/command/build_ext.py", line 633, in
get_ext_fullpath
    filename = self.get_ext_filename(modpath[-1])
  File "build/bdist.linux-i686/egg/setuptools/command/build_ext.py", line
85, in get_ext_filename
KeyError: '_Box2D'
```

Upgrade your setuptools version. 'setup.py' has been patched in the pybox2d branch
for the upcoming 2.1.0 release, but not for the trunk (2.0.2 series).

#### 64-bit Linux ####
Building from the 2.0.2b1 source release, there will be errors like:
```
Box2D/Box2D_wrap.cpp:3528: error: cast from b2Joint* to int32* loses precision
```
This issue was fixed soon after the release, but it was never repackaged for another release. If you update the individual

files found in [this](http://code.google.com/p/pybox2d/source/detail?r=184) SVN version and recompile, you'll have a mostly identical copy to 2.0.2b1,

just with a few additional setters. If you don't care about having perfect 2.0.2b1 compatibility, try building from the latest SVN instead.

### Windows ###

  1. Install [MinGW](http://downloads.sourceforge.net/mingw/MinGW-5.1.4.exe?modtime=1209244789&big_mirror=1) and then [MSYS](http://downloads.sourceforge.net/mingw/MSYS-1.0.10.exe) so that you can compile Box2D and pybox2d.
  1. Install [SWIG](http://prdownloads.sourceforge.net/swig/swigwin-1.3.40.zip) for making the Python wrapper. Install it in a location in your PATH, or add the SWIG directory to your PATH.
  1. Create Python\Lib\distutils\distutils.cfg, if it doesn't exist, and add:
```
[build]
compiler=mingw32
[build_ext]
compiler=mingw32
```
  1. If you want to build from the SVN, install the [Subversion client](http://subversion.tigris.org/files/documents/15/43360/Setup-Subversion-1.5.1.en-us.msi). Check out the project by doing
```
svn checkout http://pybox2d.googlecode.com/svn/trunk/ pybox2d
```
  1. Run MSYS and locate your pybox2d directory
```
cd /c/path/to/pybox2d/Box2D
```
  1. Build and install pybox2d
```
setup.py build
setup.py install --force
```


### OS X ###

#### Dependencies ####

To build pybox2d, you will need:
  * Apple Developer Tools (see below)
  * SWIG (see below)
  * Python (of course)

#### Install Apple Developer Tools ####

  1. This step is only required if the Apple Developer tools have not already been installed.
  1. Download the Apple Developer Tools or install them from the System Installer CD provided with your Mac.
  1. Download from: http://developer.apple.com/tools/
  1. This will give your system all the tools it needs for software development.
  1. These tools are required for you to proceed to the next step.

#### SWIG Installation ####

  1. Download the latest source release of SWIG [here](http://downloads.sourceforge.net/swig/swig-2.0.3.tar.gz)
  1. Place the file onto your Desktop
  1. Open Terminal.app located in the Applications/Utilities folder
  1. Then enter the following into the terminal window:
```
cd ~/Desktop
tar -zxf swig-*.tar.gz
cd swig-*
./configure
make
sudo make install
<ENTER THE ADMINISTRATOR/ROOT PASSWORD>
```
  1. Hopefully all went well and no errors occurred.
  1. Close the Terminal.app window
  1. SWIG is now installed onto the system and we can now move to the next step.

#### pybox2d Installation ####

  1. Download the latest source distribution of pybox2d [here](http://pybox2d.googlecode.com/files/Box2D-2.0.2b1.zip)
  1. Place the file onto your Desktop
  1. Open Terminal.app located in the Applications/Utilities folder
  1. Then enter the following into the terminal window:
```
cd ~/Desktop
unzip Box2D-*.zip
cd Box2D-*/
python setup.py build
```

> If all went well,
```
sudo python setup.py install --force
<ENTER THE ADMINISTRATOR/ROOT PASSWORD>
```
> Close the Terminal.app window and see the links on the project home page for the testbed and documentation.

#### OS X Snow Leopard / 64-bit Installations ####

Building from the 2.0.2b1 source release, there will be errors like:
```
Box2D/Box2D_wrap.cpp:3528: error: cast from b2Joint* to int32* loses precision
```
This issue was fixed soon after the release, but it was never repackaged for another release. If you update the individual files found in [this](http://code.google.com/p/pybox2d/source/detail?r=184) SVN version and recompile, you'll have a mostly identical copy to 2.0.2b1, just with a few additional setters. If you don't care about having perfect 2.0.2b1 compatibility, try building from the latest SVN instead (see the next section).

#### Building pybox2d from the SVN ####

This is only necessary if you want the latest features that pybox2d has to offer.
Follow the above headings **Install Apple Developer Tools** and **SWIG Installation**. Now follow the steps 2 and beyond for Linux.