def addSteadyStateValues(flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve, precursorTab, topActiveCoreTemp):
    ############################################################################
    ###approximate SS values by their first transient value
    ############################################################################

    flowRate[:0] = flowRate[0:1]
    coolantInlet[:0] = coolantInlet[0:1]
    coolantOutlet[:0] = coolantOutlet[0:1]
    fuelAve[:0] = fuelAve[0:1]
    cladAve[:0] = cladAve[0:1]
    topActiveCoreTemp[:0] = topActiveCoreTemp[0:1]

    for group in precursorTab[1:]:
        group[:0] = group[0:1]

    return [flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve, precursorTab, topActiveCoreTemp]

def aveFuelCladTemp(fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp, fuelAve, cladAve):
    ############################################################################
    ###average temperature of fuel and clad over axial height
    ############################################################################

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

    return [fuelAve, cladAve]

def channelPeakValues(nextLine, saturation, fuelPeak, cladPeak, coolantPeak):
    ############################################################################
    ###extracts peak temps and saturation temp in a channel
    ############################################################################
    
    saturation.append(float(nextLine[110:118]))
    fuelPeak.append(float(nextLine[28:36]))
    cladPeak.append(float(nextLine[52:60]))
    coolantPeak.append(float(nextLine[76:84]))
    chanFlag = 1

    return [saturation, fuelPeak, cladPeak, coolantPeak, chanFlag]

def correctPrimaryTab(primaryTab):
    ############################################################################
    ###makes all primary table columns same length by removing entries for time 
    ###steps in which not all info was printed out
    ############################################################################

    lengths = []
    for entry in primaryTab:
        lengths.append(len(entry))

    shortest = min(lengths)

    i = 0
    while i < len(primaryTab):
        if len(primaryTab[i]) > shortest:
            primaryTab[i] = primaryTab[i][:-1]
        i = i + 1

    return primaryTab

def deleteGlobalPlots():
    ############################################################################
    ###moves plots not specific to each channel into a global folder
    ############################################################################

    from os import remove

    remove('powerPlotLong.tif')
    remove('powerPlotShort.tif')
    remove('rhoPlotLong.tif')
    remove('rhoPlotShort.tif')
    remove('precursorPlotLong.tif')
    remove('precursorPlotShort.tif')

    remove('powerPlotLong.fig')
    remove('powerPlotShort.fig')
    remove('rhoPlotLong.fig')
    remove('rhoPlotShort.fig')
    remove('precursorPlotLong.fig')
    remove('precursorPlotShort.fig')

    return

def deleteTmpFiles():
    ############################################################################
    ###deletes temporary files used for matlab plotting
    ############################################################################

    from os import remove

    remove('./rho.txt')
    remove('./temp.txt')
    remove('./intermediate.txt')
    remove('./precursor.txt')

    return

def findRhoLimits(rhoTab):
    ############################################################################
    ###finds smallest and largest values of reactivity for use in setting plot
    ###limits
    ############################################################################

    #initialize rhoMax and rhoMin to small, but realistic values
    rhoMax = 0.1
    rhoMin = -0.1

    for component in rhoTab[4:]:
        for value in component:
            if value > rhoMax:
                rhoMax = value
            elif value < rhoMin:
                rhoMin = value

    rhoLimits = '['+str(rhoMin)+','+str(rhoMax)+']'

    return rhoLimits

def getStepReactivity(line, rhoStep, rhoTime, power, decayPower, fissionPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem):
    ############################################################################
    ###extracts reactivity coefficients for a given step and puts them into 
    ###rhoTab
    ############################################################################

    rhoStep.append(int(line[3:8]))
    rhoTime.append(float(line[8:17])) #cumulative time [s]
    power.append(float(line[30:35])) #normalized reactor power
    decayPower.append(float(line[38:43])) #decay power fraction
    fissionPower.append(power[-1]-decayPower[-1]) #fission power fraction
    netReactivity.append(float(line[53:61])) #net reactivity of core [$]
    CRDL.append(float(line[68:75])) #[$]
    radExpansion.append(float(line[75:82])) #[$]
    doppler.append(float(line[82:89])) #[$]
    fuelAxialExpansion.append(float(line[89:96])) #[$]
    cladAxialExpansion.append(float(line[96:103])) #[$]
    coolant.append(float(line[103:110])) #[$]
    structureAxialExpansion.append(float(line[110:117])) #[$]
    controlSystem.append(float(line[131:138])) #[$]

    return [rhoStep, rhoTime, power, decayPower, fissionPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem]

