rm -rf build temp Box2D_wrap* Box2D2*.py _Box2D2.pyd

REM Python 2.4
c:\python24\python.exe setup.py build -btemp\build
cat license-header.txt > Box2D2_.py
cat Box2D2.py >> Box2D2_.py
mv Box2D2_.py Box2D2.py
c:\python24\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2*.py _Box2D2.pyd

REM Python 2.5
c:\python25\python.exe setup.py build -btemp\build
cat license-header.txt > Box2D2_.py
cat Box2D2.py >> Box2D2_.py
mv Box2D2_.py Box2D2.py
c:\python25\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2*.py _Box2D2.pyd

REM Python 2.6
c:\python26\python.exe setup.py build -btemp\build
cat license-header.txt > Box2D2_.py
cat Box2D2.py >> Box2D2_.py
mv Box2D2_.py Box2D2.py
c:\python26\python.exe setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp Box2D_wrap* Box2D2*.py _Box2D2.pyd

pause

