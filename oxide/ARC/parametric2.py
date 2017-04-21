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
worths = [0.12, 0.25, 0.37, 0.50, 0.62, 0.75, 0.87, 1.00] #total worths of ARC systems, $
actuationTemps = [5, 10, 15, 20, 25, 30, 35, 40] #temperature above SS of actuation of ARC system, C. actuation span is kept constant at 65 C
actuationSpans = [75.0]#, 95, 105, 115]

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
                        fin.write('  6001     5         0.0'+"{0:12.1f}".format(temp)+"{0:12.1f}".format(temp+(span/18*2))+"{0:12.1f}".format(temp+(span/18*3))+"{0:12.1f}".format(temp+(span/18*4))+'\n')
                    elif line[:12] == '  6006     5':
                        fin.write('  6006     5'+"{0:12.1f}".format(temp+(span/18*5))+"{0:12.1f}".format(temp+(span/18*6))+"{0:12.1f}".format(temp+(span/18*7))+"{0:12.1f}".format(temp+(span/18*8))+"{0:12.1f}".format(temp+(span/18*9))+'\n')
                    elif line[:12] == '  6011     5':
                        fin.write('  6011     5'+"{0:12.1f}".format(temp+(span/18*10))+"{0:12.1f}".format(temp+(span/18*11))+"{0:12.1f}".format(temp+(span/18*12))+"{0:12.1f}".format(temp+(span/18*13))+"{0:12.1f}".format(temp+(span/18*14))+'\n')
                    elif line[:12] == '  6016     5':
                        fin.write('  6016     5'+"{0:12.1f}".format(temp+(span/18*15))+"{0:12.1f}".format(temp+(span/18*16))+"{0:12.1f}".format(temp+(span/18*17))+"{0:12.1f}".format(temp+(span/18*18))+' '+str(10000)+'\n')
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
                sleep(240)
    
                #remove excess files to preserve memory
                completedFlag = 0
                while completedFlag == 0: #if /globalPlots is available to be delted, the job is done and delete everything
                    try:
                        rmtree('./globalPlots')
                        completedFlag = 1
                    except OSError:
                        sleep(60)
                
                remove('./RESTART.dat')
                remove('./PRIMAR4.dat')
                remove('./CHANNEL.dat')
    
                chdir('../../../../') #move out of there
