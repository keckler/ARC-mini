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

peakChannelNum = 1 #channel number of assembly with peak power/flow
rhoLimits = '[-0.25,0.25]' #range of reactivity to be plotted, ($), no spaces allowed
shortTimeLimit = 500 #range of time to be plotted in short time scale plots, (s)
IHXintermediateSide = 13 #element number of intermediate side of IHX (tube side)
IHXpump = 2 #element number of intermediate pump
matlabExe = '/Applications/MATLAB_R2014b.app/bin/matlab' #for running locally
#matlabExe = 'matlab' #for running on savio


#####
#imports
#####

from os import remove
from os import getcwd
from subprocess import Popen
from sys import argv


#####
#initialize stuff
#####

print('initializing stuff...\n')

#reactivity parameters
rhoStep = []
rhoTime = [] #[s]
power = [] #normalized
decayPower = [] #normalized
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

#intermediate loop parameters
IHXintermediateInlet = [] #[K]
IHXintermediateOutlet = [] #[K]
IHXflow = [] #[normalized]

#put all entries into tables
rhoTab = [rhoStep, rhoTime, power, decayPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem]
primaryTab = [tempStep, tempTime, saturation, fuelPeak, cladPeak, coolantPeak, flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve]
intermediateTab = [IHXintermediateInlet, IHXintermediateOutlet, IHXflow]


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
            rhoStep.append(int(line[3:8]))
            rhoTime.append(float(line[8:17])) #cumulative time [s]
            power.append(float(line[30:35])) #normalized reactor power
            decayPower.append(float(line[38:43])) #normalized decay power
            netReactivity.append(float(line[53:61])) #net reactivity of core [$]
            CRDL.append(float(line[68:75])) #[$]
            radExpansion.append(float(line[75:82])) #[$]
            doppler.append(float(line[82:89])) #[$]
            fuelAxialExpansion.append(float(line[89:96])) #[$]
            cladAxialExpansion.append(float(line[96:103])) #[$]
            coolant.append(float(line[103:110])) #[$]
            structureAxialExpansion.append(float(line[110:117])) #[$]
            controlSystem.append(float(line[131:138])) #[$]
        elif line[0:34] == '                    MAIN TIME STEP': #get temps at steps
            tempStep.append(int(line.split()[3]))
            tempTime.append(float(line.split()[9][0:-4]+'E'+line.split()[9][-3:])) #convert stupid scientific notation (1.6D+04) to standard (1.6E+04)
        elif line[0:24] == ' FINISHED NULL TRANSIENT': #alter primaryTab to remove null transient info
            del tempStep[0:-1]
            del tempTime[0:-1]
            del IHXflow[0:-1]
            del IHXintermediateInlet[0:-1]
            del IHXintermediateOutlet[0:-1]
            tempTime[0] = 0.0
        elif line.split()[0] == 'MAXIMUM' and line.split()[1] == 'TEMPERATURES': #if at table of max temps, go through following lines to find peak channel info
            nextLine = fs.next()
            chanFlag = 0
            while chanFlag == 0:
                if nextLine[19:20] == str(peakChannelNum): #if peak channel, save info
                    saturation.append(float(nextLine[110:118]))
                    fuelPeak.append(float(nextLine[28:36]))
                    cladPeak.append(float(nextLine[52:60]))
                    coolantPeak.append(float(nextLine[76:84]))
                    chanFlag = 1
                else: #if peak channel not on this line, skip to next
                    nextLine = fs.next()
        elif line.split()[0] == '***' and line.split()[1] == 'TRANSIENT' and int(line.split()[-2]) == peakChannelNum: #if spot for transient normalized flow
            nextLine = fs.next()
            flowRate.append(float(nextLine.split()[-1]))
            inletFlag = 0
            while inletFlag == 0: #get inlet and outlet temps
                if nextLine.split()[0] == 'VESSEL' and nextLine.split()[1] == 'OUTLET': #get outlet temp
                    nextLine = fs.next()
                    coolantOutlet.append(float(nextLine[15:23]))
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
                            fuelNodeMidHeight.append(float(nextLine.split()[0]))
                            fuelNodeAveTemp.append(float(nextLine.split()[7]))
                            cladNodeAveTemp.append(float(nextLine.split()[2]))
                            nextLine = fs.next()
                    fuelNodeMidHeight.reverse() #reverse order of values so list goes from inlet -> outlet
                    fuelNodeAveTemp.reverse() #reverse order of values so list goes from inlet -> outlet
                    cladNodeAveTemp.reverse() #reverse order of values so list goes from inlet -> outlet
                    #find average temperature of fuel/clad by volume-weighted average
                    i = 0
                    fuelNumerator = 0 #numerator of weighted sum for fuel
                    fuelDenominator = 0 #denominator of weighted sum for fuel
                    cladNumerator = 0 #numerator of weighted sum for clad
                    cladDenominator = 0 #denominator of weighted sum for clad
                    nodeHeight = fuelNodeMidHeight[0]*2
                    while i < len(fuelNodeMidHeight)-1:
                        fuelNumerator = fuelNumerator + fuelNodeAveTemp[i]*nodeHeight
                        cladNumerator = cladNumerator + cladNodeAveTemp[i]*nodeHeight
                        fuelDenominator = fuelDenominator + nodeHeight
                        cladDenominator = cladDenominator + nodeHeight
                        nodeHeight = (fuelNodeMidHeight[i+1] - (fuelNodeMidHeight[i]+nodeHeight/2))*2
                        i = i + 1
                    fuelAve.append(fuelNumerator/fuelDenominator)
                    cladAve.append(cladNumerator/cladDenominator)
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
        else: #not of interest
            pass
    except (KeyError, ValueError, IndexError): #if the line is shit
        pass

