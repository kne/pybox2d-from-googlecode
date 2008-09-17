rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd

REM Python 2.4
c:\python24\python.exe setup.py build -btemp\build
c:\python24\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd

REM Python 2.5
c:\python25\python.exe setup.py build -btemp\build
c:\python25\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd

REM Python 2.6
c:\python26\python.exe setup.py build -btemp\build
c:\python26\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd

pause

