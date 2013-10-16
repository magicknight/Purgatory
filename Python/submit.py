#!/usr/bin/python

# submit jobs to hpcc
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

# The object dimensions, used for lesion position
obj_x = 750
obj_y = 280
obj_z = 335
# The lesion file name
lesion_file_name = 'lesion_sphere_100.obj'
# The lession size
lesion_size = 100 - 1 # I assume a cube space with volume 100*100*100 and  with 0 on non-lesion and -1 for lesion
# The object file name
object_file_name = 'bcx51R_x750_y280_z335_fuzzy1.obj'

####################### definition ##################################
# Define the parameters that we want to check for simulation

#KVpSetting = [28, 30, 60]
#MeanGlandularDose = [4, 15]
##LowestEnergy = [28, 30, 60]
#HighestEnergy = [28, 30, 60]
#ProjectionArc = [30, 60, 90]
#TotalViewsToBeProjected = [3, 11, 21]
#Lesion = [True, False]
#LesionForms = [True, False] # need a lesion from file or not
#LesionRandom = True # lesion position is random

##################### test ##########################################
KVpSetting = [28,60]
MeanGlandularDose = [4,15]
#LowestEnergy = [28, 30, 60]
HighestEnergy = [28,60]
ProjectionArc = [60,90]
TotalViewsToBeProjected = [9, 21]
LesionForms = [True, False]
LesionPositionRandom = True

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
# Get the object file to detect the edge of breast
data = np.fromfile(work_path+'/'+object_file_name, dtype = 'float32')
data = data.reshape([obj_z,obj_y,obj_x])

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
                        target_path = 'data/kvp_' + str(kvp) + '_mgd_' + str(mgd) + '_he_' + str(he) + '_pa_' + str(pa) + '_tvp_' + str(tvp) + '_lesion_' + str(lesion)
                        if not os.path.exists(target_path):
                            os.makedirs(target_path)

                        # For each projectoin config file:
                        # Open the target projection config file
                        projection_config_target = open(target_path + '/projection.cfg', 'w')
                            
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
                                          #  if ( (p_x + lesion_size) < obj_x and (p_y + lesion_size) < obj_y and (p_z + lesion_size) < obj_z ):
                                            if ( data[p_z+lesion_size,p_y,p_x] != 0 and data[p_z,p_y+lesion_size,p_x] != 0 and data[p_z,p_y,p_x+lesion_size] != 0 and data[ p_z, p_y + lesion_size,p_x+lesion_size] != 0 and data[ p_z+ lesion_size,  p_y, p_x + lesion_size] != 0 and data[p_z+lesion_size, p_y+lesion_size, p_x] != 0 and data[p_z + lesion_size, p_y + lesion_size, p_x + lesion_size] != 0):
                                                break # if the lesion position is accepted, we break the loop of generating random numbers for position
                                        # write down the cfg file 
                                        projection_config_target.write('LesionFromFile  ' + str(p_z) + ' '  + str(p_y) + ' ' + str(p_x) + ' ' + str(p_z+lesion_size) + ' ' + str(p_y+lesion_size) + ' '  + str(p_x+lesion_size) + ' '   +'  .2 .2 .2 mm '+ work_path +'/'+lesion_file_name+' \n')
                                    else:
                                        projection_config_target.write('LesionFromFile  150 80 280 249 179 379  .2 .2 .2 mm '+ work_path +'/'+lesion_file_name+' \n')
                                else:
                                    projection_config_target.write('# \n')
                            else:
                                projection_config_target.write(line)
                                
                                    

                        # Close target file
                        projection_config_target.close()
                        # Set pointer of the template file to beginning
                        projection_template.seek(0,0)
                    ######################################################################
                    
                    # For each reconstruction config file:
                        reconstruction_config_target = open( target_path + '/reconstruction.cfg', 'w')
                        
                    # Replace the arguments with what i need
                        for line in reconstruction_template:
                            if line.startswith('ProjectionArc'):
                                reconstruction_config_target.write('ProjectionArc ' + str(pa) + '\n')
                            elif line.startswith('LastProjectedView'):
                                reconstruction_config_target.write('LastProjectedView '+str(tvp-1) + '\n') # I set Last projection view as the total views - 1
                            elif line.startswith('TotalViewsToBeProjected'):
                                reconstruction_config_target.write('TotalViewsToBeProjected ' + str(tvp) + '\n')
                            else:
                                reconstruction_config_target.write(line)
                            
                        # Close target file
                        reconstruction_config_target.close()
                        # Set pointer of the template file to beginning                        
                        reconstruction_template.seek(0,0)
                    ######################################################################
                    
                        # Copy and modify the pbs job submit file
                    
                        # For projection job submission file:
                        projection_job_submit_target = open( target_path + '/prj_submit.pbs', 'w')
                    
                        # Replace the path with current target path
                        for line in pro_job_sub_tmp:
                            if line.startswith('cd'):
                                projection_job_submit_target.write('cd ' + work_path + '/' + str(target_path) + '\n')
                            elif line.startswith('./gmsss'):
                                projection_job_submit_target.write('./gmsss -o ' + work_path + '/' + 'bcx51R_x750_y280_z335_fuzzy1.obj -c projection.cfg -s projection.prj -m4 \n')
                            else:
                                projection_job_submit_target.write(line)

                        # Close target file
                        projection_job_submit_target.close()
                        # Set pointer of the template file to beginning                        
                        pro_job_sub_tmp.seek(0,0)
                    
                    
                        # For reconstruction job submission file:
                        reconstruction_job_submit_target = open( target_path + '/rec_submit.pbs', 'w')
                        
                        # Replace the path with current target path
                        for line in rec_job_sub_tmp:
                            if line.startswith('cd'):
                                reconstruction_job_submit_target.write('cd ' + work_path + '/' + str(target_path) + '\n')
                            else:
                                reconstruction_job_submit_target.write(line)

                        # Close target file
                        reconstruction_job_submit_target.close()
                        rec_job_sub_tmp.seek(0,0)
                    
                    ######################################################################
                    # Submit projection jobs #
                    ######################################################################
                        subprocess.call(['cp', 'gmsss', str(target_path)])
                        subprocess.call(['qsub', str(target_path) + '/prj_submit.pbs'])
                    
 
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

# For each projection job:
for kvp in KVpSetting:
    for mgd in MeanGlandularDose:
        for he in HighestEnergy:
            for pa in ProjectionArc:
                for tvp in TotalViewsToBeProjected:
                    for lesion in LesionForms:
                        target_path = 'data/kvp_' + str(kvp) + '_mgd_' + str(mgd) + '_he_' + str(he) + '_pa_' + str(pa) + '_tvp_' + str(tvp) + '_lesion_' + str(lesion)
                        # Copy reconstruction execute file
                        subprocess.call(['cp', 'mingle', str(target_path)])
                        # Submit reconstruction jobs
                        subprocess.call(['qsub', str(target_path) + '/rec_submit.pbs'])

######################################################################
# All done  #
######################################################################    
# Close the template file
projection_template.close()
reconstruction_template.close()
pro_job_sub_tmp.close()
rec_job_sub_tmp.close()


