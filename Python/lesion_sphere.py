#!/usr/bin/python

# This function returns an m by n array, X, in which 
# each of the m rows has the n Cartesian coordinates 
# of a random point uniformly-distributed over the 
# interior of an n-dimensional hypersphere with 
# radius r and center at the origin.  The function 
# 'randn' is initially used to generate m sets of n 
# random variables with independent multivariate 
# normal distribution, with mean 0 and variance 1.
# Then the incomplete gamma function, 'gammainc', 
# is used to map these points radially to fit in the 
# hypersphere of finite radius r with a uniform spatial distribution.
# 
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################

import  numpy as np
import string

size = 42

data = np.empty((size,size,size),dtype = 'float32')
for i in range(size):
    for j in range(size):
        for k in range(size):
            if np.sqrt((i-float(size-1)/2.0)**2 + (j-float(size-1)/2.0)**2 + (k-float(size-1)/2.0)**2) <= 20:
                data[i][j][k] = -1
                
# See this sphere in a 3D image:
#from mayavi.mlab import *
#obj = contour3d(data)

# see sphere size
len(data[data.nonzero()])
# Save to raw binary file:
data.tofile('lesion_sphere_'+str(size)+'_8mm.obj')

