def matlabPlotCommands(runDir, shortTimeLimit, rhoLimits, matlabExe):

    matlabCommands = ["rhoTab=readtable('"+runDir+"/rho.txt','Delimiter','space','ReadVariableNames',1);" #read in rho table
                      'rhoTab=table2array(rhoTab);' #convert table to array
                      'rhoTab=rhoTab(:,1:end-1);' #get rid of last column, which is NaN
                      "primaryTab=readtable('"+runDir+"/temp.txt','Delimiter','space','ReadVariableNames',1);"#read in temp table
                      'primaryTab=table2array(primaryTab);' #convert table to array
                      'primaryTab=primaryTab(:,1:end-1);' #get rid of last column, which is NaN
                      'primaryTab(:,2:5)=primaryTab(:,2:5)-273.15;primaryTab(:,7:end)=primaryTab(:,7:end)-273.15;' #convert temps from K to C
                      "intermediateTab=readtable('"+runDir+"/intermediate.txt','Delimiter','space','ReadVariableNames',1);" #read in intermediate table
                      'intermediateTab=table2array(intermediateTab);' #convert table to array
                      'intermediateTab=intermediateTab(:,1:end-1);' #get rid of last column, which is NaN
                      'intermediateTab(:,2:3)=intermediateTab(:,2:3)-273.15;' #convert temps from K to C
                      "precursorTab=readtable('"+runDir+"/precursor.txt','Delimiter','space','ReadVariableNames',1);" #read in precursor table
                      'precursorTab=table2array(precursorTab);' #convert table to array
                      'precursorTab=precursorTab(:,1:end-1);' #get rid of last column, which is NaN
                      "powerPlotLong=semilogy(rhoTab(:,1),rhoTab(:,2),rhoTab(:,1),rhoTab(:,3),'--',primaryTab(:,1),primaryTab(:,6),'-.',intermediateTab(:,1),intermediateTab(:,4),':');" #make plot of long term power behavior
                      'axis([0,rhoTab(end,1),1E-3,2]);'
                      "xlabel('time,(s)');"
                      "ylabel('normalizedPower/Flow');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('totalPower','decayPower','flowRate,peakChannel','flowRate,intermediateLoop','Location','eastoutside');"
                      "print('powerPlotLong','-dtiffn');"
                      "powerPlotShort=semilogy(rhoTab(:,1),rhoTab(:,2),rhoTab(:,1),rhoTab(:,3),'--',primaryTab(:,1),primaryTab(:,6),'-.',intermediateTab(:,1),intermediateTab(:,4),':');" #make plot of short term power behavior
                      'axis([0,'+str(shortTimeLimit)+',1E-3,2]);'
                      "xlabel('time,(s)');"
                      "ylabel('normalizedPower/Flow');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('totalPower','decayPower','flowRate,peakChannel','flowRate,intermediateLoop','Location','eastoutside');"
                      "print('powerPlotShort','-dtiff');"
                      "reactivityPlotLong=plot(rhoTab(:,1),rhoTab(:,4),rhoTab(:,1),rhoTab(:,5),rhoTab(:,1),rhoTab(:,6),rhoTab(:,1),rhoTab(:,7),'--',rhoTab(:,1),rhoTab(:,8),'--',rhoTab(:,1),rhoTab(:,9),'--',rhoTab(:,1),rhoTab(:,10),'-.',rhoTab(:,1),rhoTab(:,11),'-.',rhoTab(:,1),rhoTab(:,12),'-.');" #make plot of long term reactivity component behavior
                      'ylim('+rhoLimits+');'
                      "xlabel('time,(s)');"
                      "ylabel('reactivity,($)');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('netReactivity','CRDL','radExpansion','doppler','fuelAxialExpansion','cladAxialExpansion','coolant','structureAxialExpansion','controlSystem','Location','eastoutside');"
                      "print('rhoPlotLong','-dtiff');"
                      "reactivityPlotLong=plot(rhoTab(:,1),rhoTab(:,4),rhoTab(:,1),rhoTab(:,5),rhoTab(:,1),rhoTab(:,6),rhoTab(:,1),rhoTab(:,7),'--',rhoTab(:,1),rhoTab(:,8),'--',rhoTab(:,1),rhoTab(:,9),'--',rhoTab(:,1),rhoTab(:,10),'-.',rhoTab(:,1),rhoTab(:,11),'-.',rhoTab(:,1),rhoTab(:,12),'-.');" #make plot of short term reactivity component behavior
                      'xlim([0,'+str(shortTimeLimit)+']);'
                      'ylim('+rhoLimits+');'
                      "xlabel('time,(s)');"
                      "ylabel('reactivity,($)');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('netReactivity','CRDL','radExpansion','doppler','fuelAxialExpansion','cladAxialExpansion','coolant','structureAxialExpansion','controlSystem','Location','eastoutside');"
                      "print('rhoPlotShort','-dtiff');"
                      "plot(primaryTab(:,1),primaryTab(:,2),primaryTab(:,1),primaryTab(:,3),primaryTab(:,1),primaryTab(:,4),primaryTab(:,1),primaryTab(:,5),primaryTab(:,1),primaryTab(:,7),'--',primaryTab(:,1),primaryTab(:,8),'--',primaryTab(:,1),primaryTab(:,9),'-.',primaryTab(:,1),primaryTab(:,10),'-.',intermediateTab(:,1),intermediateTab(:,2),':',intermediateTab(:,1),intermediateTab(:,3),':');" #make plot of long term temp behavior
                      "xlabel('time,(s)');"
                      "ylabel('temperature,(C)');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('saturation','fuelPeak','cladPeak','coolantPeak','coolantInlet','coolantOutlet','fuelAve','cladAve','IHXinlet,tubeSide','IHXoutlet,tubeSide','Location','eastoutside');"
                      "print('tempPlotLong','-dtiff');"
                      "plot(primaryTab(:,1),primaryTab(:,2),primaryTab(:,1),primaryTab(:,3),primaryTab(:,1),primaryTab(:,4),primaryTab(:,1),primaryTab(:,5),primaryTab(:,1),primaryTab(:,7),'--',primaryTab(:,1),primaryTab(:,8),'--',primaryTab(:,1),primaryTab(:,9),'-.',primaryTab(:,1),primaryTab(:,10),'-.',intermediateTab(:,1),intermediateTab(:,2),':',intermediateTab(:,1),intermediateTab(:,3),':');" #make plot of short term temp behavior
                      "xlabel('time,(s)');"
                      "ylabel('temperature,(C)');"
                      'xlim([0,'+str(shortTimeLimit)+']);'
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('saturation','fuelPeak','cladPeak','coolantPeak','coolantInlet','coolantOutlet','fuelAve','cladAve','IHXinlet,tubeSide','IHXoutlet,tubeSide','Location','eastoutside');"
                      "print('tempPlotShort','-dtiff');"
                      "semilogy(precursorTab(:,1),precursorTab(:,2),precursorTab(:,1),precursorTab(:,3),precursorTab(:,1),precursorTab(:,4),precursorTab(:,1),precursorTab(:,5),'--',precursorTab(:,1),precursorTab(:,6),'--',precursorTab(:,1),precursorTab(:,7),'--');" #make plot of long term behavior
                      "ylabel('delayedNeutronProductionRate,(1/s)');"
                      "xlabel('time,(s)');"
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('group1','group2','group3','group4','group5','group6');"
                      "print('precursorPlotLong','-dtiff');"
                      "savefig('precursorPlotLong');"
                      "semilogy(precursorTab(:,1),precursorTab(:,2),precursorTab(:,1),precursorTab(:,3),precursorTab(:,1),precursorTab(:,4),precursorTab(:,1),precursorTab(:,5),'--',precursorTab(:,1),precursorTab(:,6),'--',precursorTab(:,1),precursorTab(:,7),'--');" #make plot of long term behavior
                      "ylabel('delayedNeutronProductionRate,(1/s)');"
                      "xlabel('time,(s)');"
                      'xlim([0,'+str(shortTimeLimit)+']);'
                      'ax=gca;'
                      "grid(ax,'on');"
                      "legend('group1','group2','group3','group4','group5','group6');"
                      "print('precursorPlotShort','-dtiff');"
                      "savefig('precursorPlotShort');"
                      'quit;'] #quit matlab
    
    #concatenate all commands together
    matlabCommand = ''
    for command in matlabCommands:
        matlabCommand = matlabCommand+command
    
    command = [matlabExe, '-nodesktop', '-nosplash', '-nodisplay', '-r', matlabCommand] #for running locally

    return command