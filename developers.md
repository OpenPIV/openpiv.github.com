---
layout: default
title: How to contribute
---



### How to download the software 
Use <http://www.openpiv.net/downloads.html> for the shortcuts to the zipped software packages or obtain the source code from <http://github.com/openpiv>

### How to contribute
1. Open Github account 
2. Visit our Git repositories through <http://github.com/OpenPIV>
3. Fork your favorite repository, Matlab, Python or C++
4. Fix, commit, push to your repository and send us a pull request or a patch.  
5. register on openpiv-develop mailing list by sending us an [e-mai](mailto:openpiv2008@gmail.com)


### What is the development plan? 

The big plan is:

1. move all the core algorithms for PIV and post-PIV analysis to a library, `libopenpiv` that will include Python or C/C++ code compiled through Cython. The user shall not worry about the arguments or call changes - it has to be simple and transparent.

for example, the FFTW based cross-correlation from C++ 
https://github.com/OpenPIV/openpiv-c--qt/blob/master/src/fftcrosscorrelate.cpp
to create Cython (http://docs.cython.org/src/userguide/wrapping_CPlusPlus.html) thin layer to allow their use from Python, like we already have in C: 
https://github.com/OpenPIV/openpiv-python/blob/master/openpiv/src/process.pyx

2. create test suite for the library - using one of the Python recommended unit test frameworks, py.test or pyunit, etc. 

3. From C++ Qt-based user interface create a clone for the Python version. We started but stopped, cloning the 
https://github.com/OpenPIV/openpiv-c--qt/tree/master/ui into https://github.com/OpenPIV/openpiv-python/tree/master/openpiv/ui
