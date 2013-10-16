#!/usr/bin/python

# read data from a 3D gray data array then make slice images from 3 different directions
# images are 2D data, average from each 5 slices from each direction. this one makes png images
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

array_size_z = 323
array_size_y = 257
array_size_x = 1020
lesion_position_path = 'location'
#========================== plot ============================================

import numpy as np
from matplotlib import pyplot as plt
import sys, getopt, os, string


plt.gray()

def make_slices(input_path,file_name,output_path):
    data = np.fromfile(os.path.join(input_path,file_name), dtype='float32') 
    data = data.reshape([array_size_z,array_size_y,array_size_x]) 

    # get th object label for looking for location file
    object_label = string.split(file_name,'_kvp')[0] # since reconstruction file contains parameters info such as kvp... we need to seperate from kvp to get the object phantom name as the file label.
    
    
    # Loop over all location files
    for location_root, location_dirs, location_files in os.walk(lesion_position_path):
        for lesion_position_file in location_files:
            if lesion_position_file.startswith(object_label):
                position = np.genfromtxt(os.path.join(location_root,lesion_position_file), skip_header = 1, dtype = np.int) # get position information from location file, position is a numpy array
                    
    # Right now I do images on the y direction
    for i in range(len(position)): # totally 8 locations
        plt.imshow( np.fliplr(data[ :,257-position[i,1],: ]) )
        plt.suptitle(string.split(file_name,'.')[0] + '_' + 'x' + str(position[i,0]) + '_' + 'z'+ str(position[i,2]), y = 0.7, fontsize = 8 )
        plt.savefig( os.path.join(output_path, string.split(file_name,'.')[0] + '_' + 'x' + str(position[i,0]) + '_' + 'z'+ str(position[i,2]) +  '_.png'), dpi = 200, transparent=True, bbox_inches='tight')
        plt.clf()

###################################################################### commented lines ######################################################################        
#    for i in range(array_size_y/5):
#        img = np.mean( [ data[:,i,:],data[:,i+1,:],data[:,i+2,:],data[:,i+3,:],data[:,i+4,:] ], axis = 0 )
#        # img.tofile(output_path+'/'+'Y_'+file_name+'_'+str(i)+'.img')
#        plt.imshow(img)
#        plt.savefig(output_path+'/'+'Y_'+file_name+'_'+str(i)+'.png',bbox_inches=0)
   
    
#    for i in range(array_size_x/5):
#        img = np.mean( [ data[:,:,i],data[:,:,i+1],data[:,:,i+2],data[:,:,i+3],data[:,:,i+4] ], axis = 0 )
#        # img.tofile(output_path+'/'+'X_'+file_name+'_'+str(i)+'.img')
#        plt.imshow(img)
#        plt.savefig(output_path+'/'+'X_'+file_name+'_'+str(i)+'.png',bbox_inches=0)
###################################################################### commented lines ######################################################################        
   
        
    


#========================== main program ============================================


def main(argv):

# Parse command-line arguments
   input_path = ''
   output_path = ''
   try:
      opts, args = getopt.getopt(argv,'hi:o:',['ipath=','opath='])
   except getopt.GetoptError:
      print 'png_slices.py -i <input_path> -o <output_path>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'png_slices.py -i <input_path> -o <output_path>'
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
