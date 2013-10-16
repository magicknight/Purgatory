#!/usr/bin/python

# Loop over phantom files, 
# submit projection and reconstruction obs to hpcc, do butterworth filter, after that copy the data to dora
# The lesion position can be random, fix, or read from a file. If read from a file, the location file name must start with the same name as the phantom file.
# python executable

#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################

import string
import os
import subprocess
import time
import random
import numpy as np

####################### definition ##################################

# The object dimensions, used for lesion position
obj_x = 1020
obj_y = 257
obj_z = 323
#obj_x = 750
#obj_y = 280
#obj_z = 335

# The butter worth cut off frequancy 
butter_worth_cutoff_frequency = 0.15

# The object path
object_path = '/project/tomo/zhihua/Simulation/phantom' # 
# The lesion file
lesion_file = '/project/tomo/zhihua/Simulation/lesion/lesion_sphere_42_8mm.obj'
# The lesion position path
lesion_position_path = '/project/tomo/zhihua/Simulation/location'  # 
# The computation result data folder
data_path = '/project/tomo/zhihua/Simulation/data'
# The lession size
lesion_size = 42 - 1 # I assume a cube space with volume 100*100*100 and  with 0 on non-lesion and -1 for lesion
# Destination path(loacal machine)
local_path = '/dora6/zliang/work/image/data'

# Define the parameters that we want to check for simulation

KVpSetting = [30]
MeanGlandularDose = [4]
LowestEnergy = [30]
HighestEnergy = [30]
ProjectionArc = [60]
#TotalViewsToBeProjected = [3,7,11,15,19]
TotalViewsToBeProjected = [19]
LesionForms = [True, False] # need a lesion or not
LesionPositionRandom = False # lesion position is random
LesionPositionFile = True # read lesion position from a file

##################### test ##########################################
#KVpSetting = [28,60]
#MeanGlandularDose = [4,15]
#LowestEnergy = [28, 30, 60]
#HighestEnergy = [28,60]
#ProjectionArc = [60,90]
#TotalViewsToBeProjected = [9, 21]
#LesionForms = [True, False]
#LesionPositionRandom = True

####################### main program ################################
#####################################################################


# Open template projection config file
prj_tmp_path = 'projection_config_template.cfg'
projection_template = open(prj_tmp_path)
rec_tmp_path = 'reconstruction_config_template.cfg'
reconstruction_template = open(rec_tmp_path)
# Open the template job submission file
pro_job_sub_tmp = open('run_projection_template.pbs')
rec_job_sub_tmp = open('run_reconstruction_template.pbs')

# Get current working directory
work_path = os.getcwd()

# Loop over all phantom object files
for root, dirs, files in os.walk(object_path):
    for object_name in files:
        if object_name.endswith('.obj'):
            # get th object label for looking for location file
            object_label = string.split(object_name,'.')[0]

            # Get the object file to detect the edge of breast
            obj_data = np.fromfile(os.path.join(root,object_name), dtype = 'float32')
            obj_data = obj_data.reshape([obj_z,obj_y,obj_x])



