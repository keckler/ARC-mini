alpha = 1E-5*[1 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2];
oscillationAmplitude = 100*[0.005 0.005 0.008 0.012 0.025 0.055 0.089 0.109 0.127]; %max amplitude of the power oscillations, normalized

plot(alpha, oscillationAmplitude,'*-');
xlabel('rod drive thermal expansion coefficient (1/K)');
ylabel('max power oscillations amplitude (percent nominal power)');
grid on;