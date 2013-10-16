#!/usr/bin/python

# read data from a 3D gray data array then make slice images from 3 different directions
# images are 2D data, average from each 5 slices from each direction.
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
#array_size_z = 335
#array_size_y = 280
#array_size_x = 750

array_size_z = 335
array_size_y = 280
array_size_x = 750

#========================== plot ============================================

import numpy as np

def make_slices(input_path,file_name,output_path):
    data = np.fromfile(input_path+'/'+file_name,dtype='float32',sep='') 
    data = data.reshape([array_size_z,array_size_y,array_size_x]) 
    
    for i in range(array_size_z/5):
        img = np.mean( [ data[i,:,:],data[i+1,:,:],data[i+2,:,:],data[i+3,:,:],data[i+4,:,:] ], axis = 0 )
        img.tofile(output_path+'/'+'Z_'+file_name+'_'+str(i)+'.img')
        
    for i in range(array_size_y/5):
        img = np.mean( [ data[:,i,:],data[:,i+1,:],data[:,i+2,:],data[:,i+3,:],data[:,i+4,:] ], axis = 0 )
        img.tofile(output_path+'/'+'Y_'+file_name+'_'+str(i)+'.img')
    
    for i in range(array_size_x/5):
        img = np.mean( [ data[:,:,i],data[:,:,i+1],data[:,:,i+2],data[:,:,i+3],data[:,:,i+4] ], axis = 0 )
        img.tofile(output_path+'/'+'X_'+file_name+'_'+str(i)+'.img')
        
    


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
           make_slices(input_path, name, output_path)


  # raw_input() # Wait for user to plot the next plots


if __name__ == "__main__":
   main(sys.argv[1:])
