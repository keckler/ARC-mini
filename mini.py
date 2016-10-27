#!/usr/bin/python

############################################################################
#creates a new folder for the job, moves into the folder, submits a batch job
############################################################################

#####
#imports
#####

from os import chdir
from os import getcwd
from os import listdir
from os import mkdir
from os import getcwd
from shutil import copy
from shutil import copyfile
from subprocess import Popen
from sys import argv

#####
#variables
#####

runDir = getcwd() #directory that mini is being run from
miniDir = '/global/home/users/ckeckler/docs/mini/ARC-mini' #directory that all mini shit is stored
miniExe = '~/bin/mini-5.1/mini-5.1-Linux.x'
input = str(argv[-1])
output = 'mini.out'

if input[0:1] == '/': #it is the full path, do nothing
    pass
else:
    input = runDir+'/'+input

#####
#create new run folder
#####

#make a 'run' folder if not already existing
files = listdir(miniDir)
if 'runs' in files:
    chdir(miniDir+'/runs')
else:
    mkdir(miniDir+'/runs')
    chdir(miniDir+'/runs')

#make a new incrimented folder for the input/output of run
i = 1
runFolderFlag = 0
while runFolderFlag == 0:
    try:
        mkdir(str(i))
        runFolderFlag = 1
    except OSError:
        i += 1

#move into the incriment folder
chdir(str(i))

#copy mini input into incriment folder
copy(input, './')

#####
#alter the slurm script in the ~/mini directory, 'mini_tmp.sub'
#####

#copy over the template submission script
copyfile(miniDir+'/mini_tmp.sub', miniDir+'/runs/'+str(i)+'/mini.sub')
fb = open(miniDir+'/runs/'+str(i)+'/mini.sub', 'a') #new batch file

#add command lines to execute mini and plot results
fb.write(miniExe+' < '+input+' > '+output+'\n')
fb.write(miniDir+'/extractSAS.py '+output)

fb.close()

#####
#submit the job
#####

Popen(['sbatch', 'mini.sub'])
