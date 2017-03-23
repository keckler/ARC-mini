#!/usr/bin/python

#-------------------------------------------------------------------------------
#runs many cases of transients with different values for total ARC worth
#and different actuation temperatures. 
#runs the SAS inputs in the typical way that ./mini.py does.
#creates a new folder for each of the variants
#
#run by typing './parametric.py ULOHS_inp_path UTOP_inp_path ULOF_inp_path'
#where the paths are relevant paths to templates for the respective transients
#-------------------------------------------------------------------------------

#####
#inputs
#####

transients = ['ULOHS', 'UTOP', 'ULOF'] #names of transients to run
worths = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50] #total worths of ARC systems, $
actuationTemps = [10, 20, 30, 40, 50] #temperature above SS of actuation of ARC system, C. actuation span is kept constant at 65 C

miniExe = '~/bin/mini-5.2/mini-5.x-2522-Linux.x'

#####
#imports
#####

from os import chdir
from os import getcwd
from os import mkdir
from shutil import copyfile
from subprocess import Popen
from sys import argv
from time import sleep

#####
#do stuff
#####

runDir = getcwd()+'/'

#loop through all different variations
i = 0
for transient in transients:
    #write header in results file
    fr = open('~/docs/mini/ARC-mini/oxide/ARC/results.txt', 'a')
    fr.write('transient = '+transient+'\n')
    fr.close()

    mkdir('./'+transient)
    i += 1
    for worth in worths:
        #write subheader in results file
        fr = open('~/docs/mini/ARC-mini/oxide/ARC/results.txt', 'a')
        fr.write('worth = '+str(worth)+'\n')
        fr.close()

        mkdir('./'+transient+'/'+str(worth))
        for temp in actuationTemps:
            mkdir('./'+transient+'/'+str(worth)+'/'+str(temp)) #make directory for fun
            chdir('./'+transient+'/'+str(worth)+'/'+str(temp)) #move into directory

            #make new mini input from respective template
            inpPath = runDir+str(argv[i])
            newPath = './'+transient+'_'+str(worth)+'_'+str(temp)+'.inp'
            fi = open(inpPath, 'r')
            fin = open(newPath, 'w')
            for line in fi:
                if line[:26] == '   18    8   17    1      ': #if its line with worth
                    fin.write('   18    8   17    1      '+str(worth)+'\n')
                elif line[:32] == '  6001     5         0.0        ': #if its line with temp table
                    fin.write('  6001     5         0.0          '+str(temp)+'          '+str(temp+10)+'          '+str(temp+15)+'          '+str(temp+20)+'\n')
                elif line[:12] == '  6006     5':
                    fin.write('  6006     5          '+str(temp+25)+'          '+str(temp+30)+'          '+str(temp+35)+'          '+str(temp+40)+'          '+str(temp+45)+'\n')
                elif line[:12] == '  6011     5':
                    fin.write('  6011     5          '+str(temp+50)+'          '+str(temp+55)+'         '+str(temp+60)+'         '+str(temp+65)+'      '+str(10000)+'\n')
                else: #else just copy it over
                    fin.write(line)
            fi.close()
            fin.close()

            #copy over slurm script and add commands at end
            copyfile('/global/home/users/ckeckler/docs/mini/ARC-mini/mini_tmp.sub', './mini.sub')
            fb = open('./mini.sub', 'a')
            fb.write(miniExe+' < '+newPath+' > mini.out\n')
            fb.write('/global/home/users/ckeckler/docs/mini/ARC-mini/extractSAS.py mini.out')
            fb.close()

            #run it
            Popen(['sbatch', 'mini.sub'])

            #pause so that memory limits are not exceeded
            sleep(150)

            chdir('../../../') #move out of there