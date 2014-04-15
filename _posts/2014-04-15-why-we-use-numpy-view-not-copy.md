---
layout: post
title: Why the velocity matrix has been changed every time
---

### Numpy view vs copy

OpenPIV is based on Numpy, Scipy and Matplotlib. Therefore, the most basic assumption that is important to remember is that the Numpy array assignment is ** most of the time a view ** into another array and not a copy of the array. This is to say that: 

	x = np.array([1,2,3,4])
	y = x
	z = x.copy()
	x[0] = 5
	print x
	print y
	print z


would output:

	[5,2,3,4]
	[5,2,3,4]
	[1,2,3,4]

Thus `y` is just a view of `x` and it's an assignment by reference, while `z` is a copy of `x` at the moment of creation and therefore it's an assignment by value. 

See how this affects your understanding of the results of OpenPIV: 

<http://nbviewer.ipython.org/gist/anonymous/10749186>
