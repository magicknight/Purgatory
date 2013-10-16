#!/usr/bin/python

# copy data from  hpcc to local machine
# python executable

#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################
#  Written by Zhihua Liang 2013
#  zliang5@central.uh.edu
#####################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#####################################################################

import string as s
import os
import subprocess
#import paramiko

#ssh = paramiko.SSHClient() 
#ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
#ssh.connect('172.27.9.141', username='zliang', password='Leukemia2009')
#sftp = ssh.open_sftp()
#remotepath = '/dora6/zliang/work/image/data/'

for root, dirs, files in os.walk('data'):
#    use the directory name as the destination file name.    
    remote_name = s.split(root,'/')[-1]
#    print remote_name
#    print root
    for name in files:
#        if name.endswith('.prj'):
#        subprocess.call(['rm',root+'/saftramp.out'])
#        subprocess.call(['rm',root+'/projection_sarlo.prj'])

        # sftp.put(root+name, remotepath)
        #            print 'copying', root+'/'+name
#        print name
#        print root
#        print dirs
        print 'copying', remote_name
        if name.endswith('.rec'):
            subprocess.call(['scp', '-r', root+'/'+name, 'zliang@172.27.9.141:~/work/image/data/'+remote_name+'.rec'])

#sftp.close()
#ssh.close()            
