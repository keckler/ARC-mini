def addSteadyStateValues(flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve):
    ############################################################################
    ###approximate SS values by their first transient value
    ############################################################################

    flowRate[:0] = flowRate[0:1]
    coolantInlet[:0] = coolantInlet[0:1]
    coolantOutlet[:0] = coolantOutlet[0:1]
    fuelAve[:0] = fuelAve[0:1]
    cladAve[:0] = cladAve[0:1]

    return [flowRate, coolantInlet, coolantOutlet, fuelAve, cladAve]

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

def deleteTmpFiles():
    ############################################################################
    ###deletes temporary files used for matlab plotting
    ############################################################################

    from os import remove

    remove('./rho.txt')
    remove('./temp.txt')

    return

def getStepReactivity(line, rhoStep, rhoTime, power, decayPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem):
    ############################################################################
    ###extracts reactivity coefficients for a given step and puts them into 
    ###rhoTab
    ############################################################################

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

    return [rhoStep, rhoTime, power, decayPower, netReactivity, CRDL, radExpansion, doppler, fuelAxialExpansion, cladAxialExpansion, coolant, structureAxialExpansion, controlSystem]

def nodeTemps(nextLine, fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp):
    fuelNodeMidHeight.append(float(nextLine.split()[0]))
    fuelNodeAveTemp.append(float(nextLine.split()[7]))
    cladNodeAveTemp.append(float(nextLine.split()[2]))

    return [fuelNodeMidHeight, fuelNodeAveTemp, cladNodeAveTemp]

def printReactivityTables(fr, rhoStep, rhoTab):
    ############################################################################
    ###prints temporary table of reactivity components for MATLAB plotting
    ############################################################################

    fr.write('time totalPower decayPower netReactivity CRDL radExpansion doppler fuelAxialExpansion cladAxialExpansion coolant structureAxialExpansion controlSystem NaN\n')
    for stp in rhoStep:
        for entry in rhoTab[1:]: #not including step number
            fr.write(str(entry[stp-1])+' ')
        fr.write('\n')

    return

def printTempTables(ft, tempStep, primaryTab):

    ft.write('time saturation fuelPeak cladPeak coolantPeak flowRate coolantInlet coolantOutlet fuelAve cladAve NaN\n')
    i = 0
    for stp in tempStep:
        for entry in primaryTab[1:]: #not including step number
            ft.write(str(entry[i])+' ')
        ft.write('\n')
        i = i + 1

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