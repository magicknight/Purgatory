#!/usr/bin/python

# read data from a 3D gray data array then shows image from 3 different direction
# python executable

#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################


import numpy as np
from matplotlib import pylab as plt
from scipy import ndimage as nd

data = np.fromfile('t3/reconstruction_sarlo.rec',dtype='float32',sep='')
data = data.reshape([335,280,750]) # note: for different dimension please modify this


# plot 1
fig1 = plt.figure()

# turn into gray figure
plt.gray()

subfig1 = fig1.add_subplot(2,2,1)
subfig1.imshow(data[:,:,100])

subfig2 = fig1.add_subplot(2,2,2)
subfig2.imshow(data[:,:,300])

subfig3 = fig1.add_subplot(2,2,3)
subfig3.imshow(data[:,:,500])

subfig4 = fig1.add_subplot(2,2,4)
subfig4.imshow(data[:,:,700])


# plot 2
fig2 = plt.figure()

subfig5 = fig2.add_subplot(2,1,1)
subfig5.imshow(data[:,100,:])

subfig6 = fig2.add_subplot(2,1,2)
subfig6.imshow(data[:,200,:])


# plot 3
fig3 = plt.figure()

subfig7 = fig3.add_subplot(3,1,1)
subfig7.imshow(data[100,:,:])

subfig8 = fig3.add_subplot(3,1,2)
subfig8.imshow(data[200,:,:])

subfig9 = fig3.add_subplot(3,1,3)
subfig9.imshow(data[300,:,:])


# show the fig
plt.show()

