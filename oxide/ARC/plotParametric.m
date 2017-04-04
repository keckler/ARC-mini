transients = {'ULOHS','UTOP','ULOF'};
worths = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50];
actuationTemps = [10, 20, 30, 40, 50];
maxTemps = [975.812 975.817 975.817 975.828 981.266;
            949.518 949.606 949.632 949.645 960.508;
            919.573 922.109 923.117 923.38 939.735;
            887.331 888.931 893.107 897.204 918.541;
            885.306 880.232 882.267 887.219 896.333;
            897.331 888.187 886.229 887.619 892.834;
            899.621 905.491 918.717 932.745 935.576;
            916.88 930.01 936.561 950.496 954.504;
            949.623 936.028 897.609 1023.111 971.963;
            1221.593 945.997 916.967 932.698 945.771;
            913.065 1003.758 924.401 917.337 923.637;
            932.997 889.326 899.535 927.185 914.072;
            1124.748 1124.085 1121.807 1120.333 1130.31;
            1076.83 1074.187 1071.854 1071.322 1090.252;
            1029.768 1030.167 1030.411 1031.86 1056.36;
            1033.98 1055.952 1215.538 1223.544 1216.314;
            1221.795 1221.575 1210.329 1215.039 1217.008;
            1179.021 1176.133 1218.083 1213.105 1196.287];
maxTemps = maxTemps-273.15;

colors = {'k', 'b', 'm'};

figure;    zlim([550 950])
grid on;
xlabel('actuation temperature difference (C)')
ylabel('ARC system worth ($)')
zlabel('max coolant temperature (C)')
hold on;

[X,Y] = meshgrid(actuationTemps, worths);

i = 1;
while i < length(transients)+1
    surf(X,Y,maxTemps((i-1)*length(worths)+1:i*length(worths),:), 'FaceColor', 'interp', 'FaceAlpha', i*1/length(transients), 'EdgeColor', colors{i});%,i*ones(length(worths),length(actuationTemps)))
    
    i = i + 1;
end

legend('ULOHS', 'UTOP', 'ULOF');
zlim([min(min(maxTemps))-50, max(max(maxTemps))+20]);

plot3([10 20 30 20 10],[0.25 0.50 0.75 1.0 1.25], [min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50]);

boilingTemp = fill3([actuationTemps(1), actuationTemps(1), actuationTemps(end), actuationTemps(end)], [worths(1), worths(end), worths(end), worths(1)], [880, 880, 880, 880], 'r');
alpha(boilingTemp, 0.15)