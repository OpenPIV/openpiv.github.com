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


### What are the parameters used in OpenPIV 


#### Can you please elaborate on the ''''sclt'''' parameter which is passed to the openpiv function.
E.g. if the time between the two consecutive image is 0.5 seconds and 1 pixel in the image corresponds to 50 cms, what would be the value of sclt.

**sclt** is a shortcut for _scaling factor from displacement to velocity units_. It's also called the _scale_, or _scaling_.

PIV provides the local displacement in pixel units. In order to know the displacement in the real physical units you multiply it by the scaling of **cm/pixel**, i.e. by 50 cm/pixel. To know the speed, the displacement is divided by the time separation, i.e. by 0.5 seconds, then we get: 
	scaling = sclt = 50 cm/pixels / 0.5 = 100 [cm/seconds/pixels]

For example, if the vector is 10 pixels, then the result will be

		100 * 10 = 1000 cm/s

### Whats the purpose of the local and global filtering?

**global filtering** supposingly removes the obvious **outliers**, i.e. the vectors which length is larger than the mean of the flow field plus 3 times its standard deviation. These are global outliers in the statistical sense.

**local filtering** is performed on small neighborhoods of vectors, e.g. 3 x 3 or 5 x 5, in order to find **local outliers** - the vectors that are dissimilar from the close neighbors. Typically there are about 5 per-cent of erroneous vectors and these are removed and later the missing values are interpolated from the neighbor vector values. This is also a reason for the Matlab version to generate three lists of files:
**raw** - **_noflt.txt**
**filtered** (after global and local filters) - **_flt.txt**
final (after filtering and interpolation) - **.txt**

### Why, while taking the FFT, we use the Nfft parameter? 

		ffta=fft2(a2,Nfft,Nfft);
		fftb=fft2(b2,Nfft,Nfft);`

and why the size has been specified as Nfft which is twice the interrogation window size.

In the FFT-based correlation analysis, we have to pad the window with zeros and get correlation map of the right size and avoid aliasing problem (see Raffel et al. 2007)

### Also in the same function why sub image **b2** is rotated before taking the correlation.
		b2 = b2(end:-1:1,end:-1:1);

Without rotation the result will be convolution, not correlation. The definition is 
		ifft(fft(a)*fft(conj(b))) 

conj() is replaced by rotation in the case of real values. It is more computationally efficient.


### In the find_displacement(c,s2nm) function for finding peak2, why neighbourhood pixels around peak1 are removed?   		%line no:352

These peaks might appear as 'false second peak', but they are the part 
of the same peak. Think about a top of a mountain. You want to remove
not only the single point, but cut out the top part in order to search 
for the second peak.

### In the read_pair _of_images( ) function why
		A = double(A(:,:,1))/255;           %line no:259
		B = double(B(:,:,1))/255;`

In order to convert RGB to gray scale. Not always true. 

### After the program is executed, the variable vel contains all the parameters for all the velocity vectors. Here what are the units of u & v. Is it in metres/second?

It is not, the result depends on the **SCLT** variable. if it SCLT is 1, then it is in **pixels/dt** (dt is the interval between two images).


### What is the "Outlier Filter Value" in OpenPIV?

The outlier filter value is the threshold of the global outlier filter and is says how many times the standard deviation of the whole vector field is exceeded before the vector is considered as outlier. See above discussion on the filters. 



### What is the fifth column in the Output data *.txt,*flt.txt or *noflt.txt?

The fifth column is the value of the Signal-To-Noise (s2n) ration. Note that the value is different (numerically) if the user choses Peak-to-Second-Peak ratio as the s2n parameter or Peak-to-Mean ratio as s2n parameter. The value of Peak-to-Second-Peak or Peak-to-Mean ratio is stored for the further processing. 
