---
layout: default
title: Frequently Asked Questions about OpenPIV parameters
---
## Frequently Asked Questions about OpenPIV parameters



### What is the development plan? 

The plan is:



1. The algorithms, e.g. FFTW based cross-correlate from C++ 
https://github.com/OpenPIV/openpiv-c--qt/blob/master/src/fftcrosscorrelate.cpp
to create Cython (http://docs.cython.org/src/userguide/wrapping_CPlusPlus.html) thin layer to allow their use from Python, like we already have in C: 
https://github.com/OpenPIV/openpiv-python/blob/master/openpiv/src/process.pyx

2. From C++ Qt-based user interface create a clone for the Python version. We started but stopped, cloning the 
https://github.com/OpenPIV/openpiv-c--qt/tree/master/ui into https://github.com/OpenPIV/openpiv-python/tree/master/openpiv/ui


### How to join the development team? 

1. Write us an e-mail
2. Fork the openpiv-python https://github.com/OpenPIV/openpiv-python 
3. Add or edit the core algorithms, user interface (using Qt) or post-processing routines and send us the patch or pull requests



### What are the various parameters used in OpenPIV? 

See the discussion below. 


: Hello,
:
: Thanks for the quick reply. I was able to execute the program. After going
: through the program I have some queries. It would be very kind of you if you
: clear it.
:
: 1) Can you please elaborate on the 'sclt' parameter which is passed to the
: urapiv function.
: If the time between the two consecutive image is 0.5 seconds and 1 pixel in
: the image corresponds to 50 cms, what would be the value of sclt.

PIV gives displacement in pixels, to know the displacement in your
units you multiply it by the scaling of cm/pixel, i.e. by 50 cm/pixel.
To know the speed, the displacement is divided by the time separation,
i.e. by 0.5 seconds, then we get: sclt = 50 cm/pixels / 0.5 = 100
[cm/seconds/pixels]. For example, if the vector is 10 pixels, then the
result will be 100 * 10 = 1000 cm/s

:
: 2) If the crop vector is assigned anything other than [0 0 0 0], it gives
: the following error msg..
:
: Enter the number of interrogation lines to crop
:  [Left,Top,Right,Bottom], Enter for none    [1 1 1 1]
:  Working on 1 pixels row
: .
crop is a vector that includes a number of rows or columns of interrogation windows to crop
from the borders of the image. For example, if I do 32 x 32
interrogation windows and I want to remove the top 100 pixels, I use
[0 3 0 0] (3 x 32 = 96 pixels). In your case, I need to see the images
and try it myself to be able to find the error. Please, send a pair of
images and I'll see what's going on.

:
: 3) Whats the purpose of the local and global filtering?

global filtering supposingly removes the obvious outliers, i.e. the
vectors which length is larger than the mean of the flow field plus 3
times its standard deviation. These are global outliers in the
statistical sense.

:
: 4) In the cross_correlate(a2,b2.Nfft) function, why the average value of the
: pixels are subtracted from the sub image.
: a2 = a2 - mean2(a2);         %line no:303
: b2 = b2 - mean2(b2);

you have to understand the correlation principle in this case, I
suggest to go for the book of Raffel et al. (1998). In one sentence, if your images
have not absolutely black background (zero), then the background
(which is a kind of noise) contributes to the correlation and this is
undesirable. you're welcome to change it and check. maybe in some
cases it is not true. I didn't find such a case.

:
: Also in the same function while taking the fft
: ffta=fft2(a2,Nfft,Nfft);            %line no:308
: fftb=fft2(b2,Nfft,Nfft);
: why the size has been specified as Nfft which is twice the interrogation
: window size.

the same remark: we do correlation analysis, this Nfft is to pad the
window with zeros and get correlation map of the right size.

:
: Also in the same function why sub image b2 is rotated before taking the
: correlation.
: b2 = b2(end:-1:1,end:-1:1);         %line no:306

otherwise the result will be convolution, not correlation. the
definition is ifft(fft(a)*fft(conj(b))). conj() is replaced by
rotation in the case of real values. It is more computationally
efficient.

:
:
: 5) In the find_displacement(c,s2nm) function for finding peak2, why
: neighbourhood pixels around peak1 are removed?   %line no:352

otherwise, they appear as 'false second peak', but they are the part
of the same peak. Think about a top of a mountain. You want to remove
not only the single point, but cut out the top part in order to search
for the second peak.

:
: 6) In the read_pair _of_images( ) function why
:   A = double(A(:,:,1))/255;           %line no:259
:   B = double(B(:,:,1))/255;
: statements are used.

to convert RGB to gray scale. Not always true. Should be verified for
your images. This is a version issue. not well documented, sorry.

:
: 7) After the program is executed, the variable vel contains all the
: parameters for all the velocity vectors. Here what are the units of u & v.
: Is it in metres/second?
:

it is not, it depends on your SCLT variable. if it SCLT is 1, then it
is in pixels/dt (dt is the interval between two images)
