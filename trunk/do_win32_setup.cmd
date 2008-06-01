rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd
c:\python24\python.exe setup.py build -btemp\build
rem c:\python24\python.exe setup.py bdist --formats=zip -btemp\bdist -dinstaller
c:\python24\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller

rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd

c:\python25\python.exe setup.py build -btemp\build
rem c:\python25\python.exe setup.py bdist --formats=zip -btemp\bdist -dinstaller
c:\python25\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller

rm -rf build temp Box2D_wrap* Box2D2.py _Box2D2.pyd
pause

