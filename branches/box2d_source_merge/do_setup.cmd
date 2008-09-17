rm -rf build temp
setup.py build -btemp\build
setup.py bdist --formats=zip -btemp\bdist -dinstaller
setup.py bdist_wininst -t"pyBox2D Installer" --bdist-dir temp\bdist_wininst -dinstaller
rm -rf build temp
pause