fs.close()

#alter table to include SS temps (approximating SS by values at first step)
flowRate[:0] = flowRate[0:1]
coolantInlet[:0] = coolantInlet[0:1]
coolantOutlet[:0] = coolantOutlet[0:1]
fuelAve[:0] = fuelAve[0:1]
cladAve[:0] = cladAve[0:1]


#####
#print to temporary file
#####

print('printing temporary files...\n')

#make tmp
runDir = getcwd()
fr = open('rho.txt', 'w')
ft = open('temp.txt', 'w')

#print reactivity tables
fr.write('time totalPower decayPower netReactivity CRDL radExpansion doppler fuelAxialExpansion cladAxialExpansion coolant structureAxialExpansion controlSystem NaN\n')
for stp in rhoStep:
    for entry in rhoTab[1:]: #not including step number
        fr.write(str(entry[stp-1])+' ')
    fr.write('\n')

fr.close()

#print temperature tables
ft.write('time saturation fuelPeak cladPeak coolantPeak flowRate coolantInlet coolantOutlet fuelAve cladAve NaN\n')
i = 0
for stp in tempStep:
    for entry in primaryTab[1:]: #not including step number
        ft.write(str(entry[i])+' ')
    ft.write('\n')
    i = i + 1

ft.close()


#####
#make matlab produce plots
#####

