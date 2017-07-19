transients = {'ULOHS','UTOP','ULOF'};
worths = [0.12, 0.25, 0.37, 0.50, 0.62, 0.75, 0.87, 1.00];
actuationTemps = [5, 10, 15, 20, 25, 30, 35, 40];
maxTemps = 
maxTemps = maxTemps-273.15;

styles = {'-', ':', '--'};

figure;    zlim([550 950])
grid on;
xlabel('actuation temperature difference (C)')
ylabel('ARC system worth ($)')
zlabel('max coolant temperature (C)')
hold on;

[X,Y] = meshgrid(actuationTemps, worths);

i = 1;
while i < length(transients)+1
    surf(X,Y,maxTemps((i-1)*length(worths)+1:i*length(worths),:), 'FaceColor', 'interp', 'FaceAlpha', i*1/length(transients), 'LineStyle', styles{i});%,i*ones(length(worths),length(actuationTemps)))
    
    i = i + 1;
end

legend('ULOHS', 'UTOP', 'ULOF');
zlim([min(min(maxTemps))-50, max(max(maxTemps))+20]);

%plot3([10 20 30 20 10],[0.25 0.50 0.75 1.0 1.25], [min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50 min(min(maxTemps))-50]);

%boilingTemp = fill3([actuationTemps(1), actuationTemps(1), actuationTemps(end), actuationTemps(end)], [worths(1), worths(end), worths(end), worths(1)], [880, 880, 880, 880], 'r');
%alpha(boilingTemp, 0.15)