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
worths = [0.12, 0.25, 0.37, 0.50, 0.62, 0.75, 0.87, 1.00] #total worths of ARC systems, $
actuationTemps = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] #temperature above SS of actuation of ARC system, C. actuation span is kept constant at 65 C
actuationSpans = [75, 85, 95, 105, 115]

miniExe = '~/bin/mini-5.2/mini-5.x-2522-Linux.x'

#####
#imports
#####

from os import chdir
from os import getcwd
from os import mkdir
from os import remove
from shutil import copyfile
from shutil import rmtree
from subprocess import Popen
from sys import argv
from time import sleep

#####
#do stuff
#####

runDir = getcwd()+'/'

#loop through all different variations
for span in actuationSpans:
    maxFile = runDir+str(span)+'/max.txt'
    asymptoticFile = runDir+str(span)+'/asymptotic.txt'

    mkdir('./'+str(span))

    i = 0
    for transient in transients:
        #write header in results file
        fm = open(maxFile, 'a')
        fm.write('transient = '+transient+'\n')
        fm.close()
    
        fa = open(asymptoticFile, 'a')
        fa.write('transient = '+transient+'\n')
        fa.close()
    
        mkdir('./'+str(span)+'/'+transient)
        i += 1
        for worth in worths:
            #write subheader in results file
            fm = open(maxFile, 'a')
            fm.write('worth = '+str(worth)+'\n')
            fm.close()
            
            fa = open(asymptoticFile, 'a')
            fa.write('worth = '+str(worth)+'\n')
            fa.close()
    
            mkdir('./'+str(span)+'/'+transient+'/'+str(worth))
            for temp in actuationTemps:
                mkdir('./'+str(span)+'/'+transient+'/'+str(worth)+'/'+str(temp)) #make directory for run
                chdir('./'+str(span)+'/'+transient+'/'+str(worth)+'/'+str(temp)) #move into directory
    
                #make new mini input from respective template
                inpPath = runDir+str(argv[i])
                newPath = './'+transient+'_'+str(worth)+'_'+str(temp)+'.inp'
                fi = open(inpPath, 'r')
                fin = open(newPath, 'w')
                for line in fi:
                    if line[:26] == '   18    8   17    1      ': #if its line with worth
                        fin.write('   18    8   17    1      '+str(worth)+'\n')
                    elif line[:32] == '  6001     5         0.0        ': #if its line with temp table
                        fin.write('  6001     5         0.0          '+str(temp)+'          '+str(temp+(span/13*2))+'          '+str(temp+(span/13*3))+'          '+str(temp+(span/13*4))+'\n')
                    elif line[:12] == '  6006     5':
                        fin.write('  6006     5          '+str(temp+(span/13*5))+'          '+str(temp+(span/13*6))+'          '+str(temp+(span/13*7))+'          '+str(temp+(span/13*8))+'          '+str(temp+(span/13*9))+'\n')
                    elif line[:12] == '  6011     5':
                        fin.write('  6011     5          '+str(temp+(span/13*10))+'          '+str(temp+(span/13*11))+'         '+str(temp+(span/13*12))+'         '+str(temp+(span/13*13))+'      '+str(10000)+'\n')
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
    
                #pause to wait for job to finish so that memory limits are not exceeded
                sleep(300)
    
                #remove excess files to preserver memory
                remove('./RESTART.dat')
                remove('./PRIMAR4.dat')
                remove('./CHANNEL.dat')
                rmtree('./globalPlots')
    
                chdir('../../../../') #move out of there
