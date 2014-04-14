---
layout: default
title: Frequently Asked Questions
---

### What is OpenPIV?

OpenPIV is a user-friendly software for Particle Image Velocimetry. It incorporates modules written in Matlab, Python and C++ that allows to estimate the velocity fields from images of particles and post-process the fields to obtain important fluid dynamics quantities such as vorticity, rate-of-strain, dissipation and Reynolds stresses in the case of turbulent flows.   

OpenPIV was written in Matlab (tm) in 1998 and was extended using Python and C++ (with Qt4 user interface). OpenPIV is designed to be portable: it supposedly runs on UNIX, Mac and  PCs under Windows or Linux. 


### How to cite this work 

Taylor, Z.J.; Gurka, R.; Kopp, G.A.; Liberzon, A.; , "Long-Duration Time-Resolved PIV to Study Unsteady Aerodynamics," Instrumentation and Measurement, IEEE Transactions on , vol.59, no.12, pp.3262-3269, Dec. 2010
doi: 10.1109/TIM.2010.2047149
URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=5464317&isnumber=5609237

 
### Why OpenPIV was created? 

OpenPIV was created in order to combine the know-how of different developers into a single, coherent group developing the next generation of the open source Particle Image Velocimetry software. It is based on the three older packages URAPIV, PyPIV, and URAPIV-C++. We hope that other open source PIV developers will join this initiative.

 
### What is OpenPIV good for? 
OpenPIV is good for analysing your PIV images, acquired with frame-straddle or continuous, time-resolved PIV system. It is good to check if your commercial software is not producing any strange results, it is good to use for the images taken not only of fluid, but also solid motion, cell tracking, bees or flies or birds tracking, etc.

 
### Are there copyright restrictions on the use of OpenPIV? 
Not at all if you do educational oriented or scientific work. If it is for commercial purposes, please note that we use free Qt license and therefore your derivative cannot be delivered as a commercial software. 



### How to download the software 
Use <http://www.openpiv.net/downloads.html> for the shortcuts to the zipped software packages or obtain the source code from <http://github.com/openpiv>

### How to contribute
1. Open Github account 
2. Visit our Git repositories through <http://github.com/OpenPIV>
3. Fork your favorite repository, Matlab, Python or C++
4. Fix, commit, push to your repository and send us a pull request or a patch.  
5. register on openpiv-develop mailing list by sending us an [e-mai](mailto:openpiv2008@gmail.com)



### Getting started screencasts and tutorials

