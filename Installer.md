# New version? #
Installers for 2.1 are not yet available. A precompiled version of the current SVN will always be available for Python 2.6/win32 (see [here](https://pybox2d.googlecode.com/svn/trunk/library/)), but for other platforms or Python versions, you must be prepared to build the library until there is an official release.

For the previous 2.0.2 versions, there should be installers available for most platforms and (semi-recent) Python versions. Please find the section below related to your platform, and then head to the download page.

## setuptools eggs ##

The [setuptools](http://peak.telecommunity.com/DevCenter/setuptools) eggs are available on this site and also on [pypi](http://pypi.python.org/pypi/Box2D).

To install these, first install [setuptools](http://peak.telecommunity.com/dist/ez_setup.py) (by opening it with Python) and then run: easy\_install box2d
This should find and download the appropriate eggs for your platform and install them in your site-lib directory.

Alternatively, you can download the egg from the download page, and run easy\_install on it or simply place it in your site-packages directory.

# Linux #

## Do I need to install libbox2d first? ##

No, everything that is necessary to run the basic library is included. Even if you are building from the source (see [here](BuildingfromSource.md)), the library code is included such that nothing else is necessary (except for the right tools to build it with).

## Ubuntu ##

pybox2d 2.0.2 is available via the package manager.
```
sudo apt-get install python-box2d
```

## Other distributions ##

[Build](BuildingfromSource.md) the source or use the i686 eggs with easy\_install from the Downloads page.

# OS X #

## Dependencies ##

**NOTE** The pybox2d installer will **NOT** work with the default Python installed by OS X **NOTE**

You must install a Python version from the official [site](http://www.python.org/download/).

### pygame ###

**pygame** is not included in the installer. If you want to try the testbed applications (and you should), you must install pygame. From the [pygame](http://www.pygame.org) site:

http://pygame.org/ftp/pygame-1.9.1release-py2.6-macosx10.5.zip (for Python 2.6)

http://pygame.org/ftp/pygame-1.9.1release-py2.5-macosx10.5.zip (for Python 2.5)

Note that pyobjc is no longer necessary for new versions of pygame.

### Directories ###

The library itself is installed in Python's site-packages directory: **/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/Box2D**

If, for some reason, you delete the site-packages and need to reinstall it (and the installer isn't putting the files there), you can try deleting **/Library/Receipts/Box2D**

# Windows #

## Dependencies ##

Requires the Python versions from the official [site](http://www.python.org/download/).

## pygame ##

**pygame** is not included in the installer. If you want to try the testbed applications (and you should), you must install [pygame](http://www.pygame.org) for your version of Python (to see your Python's version, go to the command prompt and type `python -V`.)

## Directories ##

The library itself is installed in Python's site-packages directory: **C:\Python25\lib\site-packages\Box2D\**