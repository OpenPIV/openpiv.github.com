---
layout: post
title: New OpenPIV-Matlab version 
---


Dear OpenPIV users

There is a new version of OpenPIV-Matlab. It finally aligns with the Python version (which is by far more advanced and better supported). In that, we have now two new parameters: 

    scale [m/pix]

and 

    dt [sec]

Default values are 0 - means no scaling and the result is in x,y [pix] and u,v [pix]

It is possible to set separately the dt and get [pix/s] 

The second major change is the output files. Because we now have two options of the output data (pix or m/s) we need a header. The obvious choice is the VEC files with the same construction as Insight (TSI) VEC files, supported by our OpenPIV Spatialbox out of the box


Please, update the openpiv-matlab and openpiv-spatialbox to the newest versions, from Github


<https://github.com/OpenPIV/openpiv-matlab/archive/master.zip>

and

<https://github.com/alexlib/openpiv-spatial-analysis-toolbox/archive/master.zip>

and read the tutorial (v 0.2)  <https://github.com/OpenPIV/openpiv-matlab/blob/master/docs/Tutorial_OpenPIV/Tutorial_OpenPIV.pdf> 