#matlab commands,  #write out matlab commands here with no spaces, end with the quit command
matlabCommands = ["rhoTab=readtable('"+runDir+"/rho.txt','Delimiter','space','ReadVariableNames',1);" #read in rho table
                  'rhoTab=table2array(rhoTab);' #convert table to array
                  'rhoTab=rhoTab(:,1:end-1);' #get rid of last column, which is NaN
                  "primaryTab=readtable('"+runDir+"/temp.txt','Delimiter','space','ReadVariableNames',1);"#read in temp table
                  'primaryTab=table2array(primaryTab);' #convert table to array
                  'primaryTab=primaryTab(:,1:end-1);' #get rid of last column, which is NaN
                  'primaryTab(:,2:5)=primaryTab(:,2:5)-273.15;primaryTab(:,7:end)=primaryTab(:,7:end)-273.15;' #convert temps from K to C
                  "powerPlotLong=semilogy(rhoTab(:,1),rhoTab(:,2),rhoTab(:,1),rhoTab(:,3),'--',primaryTab(:,1),primaryTab(:,6),'-.');" #make plot of long term power behavior
                  'axis([0,rhoTab(end,1),1E-3,2]);'
                  "xlabel('time,(s)');"
                  "ylabel('normalizedPower/Flow');"
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('totalPower','decayPower','flowRate,peakChannel');"
                  "print('powerPlotLong','-dtiffn');"
                  "powerPlotShort=semilogy(rhoTab(:,1),rhoTab(:,2),rhoTab(:,1),rhoTab(:,3),'--',primaryTab(:,1),primaryTab(:,6),'-.');" #make plot of short term power behavior
                  'axis([0,'+str(shortTimeLimit)+',1E-3,2]);'
                  "xlabel('time,(s)');"
                  "ylabel('normalizedPower/Flow');"
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('totalPower','decayPower','flowRate,peakChannel');"
                  "print('powerPlotShort','-dtiff');"
                  "reactivityPlotLong=plot(rhoTab(:,1),rhoTab(:,4),rhoTab(:,1),rhoTab(:,5),rhoTab(:,1),rhoTab(:,6),rhoTab(:,1),rhoTab(:,7),'--',rhoTab(:,1),rhoTab(:,8),'--',rhoTab(:,1),rhoTab(:,9),'--',rhoTab(:,1),rhoTab(:,10),'-.',rhoTab(:,1),rhoTab(:,11),'-.',rhoTab(:,1),rhoTab(:,12),'-.');" #make plot of long term reactivity component behavior
                  'ylim('+rhoLimits+');'
                  "xlabel('time,(s)');"
                  "ylabel('reactivity,($)');"
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('netReactivity','CRDL','radExpansion','doppler','fuelAxialExpansion','cladAxialExpansion','coolant','structureAxialExpansion','controlSystem');"
                  "print('rhoPlotLong','-dtiff');"
                  "reactivityPlotLong=plot(rhoTab(:,1),rhoTab(:,4),rhoTab(:,1),rhoTab(:,5),rhoTab(:,1),rhoTab(:,6),rhoTab(:,1),rhoTab(:,7),'--',rhoTab(:,1),rhoTab(:,8),'--',rhoTab(:,1),rhoTab(:,9),'--',rhoTab(:,1),rhoTab(:,10),'-.',rhoTab(:,1),rhoTab(:,11),'-.',rhoTab(:,1),rhoTab(:,12),'-.');" #make plot of short term reactivity component behavior
                  'xlim([0,'+str(shortTimeLimit)+']);'
                  'ylim('+rhoLimits+');'
                  "xlabel('time,(s)');"
                  "ylabel('reactivity,($)');"
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('netReactivity','CRDL','radExpansion','doppler','fuelAxialExpansion','cladAxialExpansion','coolant','structureAxialExpansion','controlSystem');"
                  "print('rhoPlotShort','-dtiff');"
                  "plot(primaryTab(:,1),primaryTab(:,2),primaryTab(:,1),primaryTab(:,3),primaryTab(:,1),primaryTab(:,4),primaryTab(:,1),primaryTab(:,5),primaryTab(:,1),primaryTab(:,7),'--',primaryTab(:,1),primaryTab(:,8),'--',primaryTab(:,1),primaryTab(:,9),'-.',primaryTab(:,1),primaryTab(:,10),'-.');" #make plot of long term temp behavior
                  "xlabel('time,(s)');"
                  "ylabel('temperature,(C)');"
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('saturation','fuelPeak','cladPeak','coolantPeak','coolantInlet','coolantOutlet','fuelAve','cladAve');"
                  "print('tempPlotLong','-dtiff');"
                  "plot(primaryTab(:,1),primaryTab(:,2),primaryTab(:,1),primaryTab(:,3),primaryTab(:,1),primaryTab(:,4),primaryTab(:,1),primaryTab(:,5),primaryTab(:,1),primaryTab(:,7),'--',primaryTab(:,1),primaryTab(:,8),'--',primaryTab(:,1),primaryTab(:,9),'-.',primaryTab(:,1),primaryTab(:,10),'-.');" #make plot of short term temp behavior
                  "xlabel('time,(s)');"
                  "ylabel('temperature,(C)');"
                  'xlim([0,'+str(shortTimeLimit)+']);'
                  'ax=gca;'
                  "grid(ax,'on');"
                  "legend('saturation','fuelPeak','cladPeak','coolantPeak','coolantInlet','coolantOutlet','fuelAve','cladAve');"
                  "print('tempPlotShort','-dtiff');"
                  'quit;'] #quit matlab

#concatenate all commands together
matlabCommand = ''
for command in matlabCommands:
    matlabCommand = matlabCommand+command

command = [matlabExe, '-nodesktop', '-nosplash', '-nodisplay', '-r', matlabCommand] #for running locally

print('plotting...')

plotRun = Popen(command)
plotRun.wait()

print('plotting complete...\n')

#####
#clean up
#####

print('cleaning up...\n')

#delete the temporary file
remove('./rho.txt')
remove('./temp.txt')
