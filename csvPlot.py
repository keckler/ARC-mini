#!/usr/bin/python

################################################################################
#uses the executables provided by ANL to convert CHANNEL.dat and PRIMAR4.dat
#files into .csv files. then imports .csv files into matlab and plots results
#in nice plots
################################################################################

#####
#imports
#####

from matlabPlotCommands_csv import matlabPlotCommands_csv
from subprocess import PIPE
from subprocess import Popen

#####
#variables
#####

channelCSVs = ['Channel000001.csv','Channel000002.csv','Channel000003.csv','Channel000004.csv','Channel000005.csv','Channel000006.csv','Channel000007.csv'] #list of channel csv filenames to be plotted
channelScript = '/global/home/users/ckeckler/codes/mini-5.1/plot/CHANNELtoCSV-Linux.x' #full path of script to convert CHANNEL.dat to .csv files
primarScript = '/global/home/users/ckeckler/codes/mini-5.1/plot/PRIMAR4toCSV-Linux.x' #full path of script to convert PRIMAR4.dat to .csv file
matlabExe = 'matlab' #for running on Savio

#####
#do stuff
#####

myinput = open('CHANNEL.dat')
channelConversion = Popen([channelScript], stdin=myinput)
channelConversion.wait()

myinput = open('PRIMAR4.dat')
myoutput = open('primar4.csv','w')
primarConversion = Popen([primarScript], stdin=myinput, stdout=myoutput)
primarConversion.wait()


for channelCSV in channelCSVs:

    command = matlabPlotCommands_csv(channelCSV, matlabExe)

    plotRun = Popen(command)
    plotRun.wait()

