#!/usr/bin/python

#-------------------------------------------------------------------------------
#run from the command line using './extractSAS output_file_name'
#extracts the reactivity components, temperatures, power, flow, etc for each printed 
#timestep. uses matlab to plot data in peak channel. 
#user is required to input which is the peak channel.
#-------------------------------------------------------------------------------

#####
#user input
#####

channelNums = [1,2,3,4] #channel numbers of to be plotted
rhoLimits = '[]' #range of reactivity to be plotted, ($), no spaces allowed, leave as '[]' if you want code to decide
shortTimeLimit = 500 #range of time to be plotted in short time scale plots, (s)
IHXintermediateSide = 13 #element number of intermediate side of IHX (tube side)
IHXpump = 2 #element number of intermediate pump
precursorDecayConstants = [1.3377E-2, 3.1026E-2, 1.1763E-1, 3.0917E-1, 8.8605E-1, 2.9416E0]
topOfActiveCore = '1.06680' #string with height of top of active core. enter exactly as printed in SAS output
#matlabExe = '/Applications/MATLAB_R2014b.app/bin/matlab' #for running locally
matlabExe = 'matlab' #for running on savio


#####
#imports
#####

from os import chdir
from os import getcwd
from os import mkdir
from subprocess import Popen
from sys import argv

from matlabPlotCommands import matlabPlotCommands
import modules


#####
#do extraction for each channel
#####

#make folders for global plots (power, rho, precursors)
mkdir('globalPlots')
mkdir('globalFigs')

