---
layout: post
title: OpenPIV runs in parallel on any platform
---


At Turbulence Structure Laboratory we create sometimes huge numbers of PIV realisations. The latest example is 1200 images (time resolved)
PIV, 5 repetitions per frequency, 3 frequencies, 3 polymer concentrations and water reference case. In total 1200 x 5 x 3 x 4 = 72000 PIV maps to be
analysed. The greatness of OpenPIV that runs on Python is not only the brilliance of the algorithms, not the clear and open code, but 
the fact that we are standing on the shoulders of (really) giants: NumPy, SciPy, Matplotlib, IPython and Cython. It allows us to use the C code
for the speed and embarrassingly easy parallelisation using multitasking capabilities of Python and IPython. So, without changing the algorithm, 
we can share the hard drive over the local ethernet network and get few PCs running Linux or Windows or Mac OS X to run OpenPIV, 
each on multiple cores. See the screenshot of all the CPUs crunching in parallel the long set of PIV images (see on the left). 

We can process sequences, pairs, triples, pairs with varying jums and dynamic time intervals, etc. 

we need more hands on testing, documentation, future developments, see on www.openpiv.net﻿

<https://plus.google.com/u/0/b/109825446414710739212/+OpenpivNet/posts>
