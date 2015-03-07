---
layout: post
title: New user reveals an old bug in Matlab version
---


See the discussion on our forum <https://groups.google.com/forum/#!topic/openpiv-users/017seGOAGWM> 

the new user has accidentally revealed an (apparently) very old bug in openpiv-matlab. It's a very rare
event to have a completely black interrogation window (all zeros) in the image surrounded by non-zero
interrogation windows, but as we see know it happens. When it happens, it corrupts the result by creating 
a non-rectangular matrix of data (x,y,u,v) and then the Spatial Toolbox <https://github.com/OpenPIV/openpiv-spatial-analysis-toolbox> fails. 

See the pull request 4 in the openpiv-matlab repository and details in the forum. Update your version if you use the 
Matlab version. 