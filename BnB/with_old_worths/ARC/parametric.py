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

transients = ['ULOF'] #names of transients to run
worths = [2.00] #total worths of ARC systems, $
actuationTemps = [0] #temperature above SS of actuation of ARC system, C
actuationSpans = [12.5]

miniExe = '~/bin/mini-5.2/mini-5.x-Linux-2742M.x'

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
                inpPath = str(argv[i])
                newPath = './'+transient+'_'+str(worth)+'_'+str(temp)+'.inp'
                fi = open(inpPath, 'r')
                fin = open(newPath, 'w')
                for line in fi:
                    if line[:26] == '   18    8   17    1      ': #if its line with worth
                        fin.write('   18    8   17    1      '+str(worth)+'\n')
                    elif line[:32] == '  6001     5         0.0        ': #if its line with temp table
                        fin.write('  6001     5         0.0'+"{0:>12.1f}".format(temp)+"{0:>12.1f}".format(temp+(span/18*2))+"{0:>12.1f}".format(temp+(span/18*3))+"{0:>12.1f}".format(temp+(span/18*4))+'\n')
                    elif line[:12] == '  6006     5':
                        fin.write('  6006     5'+"{0:>12.1f}".format(temp+(span/18*5))+"{0:>12.1f}".format(temp+(span/18*6))+"{0:>12.1f}".format(temp+(span/18*7))+"{0:>12.1f}".format(temp+(span/18*8))+"{0:>12.1f}".format(temp+(span/18*9))+'\n')
                    elif line[:12] == '  6011     5':
                        fin.write('  6011     5'+"{0:>12.1f}".format(temp+(span/18*10))+"{0:>12.1f}".format(temp+(span/18*11))+"{0:>12.1f}".format(temp+(span/18*12))+"{0:>12.1f}".format(temp+(span/18*13))+"{0:>12.1f}".format(temp+(span/18*14))+'\n')
                    elif line[:12] == '  6016     5':
                        fin.write('  6016     5'+"{0:>12.1f}".format(temp+(span/18*15))+"{0:>12.1f}".format(temp+(span/18*16))+"{0:>12.1f}".format(temp+(span/18*17))+"{0:>12.1f}".format(temp+(span/18*18))+' '+str(10000)+'\n')
                    else: #else just copy it over
                        fin.write(line)
                fi.close()
                fin.close()
    
                #copy over slurm script and add commands at end
                copyfile('/global/home/users/ckeckler/docs/ARC-mini/mini_tmp.sub', './mini.sub')
                fb = open('./mini.sub', 'a')
                fb.write(miniExe+' < '+newPath+' > mini.out\n')
                fb.write('/global/home/users/ckeckler/docs/ARC-mini/csvPlot.py')
                fb.close()
    
                #run it
                Popen(['sbatch', 'mini.sub'])
    
                #remove excess files to preserve memory
                completedFlag = 0
                while completedFlag == 0: #if /flag.txt is available to be deleted, the first channel has been plotted -- move on
                    try:
                        remove('./flag.txt')
                        completedFlag = 1
                    except OSError:
                        sleep(10)
                
                sleep(80) #give time for the other channels to be printed before moving on to next job
                remove('./RESTART.dat')
                remove('./PRIMAR4.dat')
                remove('./CHANNEL.dat')
                #remove('./mini.out')
                #remove('./primar4.csv')
                #remove('./Channel000001.csv')
                #remove('./Channel000002.csv')
                #remove('./Channel000003.csv')
                #remove('./Channel000004.csv')
                #remove('./WholeCore.csv')
                    
                chdir('../../../../') #move out of there
