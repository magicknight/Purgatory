#!/usr/bin/python

# read data from a 3D gray data array then shows slice images from 3 different directions
# python executable

#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################

#========================== definitions ============================================
array_size_z = 335
array_size_y = 280
array_size_x = 750


#========================== plot ============================================

import numpy as np
from matplotlib import pylab as plt
#from scipy import ndimage as nd

def plot(input_path,file_name,output_path):
#data = np.fromfile('t3/reconstruction_sarlo.rec',dtype='float32',sep='') # modify this to read the file 
    data = np.fromfile(input_path+'/'+file_name,dtype='float32',sep='') 
    data = data.reshape([array_size_z,array_size_y,array_size_x]) 


# plot 1 and title
    fig1 = plt.figure()
    fig1.suptitle(file_name)

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

# save image to the output    
    plt.savefig(output_path+'/'+'X_'+file_name+'.png', bbox_inches=0)


# plot 3 and title
    fig3 = plt.figure()
    fig3.suptitle(file_name)

    subfig7 = fig3.add_subplot(3,1,1)
    subfig7.imshow(data[100,:,:])

    subfig8 = fig3.add_subplot(3,1,2)
    subfig8.imshow(data[200,:,:])

    subfig9 = fig3.add_subplot(3,1,3)
    subfig9.imshow(data[300,:,:])

# save image to the output    
    plt.savefig(output_path+'/'+'Z_'+file_name+'.png', bbox_inches=0)

# plot 2 and title
    fig2 = plt.figure()
    fig2.suptitle(file_name)
    
    subfig5 = fig2.add_subplot(2,1,1)
    subfig5.imshow(data[:,100,:])
    #subfig5.set_title('100')

    subfig6 = fig2.add_subplot(2,1,2)
    subfig6.imshow(data[:,200,:])
   # subfig6.set_title('200')

# save image to the output    
    plt.savefig(output_path+'/'+'Y_'+file_name+'.png', bbox_inches=0)

# show the fig2 for reference
    fig2.show()

# for this direction, we make more slices.
    
#    for i in range(array_size_y/5):
#        data2 =  np.mean( [ data[:,i,:],data[:,i+1,:],data[:,i+2,:],data[:,i+3,:],data[:,i+4,:] ], axis = 0 )
#        plt.imshow(data2)
#        plt.savefig(output_path+'/'+'Y_'+file_name+'_'+str(i)+'.png', bbox_inches=0)

    

    

#    plt.show()



#========================== main program ============================================

import sys, getopt, os

def main(argv):

# Parse command-line arguments
   input_path = ''
   output_path = ''
   try:
      opts, args = getopt.getopt(argv,'hi:o:',['ipath=','opath='])
   except getopt.GetoptError:
      print 'test.py -i <input_path> -o <output_path>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <input_path> -o <output_path>'
         sys.exit()
      elif opt in ('-i', '--ipath'):
         input_path = arg
      elif opt in ('-o', '--opath'):
         output_path = arg
   print 'Input path is ', input_path
   print 'Output path is ', output_path

# For each file in the input path, plot 3 different direction slices
   
   for root, dirs, files in os.walk(input_path):
       for name in files:
           plot(input_path, name, output_path)


   raw_input() # Wait for user to plot the next plots


if __name__ == "__main__":
   main(sys.argv[1:])
