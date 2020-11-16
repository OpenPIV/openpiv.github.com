---
layout: default
title: Frequently Asked Questions
---

### What is Particle Image Velocimetry (PIV)
It is optical method for fluid flow measurements. Read more on the Wikipedia https://en.wikipedia.org/wiki/Particle_image_velocimetry

### What is OpenPIV?

OpenPIV is a user-friendly software for Particle Image Velocimetry. It contains software in Python, Matlab, and C++ that allows to estimate the velocity fields from images of particles and post-process the fields to obtain important fluid dynamics quantities such as vorticity, rate-of-strain, dissipation and Reynolds stresses in the case of turbulent flows. The main development focus now is on **Python** version. 


OpenPIV was originally written in Matlab (tm) in 1998 but switched to Python. OpenPIV is designed to be portable: it runs on all platforms, on mobiles, and on high performance clusters and on virtual machines. 


### Why OpenPIV was created? 

OpenPIV was created in order to combine the know-how of different developers into a single, coherent group developing the next generation of the open source Particle Image Velocimetry software. It is based on the three older packages URAPIV, PyPIV, and URAPIV-C++. We hope that other open source PIV developers will join this initiative.

 
### What is OpenPIV good for? 
OpenPIV is good for analysing your PIV images, acquired with frame-straddle or continuous, time-resolved PIV system. It is good to check if your commercial software is not producing any strange results, it is good to use for the images taken not only of fluid, but also solid motion, cell tracking, bees or flies or birds tracking, etc.

 
### Are there copyright restrictions on the use of OpenPIV? 
Read the LICENSE files in repositories, we use standard open source licenses. 

### How to cite

If you use the Python version, you can cite all versions by using the[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3930343.svg)](https://doi.org/10.5281/zenodo.3930343)

If you use another package, please the Readme files in every package: Matlab, Python, C++ and the toolboxes were created at different times and by different teams. 


---
---

 
### What are the parameters used in OpenPIV 

#### Scaling or `sclt`

*Scaling* parameter converts the `pixel/dt` units into `meters/second` or other physical units. For example, if the time between the two consecutive image is `dt = 0.5` seconds and the magnification is such that `1 pixel` in the image corresponds to `50 cm`, then the value of `sclt` is estimated as:

	sclt = 50 cm/pixels / 0.5 sec/dt = 100 [cm/seconds/pixels]

For example, if a given displacement vector was esitmated to be `10 pixels`, then the velocity will be

		100 * 10 = 1000 cm/s


#### Whats the purpose of the local and global filtering?

**global filtering** supposingly removes the obvious **outliers**, i.e. the vectors which length is larger than the mean of the flow field plus 3 times its standard deviation. These are global outliers in the statistical sense.

**local filtering** is performed on small neighborhoods of vectors, e.g. 3 x 3 or 5 x 5, in order to find **local outliers** - the vectors that are dissimilar from the close neighbors. Typically there are about 5 per-cent of erroneous vectors and these are removed and later the missing values are interpolated from the neighbor vector values. This is also a reason for the Matlab version to generate three lists of files:
**raw** - **_noflt.txt**
**filtered** (after global and local filters) - **_flt.txt**
final (after filtering and interpolation) - **.txt**


### Why, while taking the FFT, we use larger windows that the interrogation windows:

		ffta = fft2( a2, Nfft, Nfft );
		fftb = fft2( b2, Nfft, Nfft );`

and why the size has been specified as `Nfft` which is *twice the interrogation window size*.

In the FFT-based correlation analysis, we have to pad the interrogation window with zeros and get correlation map of the right size and avoid aliasing problem (see Raffel et al. 2007)


#### Also in the same function why sub image `b2` is rotated before taking the correlation

		b2 = b2(end:-1:1,end:-1:1);

Without rotation the result will be convolution. The definition is 

		ifft(fft(a)*fft(conj(b))) 

so, the operation `conj()` is replaced by *rotation* which is identical **in the case of real values**. It is more computationally efficient.


#### In the `find_displacement(c,s2nm)` function for finding `peak2`, why neighbourhood pixels around `peak1` are masked? 

These peaks might appear as "false second peak"'", but they are the part 
of the same peak. Think about a top of a mountain. You want to remove
not only the single point, but cut out the top part in order to search 
for the second peak.


#### After the program is executed, the variable `vel` contains all the parameters for all the velocity vectors. Here what are the units of `u, v`. Is it in metres/second?

It is not, the result depends on the `sclt` variable. if `sclt` is not used (i.e. equalt to 1) then the output is in `pixels/dt`, where `dt` is the time interval between the two PIV images.


#### What is the "Outlier Filter Value" in OpenPIV?

The outlier filter value is the threshold of the global outlier filter and is says how many times the standard deviation of the whole vector field is exceeded before the vector is considered as outlier. See above the discussion on various filters. 



#### What are the fifth and sixth columns in the data`*.txt`b,`*flt.txt` or `*noflt.txt`?

The fifth column is the value of the `Signal-To-Noise` (`s2n`) ratio. The sixth column is a mask of invalid vectors. Note that the value is different (numerically) if the user choses `Peak-to-Second-Peak` ratio as the `s2n` parameter or `Peak-to-Mean` ratio as `s2n` parameter. The value of `Peak-to-Second-Peak` or `Peak-to-Mean` ratio is stored for the further processing. 
