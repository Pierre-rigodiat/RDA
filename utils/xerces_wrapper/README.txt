Installation Instructions:

Linux:
- Download Xerces-c 3.1.13
- In setup.py, update the value of library_dirs and include_dirs to the xerces folder
- Run python setup.py install


Cygwin:
- Download Xerces-c 3.1.13
- In setup.py, update the value of library_dirs and include_dirs to the xerces folder
- Run python setup.py install
- Copy _xerces_warpper.dll into the site-packages of python


Tips:
- to know the location of the site-packages folder: import site; site.getsitepackages()