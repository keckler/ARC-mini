clear all;

run('~/Downloads/BnB_bumat3.m');
Na = 6.022E23; %avogadro's number
vol = 42*sqrt(3)/2*18.9^2*12.5; %volume of batch segment, cm^3
batchList = 1:12;
axialList = 1:24;
x = [12.5:12.5:300]';

%do it for coolant
run('~/Documents/work/ARC/serpent/worths/cool/BnB_sens.m');
% run('~/Documents/work/ARC/serpent/worths/clad/BnB_sens.m');
% run('~/Documents/work/ARC/serpent/worths/fuel/BnB_sens.m');
isotopes = [11023];
batchSensitivities = zeros(length(axialList), length(batchList));
totalCoolant = 0;

for batch = batchList
    for axial = axialList
        mat = sprintf('Batch%iAxial%i', batch, axial);
        rho = 0;
        for iMatIsotope = 1:length(eval(sprintf('m%s(:,1)',mat)))
            matIsotope = eval(sprintf('m%s(%i,1)',mat,iMatIsotope));
            for isotope = isotopes
                if matIsotope == isotope
                    MW = mod(isotope,1000);
                    N = eval(sprintf('m%s(%i,2)',mat,iMatIsotope));
                    rho = rho + N*MW/Na*10^24; %g/cm^3
                end
            end
        end
        mass = vol*rho/1000; %kg
        sensitivity = ADJ_PERT_KEFF_SENS_E_INT(eval(sprintf('iSENS_MAT_%s',mat)), iSENS_ZAI_110230, iSENS_PERT_TOT_XS, 1);
        totalCoolant = totalCoolant + sensitivity;
        sensPerMass = sensitivity/mass;
        batchSensitivities(axial, batch) = sensPerMass;
    end
end

fprintf('total coolant worth = %f\n', totalCoolant);

channelSensitivities = zeros(length(axialList), 7);
channelSensitivities(:,1) = batchSensitivities(:,1);
channelSensitivities(:,2) = (batchSensitivities(:,2)+batchSensitivities(:,3))/2;
channelSensitivities(:,3) = (batchSensitivities(:,4)+batchSensitivities(:,5)+batchSensitivities(:,6))/3;
channelSensitivities(:,4) = (batchSensitivities(:,7)+batchSensitivities(:,8)+batchSensitivities(:,9)+batchSensitivities(:,10)+batchSensitivities(:,11)+batchSensitivities(:,12))/6;
channelSensitivities(:,6) = batchSensitivities(:,1);
channelSensitivities(:,7) = batchSensitivities(:,2);

chan1 = fit(x,channelSensitivities(:,1),'smoothingspline');
chan2 = fit(x,channelSensitivities(:,2),'smoothingspline');
chan3 = fit(x,channelSensitivities(:,3),'smoothingspline');
chan4 = fit(x,channelSensitivities(:,4),'smoothingspline');
chan5 = fit(x,channelSensitivities(:,5),'smoothingspline');
chan6 = fit(x,channelSensitivities(:,6),'smoothingspline');
chan7 = fit(x,channelSensitivities(:,7),'smoothingspline');

channelSensitivities(:,1) = chan1(x);
channelSensitivities(:,2) = chan2(x);
channelSensitivities(:,3) = chan3(x);
channelSensitivities(:,4) = chan4(x);
channelSensitivities(:,5) = chan5(x);
channelSensitivities(:,6) = chan6(x);
channelSensitivities(:,7) = chan7(x);

channelSensitivities = -channelSensitivities;