for channel in channelNums:

    print('channel '+str(channel)+' extraction:\n')

    #####
    #initialize stuff
    #####
    
    print('initializing stuff...\n')
    
    #reactivity parameters
    rhoStep = []
    rhoTime = [] #[s]
    power = [] #normalized
    decayPower = [] #fraction of normalized total power
    fissionPower = [] #fraction of normalized total power
    netReactivity = [] #[$]
    CRDL = [] #[$]
    radExpansion = [] #[$]
    doppler = [] #[$]
    fuelAxialExpansion = [] #[$]
    cladAxialExpansion = [] #[$]
    coolant = [] #[$]
    structureAxialExpansion = [] #[$]
    controlSystem = [] #[$]
    
    #primary loop parameters
    tempStep = [] #time steps in temperature table
    tempTime = [] #times in temperature tables [s]
    saturation = [] #[K]
    fuelPeak = [] #[K]
    cladPeak = [] #[K]
    coolantPeak = [] #[K]
    flowRate = [] #normalized
    coolantInlet = [] #[K]
    coolantOutlet = [] #[K]
    fuelAve = [] #[K]
    cladAve = [] #[K]
    topActiveCoreTemp = [] #[K]
    
    #intermediate loop parameters
    IHXintermediateInlet = [] #[K]
    IHXintermediateOutlet = [] #[K]
    IHXflow = [] #[normalized]
    
    #delayed neutron precursor decay rates
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    group5 = []
    group6 = []
    
    #put all entries into tables
    rhoTab = [rhoStep, rhoTime, power, decayPower, fissionPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem]
    primaryTab = [tempStep, tempTime, saturation, fuelPeak, cladPeak, coolantPeak, flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve, topActiveCoreTemp]
    intermediateTab = [tempStep, tempTime, IHXintermediateInlet, IHXintermediateOutlet, IHXflow]
    precursorTab = [tempTime, group1, group2, group3, group4, group5, group6]
    
    
    #####
    #open file and read
    #####
    
    print('reading from SAS output file...\n')
    
    outputFile = str(argv[-1])
    
    fs = open(outputFile, 'r')
    
    tempTableFlag = 0
    for line in fs:
        try:
            if line[0:3] == ' ++': #get reactivity at steps
                rhoTab = modules.getStepReactivity(line, rhoStep, rhoTime, power, decayPower, fissionPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem)
            elif line[0:34] == '                    MAIN TIME STEP': #get times at steps
                [tempStep, tempTime] = modules.tempStepTime(line, tempStep, tempTime)
            elif line[0:24] == ' FINISHED NULL TRANSIENT': #alter primaryTab to remove null transient info
                [tempStep, tempTime, IHXflow, IHXintermediateInlet, IHXintermediateOutlet] = modules.removeSteadyState(tempStep, tempTime, IHXflow, IHXintermediateInlet, IHXintermediateOutlet)
            elif line.split()[0] == 'MAXIMUM' and line.split()[1] == 'TEMPERATURES': #if at table of max temps, go through following lines to find peak channel info
                nextLine = fs.next()
                chanFlag = 0
                while chanFlag == 0:
                    if nextLine[19:20] == str(channel): #if peak channel, save info
                        [saturation, fuelPeak, cladPeak, coolantPeak, chanFlag] = modules.channelPeakValues(nextLine, saturation, fuelPeak, cladPeak, coolantPeak)
                    else: #if peak channel not on this line, skip to next
                        nextLine = fs.next()
            elif line.split()[0] == '***' and line.split()[1] == 'TRANSIENT' and int(line.split()[-2]) == channel: #if spot for transient normalized flow
                nextLine = fs.next()
                flowRate.append(float(nextLine.split()[-1]))
                inletFlag = 0
                while inletFlag == 0: #get inlet, outlet, and top of active core temps
                    if nextLine.split()[0] == 'VESSEL' and nextLine.split()[1] == 'OUTLET': #get outlet temp
                        nextLine = fs.next()
                        coolantOutlet.append(float(nextLine[15:23]))
                    elif nextLine.split()[0] == topOfActiveCore: #get temp at top of active core
                        topActiveCoreTemp.append(float(nextLine[15:23]))
                        nextLine = fs.next()
                    elif nextLine.split()[0] == '0.00000': #get inlet temp
                        coolantInlet.append(float(nextLine[15:23]))
                        inletFlag = 1
                    else:
                        nextLine = fs.next()
                fuelFlag = 0
                while fuelFlag == 0:
                    if nextLine[0:39] == '              INNER   MIDPOINT    OUTER': #get average fuel temp
                        nextLine = fs.next()
                        nextLine = fs.next() #skip two lines
                        fuelNodeMidHeight = []
                        fuelNodeAveTemp = []
                        cladNodeAveTemp = []
                        fuelNodeFlag = 0
                        while fuelNodeFlag == 0:
                            if nextLine == '\n': #if blank line, table is over
                                fuelNodeFlag = 1
                            else: #read in values
                                [fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp] = modules.nodeTemps(nextLine, fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp)
                                nextLine = fs.next()
                        [fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp] = modules.reverseNodeOrder(fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp)
                        #find average temperature of fuel/clad by volume-weighted average
                        [fuelAve, cladAve] = modules.aveFuelCladTemp(fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp, fuelAve, cladAve)
                        fuelFlag = 1
                    else: #move to next line to find table
                        nextLine = fs.next()
            elif line[0:36] == '                               PUMPS': #get intermediate loop flow rate from pump info
                nextLine = fs.next() #skip a line
                if nextLine == ' PUMP       FLOW                  HEAD                  SPEED               PUMP TORQUE     MOTOR TORQUE     HYDRAULIC EFFICIENCY': #if its first instance, skip it
                    pass
                else: #if not first instance, record normalized flow
                    nextLine = fs.next() #skip line
                    IHXflow.append(float(nextLine.split()[7]))
            elif line[0:20] == ' IHX TEMPERATURES, K' and int(line.split()[-1]) == IHXintermediateSide: #get temps at inlet and outlet of IHX intermediate side (tube side)
                nextLine = fs.next() #skip 4 lines
                nextLine = fs.next()
                nextLine = fs.next()
                nextLine = fs.next()
                IHXintermediateInlet.append(float(nextLine.split()[4]))
                IHXnodeFlag = 0
                while IHXnodeFlag == 0: #go through table until reaching end
                    previousLine = nextLine
                    nextLine = fs.next()
                    if nextLine == '\n': #if its empty, the previous line has outlet coolant temp
                        IHXintermediateOutlet.append(float(previousLine.split()[2]))
                        IHXnodeFlag = 1
            elif line[0:40] == '            NUMBER         CONCENTRATION': #get delayed neutron precursor concentrations and multiply by decay constant
                i = 1 #iterate for group
                for group in precursorTab[1:]:
                    nextLine = fs.next()
                    if nextLine[27:28] == '-': #if value is negative, set it to zero
                        group.append(0.0)
                    else:
                        group.append(float(nextLine.split()[1][0:7]+'E'+nextLine.split()[1][8:])*precursorDecayConstants[i-1])
                    i = i + 1
            else: #not of interest
                pass
        except (KeyError, ValueError, IndexError): #if the line is shit
            pass
    
    fs.close()
    
    #alter table to include SS temps (approximating SS by values at first step)
    [flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve, precursorTab, topActiveCoreTemp] = modules.addSteadyStateValues(flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve, precursorTab, topActiveCoreTemp)
    
    #find min and max rho components if not specified by user
    if rhoLimits == '[]':
        rhoLimits = modules.findRhoLimits(rhoTab)

    #alter tables if only part of the info was printed out/read in (i.e. if SAS printed out saturation temp but aborted before printing out coolant peak temp)
    primaryTab = modules.correctPrimaryTab(primaryTab)
    precursorTab = modules.correctPrecursorTab(precursorTab)

    
    #####
    #print to temporary file
    #####
    
    print('printing temporary files...\n')
    
    #make new directory and move into it
    mkdir('chan'+str(channel))
    chdir('./chan'+str(channel))

    #make tmp
    runDir = getcwd()
    fr = open('rho.txt', 'w')
    fp = open('temp.txt', 'w')
    fi = open('intermediate.txt', 'w')
    fpr = open('precursor.txt', 'w')
    
    #print reactivity tables
    modules.printReactivityTables(fr, rhoTab)
    fr.close()
    
    #print primary tables
    modules.printPrimaryTables(fp, primaryTab)
    fp.close()
    
    #print intermediate tables
    modules.printIntermediateTables(fi, intermediateTab)
    fi.close()
    
    #print precursor tables
    modules.printPrecursorTables(fpr, precursorTab)
    fpr.close()
    
    
    #####
    #make matlab produce plots
    #####
    
    #matlab commands,  #write out matlab commands here with no spaces, end with the quit command
    command = matlabPlotCommands(runDir, shortTimeLimit, rhoLimits, matlabExe)
    
    print('plotting...')
    
    plotRun = Popen(command)
    plotRun.wait()
    
    print('plotting complete...\n')
    
    #####
    #clean up
    #####
    
    print('cleaning up...\n')
    
    #delete temporary files
    modules.deleteTmpFiles()

    #move power, rho, and precursor plots out of channel-specific folders, as they are global to whole core
    if channel == channelNums[0]: #if this is first channel in list, move plots
        modules.moveGlobalPlots()
    else: #if not first channel in list, just delete files, they are duplicate
        modules.deleteGlobalPlots()

    #move out of channel directory
    chdir('../')

print('data extraction complete')