1. Matlab - see the screencast http://youtu.be/yg-LjAt-v3Q or read the tutorial by <a href="mailto:Sergio.Bengoechea.Lozano@tnt.TU-Berlin.DE"> Sergio Bengoechea Lozano, TU Berlin </a>
[[https://github.com/OpenPIV/openpiv.github.com/wiki/Tutorial_OpenPIV.pdf]]
2. Python - http://www.openpiv.net/openpiv-python/
3. C++ - not ready yet
4. Spatial and Temporal Analysis Toolbox http://www.openpiv.net/openpiv-spatial-analysis-toolbox/


### Support and documentation
How to get support? Where to ask questions? Use one of the following:
1. Use our mailing list [openpiv-users@googlegroups.com](mailto:openpiv-users@googlegroups.com)
2. E-mail to [openpiv2008@gmail.com](openpiv2008@gmail.com)
3. Comment on the Github repository or open an issue on Github


### How do we help our users

We typically answer very quickly on our mailing list. Users that have difficulty to read images or process it, send e-mails like this one: 

	`Dear Sir/Madam,

	I am not being able to load images at all. Everytime I try to load an image tif/bmp/etc... I hear a error sound on my mac and thats it.
	Any advice?`


We usually suggest to have a Dropbox or FTP with a bunch of images (in this particular case it was very helpful to see more than just a first pair, because there is no motion in the first pair). 

We got a Dropbox share and the question about our Matlab GUI-based version. So instead of writing back, we shot this screenshot and send back to the user. **On the way to the next satisfied OpenPIV user :)**

[Screenshot of Matlab GUI-based OpenPIV session](https://www.dropbox.com/s/ysyvl8oxw635pqg/Screen%20Recording%2011%20-%20Wi-Fi.m4v)


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


-----

### What are the parameters used in OpenPIV 


#### Can you please elaborate on the ''''sclt'''' parameter which is passed to the openpiv function.
E.g. if the time between the two consecutive image is 0.5 seconds and 1 pixel in the image corresponds to 50 cms, what would be the value of sclt.

**sclt** is a shortcut for _scaling factor from displacement to velocity units_. It's also called the _scale_, or _scaling_.

PIV provides the local displacement in pixel units. In order to know the displacement in the real physical units you multiply it by the scaling of **cm/pixel**, i.e. by 50 cm/pixel. To know the speed, the displacement is divided by the time separation, i.e. by 0.5 seconds, then we get: 
`scaling = sclt = 50 cm/pixels / 0.5 = 100 [cm/seconds/pixels]`

For example, if the vector is 10 pixels, then the result will be `100 * 10 = 1000 cm/s`

### Whats the purpose of the local and global filtering?

**global filtering** supposingly removes the obvious **outliers**, i.e. the vectors which length is larger than the mean of the flow field plus 3 times its standard deviation. These are global outliers in the statistical sense.

**local filtering** is performed on small neighborhoods of vectors, e.g. 3 x 3 or 5 x 5, in order to find **local outliers** - the vectors that are dissimilar from the close neighbors. Typically there are about 5 per-cent of erroneous vectors and these are removed and later the missing values are interpolated from the neighbor vector values. This is also a reason for the Matlab version to generate three lists of files:
**raw** - **_noflt.txt**
**filtered** (after global and local filters) - **_flt.txt**
final (after filtering and interpolation) - **.txt**

### Why, while taking the FFT, we use the Nfft parameter? 

`ffta=fft2(a2,Nfft,Nfft);           
fftb=fft2(b2,Nfft,Nfft);`

and why the size has been specified as Nfft which is twice the interrogation window size.

In the FFT-based correlation analysis, we have to pad the window with zeros and get correlation map of the right size and avoid aliasing problem (see Raffel et al. 2007)

### Also in the same function why sub image **b2** is rotated before taking the correlation.
`b2 = b2(end:-1:1,end:-1:1);`

Without rotation the result will be convolution, not correlation. The definition is **ifft(fft(a)*fft(conj(b)))**. conj() is replaced by rotation in the case of real values. It is more computationally efficient.


### In the find_displacement(c,s2nm) function for finding peak2, why neighbourhood pixels around peak1 are removed?   %line no:352

These peaks might appear as 'false second peak', but they are the part 
of the same peak. Think about a top of a mountain. You want to remove
not only the single point, but cut out the top part in order to search 
for the second peak.

### In the read_pair _of_images( ) function why
`A = double(A(:,:,1))/255;           %line no:259
B = double(B(:,:,1))/255;`

In order to convert RGB to gray scale. Not always true. 

### After the program is executed, the variable vel contains all the parameters for all the velocity vectors. Here what are the units of u & v. Is it in metres/second?

It is not, the result depends on the **SCLT** variable. if it SCLT is 1, then it is in **pixels/dt** (dt is the interval between two images).


### What is the "Outlier Filter Value" in OpenPIV?

The outlier filter value is the threshold of the global outlier filter and is says how many times the standard deviation of the whole vector field is exceeded before the vector is considered as outlier. See above discussion on the filters. 



### What is the fifth column in the Output data *.txt,*flt.txt or *noflt.txt?

The fifth column is the value of the Signal-To-Noise (s2n) ration. Note that the value is different (numerically) if the user choses Peak-to-Second-Peak ratio as the s2n parameter or Peak-to-Mean ratio as s2n parameter. The value of Peak-to-Second-Peak or Peak-to-Mean ratio is stored for the further processing. 