fprintf('coolant void\n');
for i = 1:7
    fprintf('chan%i\n', i);
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(1,i), channelSensitivities(2,i), channelSensitivities(3,i), channelSensitivities(4,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(5,i), channelSensitivities(6,i), channelSensitivities(7,i), channelSensitivities(8,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(9,i), channelSensitivities(10,i), channelSensitivities(11,i), channelSensitivities(12,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(13,i), channelSensitivities(14,i), channelSensitivities(15,i), channelSensitivities(16,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(17,i), channelSensitivities(18,i), channelSensitivities(19,i), channelSensitivities(20,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(21,i), channelSensitivities(22,i), channelSensitivities(23,i), channelSensitivities(24,i));
end
fprintf('\n');

%do it for cladding
run('~/Documents/work/ARC/serpent/worths/clad/BnB_sens.m');
isotopes = [26056
                24052
                26054
                42100
                42098
                26057
                42097
                42095
                24053
                24050
                42096
                74000
                24054
                28058
                26058
                6000
                42092
                28060
                42094
                28062
                23051
                28061
                28064]';
batchSensitivities = zeros(length(axialList), length(batchList));

for batch = batchList
    for axial = axialList
        mat = sprintf('Batch%iAxial%i', batch, axial);
        rho = 0;
        for iMatIsotope = 1:length(eval(sprintf('m%s(:,1)',mat)))
            matIsotope = eval(sprintf('m%s(%i,1)',mat,iMatIsotope));
            for isotope = isotopes
                if matIsotope == isotope
                    MW = mod(isotope,1000);
                    N = eval(sprintf('m%s(%i,2)',mat,iMatIsotope));
                    rho = rho + N*MW/Na*10^24; %g/cm^3
                end
            end
        end
        mass = vol*rho/1000; %kg
        sensitivity = ADJ_PERT_KEFF_SENS_E_INT(eval(sprintf('iSENS_MAT_%s',mat)), iSENS_ZAI_SUM, iSENS_PERT_TOT_XS, 1);
        sensPerMass = sensitivity/mass;
        batchSensitivities(axial, batch) = sensPerMass;
    end
end

channelSensitivities = zeros(length(axialList), 7);
channelSensitivities(:,1) = batchSensitivities(:,1);
channelSensitivities(:,2) = (batchSensitivities(:,2)+batchSensitivities(:,3))/2;
channelSensitivities(:,3) = (batchSensitivities(:,4)+batchSensitivities(:,5)+batchSensitivities(:,6))/3;
channelSensitivities(:,4) = (batchSensitivities(:,7)+batchSensitivities(:,8)+batchSensitivities(:,9)+batchSensitivities(:,10)+batchSensitivities(:,11)+batchSensitivities(:,12))/6;
channelSensitivities(:,6) = batchSensitivities(:,1);
channelSensitivities(:,7) = batchSensitivities(:,2);

chan1 = fit(x,channelSensitivities(:,1),'smoothingspline');
chan2 = fit(x,channelSensitivities(:,2),'smoothingspline');
chan3 = fit(x,channelSensitivities(:,3),'smoothingspline');
chan4 = fit(x,channelSensitivities(:,4),'smoothingspline');
chan5 = fit(x,channelSensitivities(:,5),'smoothingspline');
chan6 = fit(x,channelSensitivities(:,6),'smoothingspline');
chan7 = fit(x,channelSensitivities(:,7),'smoothingspline');

channelSensitivities(:,1) = chan1(x);
channelSensitivities(:,2) = chan2(x);
channelSensitivities(:,3) = chan3(x);
channelSensitivities(:,4) = chan4(x);
channelSensitivities(:,5) = chan5(x);
channelSensitivities(:,6) = chan6(x);
channelSensitivities(:,7) = chan7(x);

fprintf('cladding\n');
for i = 1:7
    fprintf('chan%i\n', i);
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(1,i), channelSensitivities(2,i), channelSensitivities(3,i), channelSensitivities(4,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(5,i), channelSensitivities(6,i), channelSensitivities(7,i), channelSensitivities(8,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(9,i), channelSensitivities(10,i), channelSensitivities(11,i), channelSensitivities(12,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(13,i), channelSensitivities(14,i), channelSensitivities(15,i), channelSensitivities(16,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(17,i), channelSensitivities(18,i), channelSensitivities(19,i), channelSensitivities(20,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(21,i), channelSensitivities(22,i), channelSensitivities(23,i), channelSensitivities(24,i));
end
fprintf('\n');

%do it for fuel
run('~/Documents/work/ARC/serpent/worths/fuel/BnB_sens.m');
isotopes = [92238
            94239
            94240
            54134
            55135
            54136
            56138
            55137
            55133
            57139
            44102
            58140
            54132
            59141
            58142
            44104
            60143
            45103
            60144
            44101
            40096
            43099
            46106
            54131
            60146
            40094
            60145
            46105
            40093
            40092
            52130
            46108
            40091
            60148
            46107
            94241
            38090
            39089
            53129
            60150
            46104
            44100
            62152
            62149
            38088
            62147
            23000
            61147
            37087
            93237
            52128
            62148
            56137
            62150
            44106
            58144
            56136
            47109
            62151]';
batchSensitivities = zeros(length(axialList), length(batchList));

for batch = batchList
    for axial = axialList
        mat = sprintf('Batch%iAxial%i', batch, axial);
        rho = 0;
        for iMatIsotope = 1:length(eval(sprintf('m%s(:,1)',mat)))
            matIsotope = eval(sprintf('m%s(%i,1)',mat,iMatIsotope));
            for isotope = isotopes
                if matIsotope == isotope
                    MW = mod(isotope,1000);
                    N = eval(sprintf('m%s(%i,2)',mat,iMatIsotope));
                    rho = rho + N*MW/Na*10^24; %g/cm^3
                end
            end
        end
        mass = vol*rho/1000; %kg
        sensitivity = ADJ_PERT_KEFF_SENS_E_INT(eval(sprintf('iSENS_MAT_%s',mat)), iSENS_ZAI_SUM, iSENS_PERT_TOT_XS, 1);
        sensPerMass = sensitivity/mass;
        batchSensitivities(axial, batch) = sensPerMass;
    end
end

channelSensitivities = zeros(length(axialList), 7);
channelSensitivities(:,1) = batchSensitivities(:,1);
channelSensitivities(:,2) = (batchSensitivities(:,2)+batchSensitivities(:,3))/2;
channelSensitivities(:,3) = (batchSensitivities(:,4)+batchSensitivities(:,5)+batchSensitivities(:,6))/3;
channelSensitivities(:,4) = (batchSensitivities(:,7)+batchSensitivities(:,8)+batchSensitivities(:,9)+batchSensitivities(:,10)+batchSensitivities(:,11)+batchSensitivities(:,12))/6;
channelSensitivities(:,6) = batchSensitivities(:,1);
channelSensitivities(:,7) = batchSensitivities(:,2);

chan1 = fit(x,channelSensitivities(:,1),'smoothingspline');
chan2 = fit(x,channelSensitivities(:,2),'smoothingspline');
chan3 = fit(x,channelSensitivities(:,3),'smoothingspline');
chan4 = fit(x,channelSensitivities(:,4),'smoothingspline');
chan5 = fit(x,channelSensitivities(:,5),'smoothingspline');
chan6 = fit(x,channelSensitivities(:,6),'smoothingspline');
chan7 = fit(x,channelSensitivities(:,7),'smoothingspline');

channelSensitivities(:,1) = chan1(x);
channelSensitivities(:,2) = chan2(x);
channelSensitivities(:,3) = chan3(x);
channelSensitivities(:,4) = chan4(x);
channelSensitivities(:,5) = chan5(x);
channelSensitivities(:,6) = chan6(x);
channelSensitivities(:,7) = chan7(x);

fprintf('fuel\n');
for i = 1:7
    fprintf('chan%i\n', i);
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(1,i), channelSensitivities(2,i), channelSensitivities(3,i), channelSensitivities(4,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(5,i), channelSensitivities(6,i), channelSensitivities(7,i), channelSensitivities(8,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(9,i), channelSensitivities(10,i), channelSensitivities(11,i), channelSensitivities(12,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(13,i), channelSensitivities(14,i), channelSensitivities(15,i), channelSensitivities(16,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(17,i), channelSensitivities(18,i), channelSensitivities(19,i), channelSensitivities(20,i));
    fprintf('%11.4e %11.4e %11.4e %11.4e\n', channelSensitivities(21,i), channelSensitivities(22,i), channelSensitivities(23,i), channelSensitivities(24,i));
end
fprintf('\n');