# Loop over all the variables
            for kvp in KVpSetting:
                for mgd in MeanGlandularDose:
                    for he in HighestEnergy:
                        for pa in ProjectionArc:
                            for tvp in TotalViewsToBeProjected:
                                for lesion in LesionForms:
                        
                    ######################################################################
                                    # File copying and modification #
                    ######################################################################

                                    # Set target path, if target directory not exist, make it.
                                    target_path = os.path.join(data_path, object_label + '_kvp_' + str(kvp) + '_mgd_' + str(mgd) + '_he_' + str(he) + '_pa_' + str(pa) + '_tvp_' + str(tvp) + '_lesion_' + str(lesion) )
                                    if not os.path.exists(target_path):
                                        os.makedirs(target_path)

                                        # For each projectoin config file:
                                        # Open the target projection config file
                                    projection_config_target = open( os.path.join(target_path,  'projection.cfg'), 'w')
                                        
                                    # Replace the arguments with what i need
                                    for line in projection_template:
                                        if line.startswith('KVpSetting'):
                                            projection_config_target.write('KVpSetting '+str(kvp) + '\n')
                                        elif line.startswith('MeanGlandularDose'):
                                            projection_config_target.write('MeanGlandularDose '+str(mgd) + '\n')
                                        elif line.startswith('LowestEnergy'):
                                            projection_config_target.write('LowestEnergy '+str(he) + '\n') # I set lowest energy equal to highest energy here. 
                                        elif line.startswith('HighestEnergy'):
                                            projection_config_target.write('HighestEnergy '+str(he) + '\n') 
                                        elif line.startswith('ProjectionArc'):
                                            projection_config_target.write('ProjectionArc '+str(pa) + '\n')
                                        elif line.startswith('LastProjectedView'):
                                            projection_config_target.write('LastProjectedView '+str(tvp-1) + '\n') # I set Last projection view as the total views - 1
                                        elif line.startswith('TotalViewsToBeProjected'):
                                            projection_config_target.write('TotalViewsToBeProjected ' + str(tvp) + '\n')
                                        elif line.startswith('LesionFromFile'):
                                            if lesion:
                                                if LesionPositionRandom: # generate a random position
                                                    random.seed()
                                                    while True: # here we detect if the lesion is out of the breast
                                                        p_x = random.randint(0,obj_x-lesion_size-1)
                                                        p_y = random.randint(0,obj_y-lesion_size-1)
                                                        p_z = random.randint(0,obj_z-lesion_size-1)
                                                        if ( obj_data[p_z+lesion_size,p_y,p_x] != 0 and  obj_data[p_z,p_y+lesion_size,p_x] != 0 and  obj_data[p_z,p_y,p_x+lesion_size] != 0 and  obj_data[ p_z, p_y + lesion_size,p_x+lesion_size] != 0 and  obj_data[ p_z+ lesion_size,  p_y, p_x + lesion_size] != 0 and  obj_data[p_z+lesion_size, p_y+lesion_size, p_x] != 0 and  obj_data[p_z + lesion_size, p_y + lesion_size, p_x + lesion_size] != 0):
                                                            break # if the lesion position is accepted, we break the loop of generating random numbers for position
                                                            # write down the cfg file 
                                                        projection_config_target.write('LesionFromFile  ' + str(p_z) + ' '  + str(p_y) + ' ' + str(p_x) + ' ' + str(p_z+lesion_size) + ' ' + str(p_y+lesion_size) + ' '  + str(p_x+lesion_size) + ' '   +'  .2 .2 .2 mm ' + lesion_file+' \n')
                                                elif LesionPositionFile: # if not a random positin for lesion  # if position is in a file, read in position data.
                                                    # Loop over all location files
                                                    for location_root, location_dirs, location_files in os.walk(lesion_position_path):
                                                        for lesion_position_file in location_files:
                                                            if lesion_position_file.startswith(object_label):
                                                                # get th object label for looking for location file
                                                                f = open( os.path.join(location_root,lesion_position_file) ) 
                                                                header = f.readline() # get rid of header
                                                                for each_line in f: # each line contains a lesion
                                                                    x,y,z = [int(p) for p in each_line.split()]
                                                                    projection_config_target.write('LesionFromFile  ' + str(z-lesion_size/2)  + ' ' +  str(y-lesion_size/2)  + ' ' + str(x-lesion_size/2)  + ' ' +  str(z+lesion_size/2) +  ' ' + str(y+lesion_size/2)  + ' ' +  str(x+lesion_size/2)  + '  .2 .2 .2 mm '+ lesion_file+' \n') # -lesion_size/2 is to put the center of lesion to the position
                                                else:
                                                    projection_config_target.write('LesionFromFile  150 80 280 249 179 379  .2 .2 .2 mm '+lesion_file+' \n')
                                            else: # if not need a lesion
                                                projection_config_target.write('# \n')
                                    
                                        elif line.startswith('ObjectMatrixDimensions_X'): # modify the object dimension
                                            projection_config_target.write('ObjectMatrixDimensions_X '+str(obj_x) +'\n')
                                        elif line.startswith('ObjectMatrixDimensions_Y'): # modify the object dimension
                                            projection_config_target.write('ObjectMatrixDimensions_Y '+str(obj_y) +'\n')
                                        elif line.startswith('ObjectMatrixDimensions_Z'): # modify the object dimension
                                            projection_config_target.write('ObjectMatrixDimensions_Z '+str(obj_z) +'\n')
                                        elif line.startswith('HighestObjectIndices_X'): # modify the object dimension
                                                projection_config_target.write('HighestObjectIndices_X '+str(obj_x-1) +'\n')
                                        elif line.startswith('HighestObjectIndices_Y'): # modify the object dimension
                                            projection_config_target.write('HighestObjectIndices_Y '+str(obj_y-1) +'\n')
                                        elif line.startswith('HighestObjectIndices_Z'): # modify the object dimension
                                            projection_config_target.write('HighestObjectIndices_Z '+str(obj_z-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_X'): # modify the object dimension
                                            projection_config_target.write('InputHighestObjectIndices_X '+str(obj_x-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_Y'): # modify the object dimension
                                            projection_config_target.write('InputHighestObjectIndices_Y '+str(obj_y-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_Z'): # modify the object dimension
                                            projection_config_target.write('InputHighestObjectIndices_Z '+str(obj_z-1) +'\n')
                                            
                                        else: # not the line that needs to be modified, copy it without change anything 
                                            projection_config_target.write(line)
                                                
                                                
                                                
                                    # Close target file
                                    projection_config_target.close()
                                    # Set pointer of the template file to beginning
                                    projection_template.seek(0,0)
                    ######################################################################
                    
                                    # For each reconstruction config file:
                                    reconstruction_config_target = open( os.path.join(target_path, 'reconstruction.cfg'), 'w')
                        
                                    # Replace the arguments with what i need
                                    for line in reconstruction_template:
                                        if line.startswith('ProjectionArc'):
                                            reconstruction_config_target.write('ProjectionArc ' + str(pa) + '\n')
                                        elif line.startswith('LastProjectedView'):
                                            reconstruction_config_target.write('LastProjectedView '+str(tvp-1) + '\n') # I set Last projection view as the total views - 1
                                        elif line.startswith('TotalViewsToBeProjected'):
                                            reconstruction_config_target.write('TotalViewsToBeProjected ' + str(tvp) + '\n')
                                            
                                    # modify the object dimensions
                                        elif line.startswith('ObjectMatrixDimensions_X'): # modify the object dimension
                                            reconstruction_config_target.write('ObjectMatrixDimensions_X '+str(obj_x) +'\n')
                                        elif line.startswith('ObjectMatrixDimensions_Y'): # modify the object dimension
                                            reconstruction_config_target.write('ObjectMatrixDimensions_Y '+str(obj_y) +'\n')
                                        elif line.startswith('ObjectMatrixDimensions_Z'): # modify the object dimension
                                            reconstruction_config_target.write('ObjectMatrixDimensions_Z '+str(obj_z) +'\n')
                                        elif line.startswith('HighestObjectIndices_X'): # modify the object dimension
                                            reconstruction_config_target.write('HighestObjectIndices_X '+str(obj_x-1) +'\n')
                                        elif line.startswith('HighestObjectIndices_Y'): # modify the object dimension
                                            reconstruction_config_target.write('HighestObjectIndices_Y '+str(obj_y-1) +'\n')
                                        elif line.startswith('HighestObjectIndices_Z'): # modify the object dimension
                                            reconstruction_config_target.write('HighestObjectIndices_Z '+str(obj_z-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_X'): # modify the object dimension
                                            reconstruction_config_target.write('InputHighestObjectIndices_X '+str(obj_x-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_Y'): # modify the object dimension
                                            reconstruction_config_target.write('InputHighestObjectIndices_Y '+str(obj_y-1) +'\n')
                                        elif line.startswith('InputHighestObjectIndices_Z'): # modify the object dimension
                                            reconstruction_config_target.write('InputHighestObjectIndices_Z '+str(obj_z-1) +'\n')
                                            
                                        else:
                                            reconstruction_config_target.write(line)
                                            
                                    # Close target file
                                    reconstruction_config_target.close()
                                    # Set pointer of the template file to beginning                        
                                    reconstruction_template.seek(0,0)
                    ######################################################################
                    
                                    # Copy and modify the pbs job submit file

                                    # For projection job submission file:
                                    projection_job_submit_target = open( os.path.join(target_path, 'prj_submit.pbs'), 'w')
                    
                                    # Replace the path with current target path
                                    for line in pro_job_sub_tmp:
                                        if line.startswith('cd'):
                                            projection_job_submit_target.write('cd ' + target_path + '\n')
                                        elif line.startswith('./gmsss'):
                                            projection_job_submit_target.write('./gmsss -o ' + os.path.join(root,object_name) + ' -c projection.cfg -s projection.prj -m4 \n')
                                        else:
                                            projection_job_submit_target.write(line)
                                            
                                    # Close target file
                                    projection_job_submit_target.close()
                                    # Set pointer of the template file to beginning                        
                                    pro_job_sub_tmp.seek(0,0)
                    
                    
                                    # For reconstruction job submission file:
                                    reconstruction_job_submit_target = open( os.path.join(target_path, 'rec_submit.pbs'), 'w')
                        
                                    # Replace the path with current target path
                                    for line in rec_job_sub_tmp:
                                        if line.startswith('cd'):
                                            reconstruction_job_submit_target.write('cd ' + target_path + '\n')
                                        else:
                                            reconstruction_job_submit_target.write(line)

                                    # Close target file
                                    reconstruction_job_submit_target.close()
                                    rec_job_sub_tmp.seek(0,0)
                    
                    ######################################################################
                    # Submit projection jobs #
                    ######################################################################
                                    subprocess.call(['cp', 'gmsss', target_path])
                                    subprocess.call(['qsub', '-d', target_path, 'prj_submit.pbs'])

 
# Close the template file
projection_template.close()
reconstruction_template.close()
pro_job_sub_tmp.close()
rec_job_sub_tmp.close()
######################################################################
# Submit reconstruction jobs #
######################################################################       
# Check if all the projection jobs finished, if not, wait 30 seconds
#while subprocess.check_output('qstat').find('Tomo_Prj') > 0: # a new function in python 2.75
#    time.sleep(30.0)
while subprocess.Popen(["qstat"], stdout=subprocess.PIPE).communicate()[0].find('Tomo_Prj') > 0:
    time.sleep(10.0)

# Clean up template files
#subprocess.call(['rm', 'Tomo_Prj.*'])

# Loop over all data path:
for root, dirs, files in os.walk(data_path):
    for directory in dirs:
        if not directory.startswith('data'):
            current_path = os.path.join(root,directory)
            # Copy reconstruction execute file
            subprocess.call(['cp', 'mingle', current_path ])
            # Submit reconstruction jobs
            subprocess.call(['qsub', '-d', current_path, 'rec_submit.pbs'])




######################################################################
# Apply Butter filter to every file  #
######################################################################    
# Check if all the reconstruction jobs finished, if not, wait 10 seconds
#    time.sleep(30.0)
while subprocess.Popen(["qstat"], stdout=subprocess.PIPE).communicate()[0].find('Tomo_Rec') > 0:
    time.sleep(10.0)

butterworth_tmp = open('butterworth.pbs')

# Loop over all data path:
for root, dirs, files in os.walk(data_path):
    for directory in dirs:
        if not directory.startswith('data'):
            current_path = os.path.join(root,directory)
            butter_pbs = open( os.path.join(current_path, 'butterworth.pbs'), 'w')
            # Replace the butterworth pbs with properly arguments.
            for line in butterworth_tmp:
                if line.startswith('./b3dfftw'):
                    butter_pbs.write('./b3dfftw reconstruction.rec b3d_reconstruction.rec  ' + ' -f ' + str(butter_worth_cutoff_frequency) +  ' -x '+ str(obj_x) +  ' -y ' + str(obj_y) +  ' -z ' + str(obj_z) +  ' \n')
                else:
                    butter_pbs.write(line)
            butter_pbs.close()
            # get the pointer of template file to the begginning
            butterworth_tmp.seek(0,0)
            # Submit butterfilter jobs                
            subprocess.call(['cp', 'b3dfftw', current_path])
            subprocess.call(['qsub', '-d', current_path, 'butterworth.pbs'])

butterworth_tmp.close()

######################################################################
# Copy every file to dora #
######################################################################    
# Check if all the butterworth filter jobs finished, if not, wait 10 seconds
#while subprocess.check_output('qstat').find('Tomo_Prj') > 0: # a new function in python 2.75
#    time.sleep(30.0)
while subprocess.Popen(["qstat"], stdout=subprocess.PIPE).communicate()[0].find('Tomo_BWF') > 0:
    time.sleep(10.0)
    
for root, dirs, files in os.walk(data_path):
    for name in files:
        if name.endswith('.rec') and name.startswith('b3d'):
            remote_name = root.split('/')[-1] # Get the directory name for remote rename the data file
            subprocess.call(['scp',  os.path.join(root,name), 'zliang@172.27.9.141:'+ os.path.join(local_path, remote_name+'_b3d.rec')])


######################################################################
# All done  #
######################################################################    


#sftp.close()
#ssh.close()            
