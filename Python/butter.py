#!/usr/bin/python

# submit jobs to hpcc, do butterworth filter, after that copy the data to dora
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
# For each reconstruction job:
for kvp in KVpSetting:
    for mgd in MeanGlandularDose:
        for he in HighestEnergy:
            for pa in ProjectionArc:
                for tvp in TotalViewsToBeProjected:
                    for lesion in LesionForms:
                        target_path = 'data/kvp_' + str(kvp) + '_mgd_' + str(mgd) + '_he_' + str(he) + '_pa_' + str(pa) + '_tvp_' + str(tvp) + '_lesion_' + str(lesion)
                        # Submit butterfilter jobs
                        subprocess.call(['cp', 'butterworth.pbs', str(target_path)])
                        subprocess.call(['cp', 'b3dfftw', str(target_path)])
                        subprocess.call(['qsub', '-d', str(target_path), 'butterworth.pbs'])


