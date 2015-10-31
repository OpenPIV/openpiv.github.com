---
layout: post
title: OpenPIV works on Windows 8.1 64bit
---

Roi Gurka group has revealed a bug in lib.pyx that fails the run of openpiv-python on 64bit Window machines. 
We've looked into it and fixed it in the latest 0.20.1 version, see on PyPi and Github. 

Recommended installation procedure is given below. 



Meanwhile, take a look at the most fresh Physical Review Letter on the aerodynamics of tandem 
flapping wings <http://journals.aps.org/prl/abstract/10.1103/PhysRevLett.115.188101#fulltext> 

We're proud to notice that this interesting work has been performed using OpenPIV. 


Best regards
Alex




------

The instructions to use with Windows 8.1 64 bit machine with Anaconda 64 bit (Python 2.7). 

1. install Microsoft compiler for Python 2.7
a) following this page: https://github.com/cython/cython/wiki/CythonExtensionsOnWindows 
Install Microsoft Visual C++ Compiler for Python just like before.

Launch MSVC for Python command prompt

(go to start menu > Microsoft Visual C++ Compiler Package for Python 2.7 > Visual C++ 2008 32-bit Command Prompt)

Enter the following commands:

    SET DISTUTILS_USE_SDK=1

    SET MSSdk=1

2. Download the updated package of openpiv https://github.com/OpenPIV/openpiv-python/archive/master.zip
3. unzip, e.g. to C:\openpiv, enter the folder and run the setup from the Anaconda shell: 
    $$ python setup.py install

after that the tutorial should work without problem. The tutorial is inside the openpiv package: 

    $$ cd openpiv/tutoria-part1 
    $$ python tutorial-part1.py
