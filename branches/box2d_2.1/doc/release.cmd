@echo off
@echo --- Building ---
cd ..
call build
cd doc
cd Doxygen
@echo --- Doxygen ---
call generate
cd ..

@echo --- Epydoc ---
python gen_epydoc.py

@echo --- Adding the files to the SVN ---
svn -q add doxygen/html_output/*
svn -q add doxygen/xml_output/*
svn -q add epydoc/*
