%plots the margin to coolant boiling with increasing S for all three 
%transients. 

S = [45 55 65 75 85];

%DeltaT_{act} = 10, w = 0.87$
ULOHS = [91.57 91.55 91.53 91.51 91.48];
UTOP = [2.75 17.85 62.79 60.74 57.49];
ULOF = [185.7 187.2 188.0 187.7 187.7];

figure;
plot(S, ULOHS, '*-', S, UTOP, '^-', S, ULOF, 's-');
grid on;
legend('ULOHS', 'UTOP', 'ULOF');
xlabel('S (C)');
ylabel('margin to coolant boiling gained (C)');