def moveGlobalPlots():
    ############################################################################
    ###moves plots not specific to each channel into a global folder
    ############################################################################

    from shutil import move

    move('powerPlotLong.tif','../globalPlots/')
    move('powerPlotShort.tif','../globalPlots/')
    move('rhoPlotLong.tif','../globalPlots/')
    move('rhoPlotShort.tif','../globalPlots/')
    move('precursorPlotLong.tif','../globalPlots/')
    move('precursorPlotShort.tif','../globalPlots/')

    move('powerPlotLong.fig','../globalFigs/')
    move('powerPlotShort.fig','../globalFigs/')
    move('rhoPlotLong.fig','../globalFigs/')
    move('rhoPlotShort.fig','../globalFigs/')
    move('precursorPlotLong.fig','../globalFigs/')
    move('precursorPlotShort.fig','../globalFigs/')

    return

def nodeTemps(nextLine, fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp):
    fuelNodeMidHeight.append(float(nextLine.split()[0]))
    fuelNodeAveTemp.append(float(nextLine.split()[7]))
    cladNodeAveTemp.append(float(nextLine.split()[2]))

    return [fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp]

def printIntermediateTables(fi, intermediateTab):
    ############################################################################
    ###prints temporary table of intermediate circuit parameters for MATLAB 
    ###plotting
    ############################################################################

    fi.write('time IHXinlet IHXoutlet IHXflow NaN\n')
    i = 0
    for stp in intermediateTab[0]:
        for entry in intermediateTab[1:]: #not including step number
            fi.write(str(entry[i])+' ')
        fi.write('\n')
        i = i + 1

    return

def printPrecursorTables(fpr, precursorTab):
    ############################################################################
    ###prints temporary table of precursor concentrations for MATLAB plotting
    ############################################################################

    fpr.write('time group1 group2 group3 group4 group5 group6 NaN\n')
    i = 0
    for stp in precursorTab[0]:
        for entry in precursorTab:
            fpr.write(str(entry[i])+' ')
        fpr.write('\n')
        i = i + 1

    return

def printPrimaryTables(fp, primaryTab):
    ############################################################################
    ###prints temporary table of primary circuit parameters for MATLAB plotting
    ############################################################################

    fp.write('time saturation fuelPeak cladPeak coolantPeak flowRate coolantInlet coolantOutlet fuelAve cladAve topActiveCoreTemp NaN\n')
    i = 0
    for stp in primaryTab[0]:
        for entry in primaryTab[1:]: #not including step number
            fp.write(str(entry[i])+' ')
        fp.write('\n')
        i = i + 1

    return

def printReactivityTables(fr, rhoTab):
    ############################################################################
    ###prints temporary table of reactivity components for MATLAB plotting
    ############################################################################

    fr.write('time totalPower decayPower fissionPower netReactivity CRDL radExpansion doppler fuelAxialExpansion cladAxialExpansion coolant structureAxialExpansion controlSystem NaN\n')
    for stp in rhoTab[0]:
        for entry in rhoTab[1:]: #not including step number
            fr.write(str(entry[stp-1])+' ')
        fr.write('\n')

    return

def removeSteadyState(tempStep, tempTime, IHXflow, IHXintermediateInlet, IHXintermediateOutlet):
    ############################################################################
    ###removes null transient values from arrays
    ############################################################################

    del tempStep[0:-1]
    del tempTime[0:-1]
    del IHXflow[0:-1]
    del IHXintermediateInlet[0:-1]
    del IHXintermediateOutlet[0:-1]
    tempTime[0] = 0.0

    return [tempStep, tempTime, IHXflow, IHXintermediateInlet, IHXintermediateOutlet]

def reverseNodeOrder(fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp):
    ############################################################################
    ###reverses the order of the arrays so that values go from inlet -> outlet
    ############################################################################

    fuelNodeMidHeight.reverse() #reverse order of values so list goes from inlet -> outlet
    fuelNodeAveTemp.reverse() #reverse order of values so list goes from inlet -> outlet
    cladNodeAveTemp.reverse() #reverse order of values so list goes from inlet -> outlet

    return [fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp]

def tempStepTime(line, tempStep, tempTime):
    ############################################################################
    ###extracts time steps and associated times
    ############################################################################

    tempStep.append(int(line.split()[3]))
    tempTime.append(float(line.split()[9][0:-4]+'E'+line.split()[9][-3:])) #convert stupid scientific notation (1.6D+04) to standard (1.6E+04)

    return [tempStep, tempTime]