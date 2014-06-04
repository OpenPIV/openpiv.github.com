---
layout: post
title: How to use regular expressions
---

### How to load .txt files created by OpenPIV Matlab version for the OpenPIV Spatial Toolbox

The openpiv-matlab creates 3 sets of .txt files in teh folder ```.txt```, ```_flt.txt``` and ```_noflt.txt```

These are the final version (filtered + interpolated), only filtered (not interpolated) and not-filtered (raw) data. 

For the use with openpiv-spatialbox it's easy to choose only the .txt files using the regular expressions:

in the left top corner select ```*.txt``` and in the right to it field enter: 

    ^(?!.*flt*).*$
    
and you'll get in the selection window only the ```.txt``` files. 


<img src="https://dl.dropboxusercontent.com/u/5266698/openpiv-spatialbox-regular-expression.png">
