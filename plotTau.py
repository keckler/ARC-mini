#!/usr/bin/python

#-------------------------------------------------------------------------------
#run from command line using './plotTau output_file_name'
#extracts tau value and results from lag compensator (i.e. ARC reservoir temp, 
#outlet temp, flow) and plots over course of transient
#-------------------------------------------------------------------------------

#####
#user input
#####

matlabExe = '/Applications/MATLAB_R2016b.app/bin/matlab' #for running locally
#matlabExe = 'matlab' #for running on savio


#####
#imports
#####

from os import remove
from subprocess import Popen
from sys import argv


#####
#initialize stuff
#####

time = [] #time [s]
flow = [] #normalized flowrate
tau = [] #normalized variable time lag parameter [s]
reservoirTemp = [] #lag-compensator calculated reservoir temp [C]
outletTemp = [] #outlet temp of channel [C]


#####
#do extraction
#####

outputFile = str(argv[-1])

fo = open(outputFile, 'r')

for line in fo:
    numWordsPerLine = len(line.split())
    if numWordsPerLine == 0:
        pass
    elif numWordsPerLine == 4:
        if line.split()[1] == 'CTLSUB': #it is the CTLSUB block
            nextLine = fo.next()
            nextLine = fo.next()
            nextLine = fo.next()
            time.append(float(nextLine.split()[9][0:10])*10**float(nextLine.split()[9][-2:]))
            for i in range(1,23):
                nextLine = fo.next()
            flow.append(float(nextLine.split()[-1][0:10])*10**float(nextLine.split()[-1][-3:]))
            nextLine = fo.next()
            tau.append(float(nextLine.split()[-1][0:10])*10**float(nextLine.split()[-1][-3:]))
            nextLine = fo.next()
            nextLine = fo.next()
            reservoirTemp.append(float(nextLine.split()[-1][0:10])*10**float(nextLine.split()[-1][-3:]) - 273)
            outletTemp.append(float(nextLine.split()[5][0:10])*10**float(nextLine.split()[5][-3:]) - 273)
    else:
        pass

fo.close()

#remove null transient values
del time[0:2]
del flow[0:2]
del tau[0:2]
del reservoirTemp[0:2]
del outletTemp[0:2]


#####
#print to temporary file
#####

fr = open('results.txt', 'w')

for i in range(0,len(time)):
    fr.write(str(time[i])+' '+str(flow[i])+' '+str(tau[i])+' '+str(reservoirTemp[i])+' '+str(outletTemp[i])+'\n')

fr.close()


#####
#plot
#####

matlabCommands = ["table=readtable('./results.txt','Delimiter','space');"
                  "array=table2array(table);"
                  "time=array(:,1);"
                  "flow=array(:,2);"
                  "tau=array(:,3);"
                  "reservoirTemp=array(:,4);"
                  "outletTemp=array(:,5);"
                  "fig=axes();"
                  "xlabel('time,(s)');"
                  "yyaxis(fig,'left');"
                  "plot(time,flow,'-',time,tau,'--');"
                  "ylabel('normalizedFlow/normalizedTau');"
                  "yyaxis(fig,'right');"
                  "plot(time,reservoirTemp,'-',time,outletTemp,'--');"
                  "ylabel('temperature,(C)');"
                  "grid(fig,'on');"
                  "legend('normalizedFlow','normalizedTau','reservoirTemp','outletTemp');"
                  "print('tauPlot','-dtiff');"
                  "savefig('tauPlot');"
                  "quit;"]

matlabCommand = ''
for command in matlabCommands:
    matlabCommand = matlabCommand+command

plotRun = Popen([matlabExe, '-nodesktop', '-nosplash', '-nodisplay', '-r', matlabCommand])
plotRun.wait()


#####
#clean up
#####

remove('./results.txt')