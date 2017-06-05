def matlabPlotCommands_csv(channelCSV, matlabExe):
    #runs matlab for plotting data extracted to .csv format

    matlabCommands = ["channel=csvread('"+channelCSV+"',1,0);" #import channel csv output
                      "wholeCore=csvread('WholeCore.csv',1,0);" #import whole core csv output
                      "primar=csvread('primar4.csv',1,0);" #import primar4 csv output
                      "powerPlot=semilogy(wholeCore(:,3),wholeCore(:,5),'-',wholeCore(:,3),wholeCore(:,5)-wholeCore(:,8),'--',wholeCore(:,3),wholeCore(:,8),'--',primar(:,4),[ones(49,1);primar(50:end,5)./primar(50,5)],'.-');" #power/flow plot
                      "legend('totalPower','fissionPower','decayPower','flow');"
                      "xlabel('time,(s)');"
                      "ylabel('normalizedPower/Flow');"
                      "ax=gca;"
                      "grid(ax,'on');"
                      "savefig('powerPlot');"
                      "tempPlot=plot(channel(:,1),channel(:,10)-273.15,channel(:,1),channel(:,9)-273.15,'--',channel(:,1),channel(:,8)-273.15,'--',channel(:,1),channel(:,7)-273.15,'--',channel(:,1),channel(:,18)-273.15,'-.',channel(:,1),channel(:,19)-273.15,'-.');" #channel temps plot
                      "xlabel('time,(s)');"
                      "ylabel('temperature,(C)');"
                      "ax=gca;"
                      "grid(ax,'on');"
                      "legend('saturation','fuelPeak','cladPeak','coolantPeak','coolantOutlet','coolantInlet');"
                      "savefig('tempPlot.fig');"
                      "rhoPlot=plot(wholeCore(:,3),wholeCore(:,9),wholeCore(:,3),wholeCore(:,10),'--',wholeCore(:,3),wholeCore(:,9)-wholeCore(:,10)-wholeCore(:,11)-wholeCore(:,12)-wholeCore(:,13)-wholeCore(:,14)-wholeCore(:,15)-wholeCore(:,16)-wholeCore(:,17),'--',wholeCore(:,3),wholeCore(:,11),'-.',wholeCore(:,3),wholeCore(:,14),'-.',wholeCore(:,3),wholeCore(:,15),'-.',wholeCore(:,3),wholeCore(:,12),'-.',wholeCore(:,3),wholeCore(:,13),'-.',wholeCore(:,3),wholeCore(:,16),'-.',wholeCore(:,3),wholeCore(:,17),'-.');"
                      "xlabel('time,(s)');"
                      "ylabel('reactivity,($)');"
                      "ax=gca;"
                      "grid(ax,'on');"
                      "legend('net','controlRods','ARC','doppler','CRDL','coolant','axial','radial','fuel','clad');"
                      "savefig('rhoPlot.fig');"
                      "dummy=fopen('flag.txt','w');"#make file just as flag for when run is complete
                      "fclose(dummy);"
                      "maxFile=fopen('../../../max.txt','a');" #open file of max temps and write to it
                      "fprintf(maxFile,'%f\\n',max(channel(:,7)));"
                      "fclose(maxFile);"
                      "asyFile=fopen('../../../asymptotic.txt','a');" #open file of asymptotic temps and write to it
                      "fprintf(asyFile,'%f\\n',channel(end,7));"
                      "fclose(asyFile);"
                      "quit;"]

    #concatenate all commands together
    matlabCommand = ''
    for command in matlabCommands:
        matlabCommand = matlabCommand+command

    command = [matlabExe, '-nodesktop', '-nosplash', '-nodisplay', '-r', matlabCommand]

    return command